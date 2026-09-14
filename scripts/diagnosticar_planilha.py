#!/usr/bin/env python3
"""Inventário somente leitura de pastas de trabalho .xlsx/.xlsm.

O programa nunca grava na planilha analisada. Ele gera JSON e Markdown em uma
pasta de saída separada para apoiar o diagnóstico antes/depois.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zipfile import BadZipFile, ZipFile
import xml.etree.ElementTree as ET

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CELL_RE = re.compile(r"^([A-Z]+)([0-9]+)$")
ABSOLUTE_WINDOWS_PATH_RE = re.compile(r"(?i)(?:[A-Z]:\\\\|file:///|\\\\\\\\)")
REF_ERROR_RE = re.compile(r"#REF!", re.IGNORECASE)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_xml(zip_file: ZipFile, member: str) -> ET.Element | None:
    try:
        return ET.fromstring(zip_file.read(member))
    except KeyError:
        return None
    except ET.ParseError as exc:
        raise ValueError(f"XML inválido em {member}: {exc}") from exc


def read_relationships(zip_file: ZipFile, member: str) -> dict[str, dict[str, str]]:
    root = read_xml(zip_file, member)
    if root is None:
        return {}
    result: dict[str, dict[str, str]] = {}
    for rel in root:
        rel_id = rel.attrib.get("Id")
        if rel_id:
            result[rel_id] = dict(rel.attrib)
    return result


def resolve_target(base_dir: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(base_dir, target))


def column_number(cell_ref: str) -> tuple[int, int] | None:
    match = CELL_RE.match(cell_ref.upper())
    if not match:
        return None
    col = 0
    for char in match.group(1):
        col = col * 26 + ord(char) - 64
    return col, int(match.group(2))


def shared_strings(zip_file: ZipFile) -> list[str]:
    root = read_xml(zip_file, "xl/sharedStrings.xml")
    if root is None:
        return []
    values: list[str] = []
    for item in root.findall(f"{{{NS_MAIN}}}si"):
        values.append("".join(node.text or "" for node in item.iter() if local_name(node.tag) == "t"))
    return values


def cell_value(cell: ET.Element, strings: list[str]) -> str:
    kind = cell.attrib.get("t", "")
    if kind == "inlineStr":
        return "".join(node.text or "" for node in cell.iter() if local_name(node.tag) == "t")
    value = cell.find(f"{{{NS_MAIN}}}v")
    raw = "" if value is None or value.text is None else value.text
    if kind == "s" and raw.isdigit():
        index = int(raw)
        return strings[index] if index < len(strings) else raw
    return raw


def count_objects(root: ET.Element | None) -> int:
    if root is None:
        return 0
    object_tags = {"twoCellAnchor", "oneCellAnchor", "absoluteAnchor", "shape", "control"}
    return sum(1 for node in root.iter() if local_name(node.tag) in object_tags)


def scan_text_member(zip_file: ZipFile, member: str) -> str:
    try:
        return zip_file.read(member).decode("utf-8", errors="replace")
    except KeyError:
        return ""


def inspect_workbook(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    if path.suffix.lower() not in {".xlsx", ".xlsm", ".xltx", ".xltm"}:
        raise ValueError("Formato não suportado. Use .xlsx, .xlsm, .xltx ou .xltm.")

    try:
        package = ZipFile(path)
    except BadZipFile as exc:
        raise ValueError("O arquivo não é uma pasta de trabalho Open XML válida.") from exc

    with package:
        members = set(package.namelist())
        workbook = read_xml(package, "xl/workbook.xml")
        if workbook is None:
            raise ValueError("Pacote sem xl/workbook.xml.")

        workbook_rels = read_relationships(package, "xl/_rels/workbook.xml.rels")
        strings = shared_strings(package)
        sheets: list[dict[str, Any]] = []
        total_formulas = 0
        total_ref_errors = 0
        total_objects = 0

        sheets_node = workbook.find(f"{{{NS_MAIN}}}sheets")
        for sheet in list(sheets_node or []):
            name = sheet.attrib.get("name", "")
            rel_id = sheet.attrib.get(f"{{{NS_REL}}}id", "")
            rel = workbook_rels.get(rel_id, {})
            target = resolve_target("xl", rel.get("Target", "")) if rel else ""
            root = read_xml(package, target) if target else None
            dimension = ""
            nonempty_panel = 0
            formula_count = 0
            ref_errors = 0
            table_files: list[str] = []
            drawing_files: list[str] = []
            macro_links: list[str] = []
            object_count = 0

            if root is not None:
                dim = root.find(f"{{{NS_MAIN}}}dimension")
                dimension = "" if dim is None else dim.attrib.get("ref", "")
                for cell in root.iter(f"{{{NS_MAIN}}}c"):
                    ref = column_number(cell.attrib.get("r", ""))
                    value = cell_value(cell, strings)
                    formula = cell.find(f"{{{NS_MAIN}}}f")
                    formula_text = "" if formula is None or formula.text is None else formula.text
                    if formula is not None:
                        formula_count += 1
                    ref_errors += len(REF_ERROR_RE.findall(formula_text))
                    ref_errors += len(REF_ERROR_RE.findall(value))
                    if ref and 1 <= ref[0] <= 9 and 1 <= ref[1] <= 8 and (value or formula_text):
                        nonempty_panel += 1

                sheet_dir = posixpath.dirname(target)
                sheet_file = posixpath.basename(target)
                sheet_rels_path = posixpath.join(sheet_dir, "_rels", sheet_file + ".rels")
                sheet_rels = read_relationships(package, sheet_rels_path)
                for relationship in sheet_rels.values():
                    resolved = resolve_target(sheet_dir, relationship.get("Target", ""))
                    rel_type = relationship.get("Type", "")
                    if rel_type.endswith("/table"):
                        table_files.append(resolved)
                    if rel_type.endswith("/drawing") or rel_type.endswith("/vmlDrawing"):
                        drawing_files.append(resolved)
                        drawing_root = read_xml(package, resolved)
                        object_count += count_objects(drawing_root)
                        drawing_text = scan_text_member(package, resolved)
                        macro_links.extend(
                            item.strip()
                            for item in re.findall(r"(?is)<[^>]*FmlaMacro[^>]*>(.*?)</[^>]*FmlaMacro>", drawing_text)
                            if item.strip()
                        )

            tables = []
            for table_file in table_files:
                table_root = read_xml(package, table_file)
                if table_root is not None:
                    tables.append({
                        "arquivo": table_file,
                        "nome": table_root.attrib.get("name", ""),
                        "nome_exibicao": table_root.attrib.get("displayName", ""),
                        "referencia": table_root.attrib.get("ref", ""),
                    })

            total_formulas += formula_count
            total_ref_errors += ref_errors
            total_objects += object_count
            sheets.append({
                "nome": name,
                "estado": sheet.attrib.get("state", "visible"),
                "arquivo_xml": target,
                "dimensao_usada": dimension,
                "celulas_preenchidas_A1_I8": nonempty_panel,
                "formulas": formula_count,
                "ocorrencias_ref": ref_errors,
                "tabelas": tables,
                "arquivos_desenho": drawing_files,
                "objetos_estimados": object_count,
                "macros_vinculadas_detectadas": sorted(set(macro_links)),
            })

        defined_names = []
        names_node = workbook.find(f"{{{NS_MAIN}}}definedNames")
        for item in list(names_node or []):
            defined_names.append({
                "nome": item.attrib.get("name", ""),
                "escopo_local": item.attrib.get("localSheetId"),
                "formula": item.text or "",
                "ocorrencias_ref": len(REF_ERROR_RE.findall(item.text or "")),
            })

        connections_root = read_xml(package, "xl/connections.xml")
        connections = []
        if connections_root is not None:
            for node in connections_root:
                if local_name(node.tag) == "connection":
                    connections.append({
                        "nome": node.attrib.get("name", ""),
                        "descricao": node.attrib.get("description", ""),
                        "tipo": node.attrib.get("type", ""),
                    })

        all_tables = [item for sheet in sheets for item in sheet["tabelas"]]
        external_links = sorted(m for m in members if m.startswith("xl/externalLinks/") and m.endswith(".xml"))
        query_tables = sorted(m for m in members if m.startswith("xl/queryTables/") and m.endswith(".xml"))
        custom_xml = sorted(m for m in members if m.startswith("customXml/") and m.endswith(".xml"))
        text_members = [
            m for m in members
            if m.endswith((".xml", ".rels")) and not m.startswith("docProps/")
        ]
        absolute_path_hits: list[dict[str, str]] = []
        for member in text_members:
            text = scan_text_member(package, member)
            if ABSOLUTE_WINDOWS_PATH_RE.search(text):
                absolute_path_hits.append({"arquivo": member, "observacao": "possível caminho absoluto"})

        vba_member = "xl/vbaProject.bin"
        banco = next((s for s in sheets if s["nome"].casefold() == "banco de dados".casefold()), None)
        listas = next((s for s in sheets if s["nome"].casefold() == "listas".casefold()), None)

        return {
            "gerado_em_utc": datetime.now(timezone.utc).isoformat(),
            "arquivo": path.name,
            "tamanho_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
            "extensao": path.suffix.lower(),
            "possui_vba": vba_member in members,
            "vba": {
                "arquivo": vba_member if vba_member in members else None,
                "tamanho_bytes": package.getinfo(vba_member).file_size if vba_member in members else 0,
                "componentes": "não contado sem extração especializada do vbaProject.bin",
            },
            "quantidades": {
                "abas": len(sheets),
                "tabelas": len(all_tables),
                "conexoes": len(connections),
                "query_tables": len(query_tables),
                "vinculos_externos": len(external_links),
                "nomes_definidos": len(defined_names),
                "formulas": total_formulas,
                "ocorrencias_ref": total_ref_errors + sum(n["ocorrencias_ref"] for n in defined_names),
                "objetos_estimados": total_objects,
            },
            "banco_de_dados": banco,
            "listas": listas,
            "abas": sheets,
            "tabelas": all_tables,
            "conexoes": connections,
            "query_tables": query_tables,
            "vinculos_externos": external_links,
            "nomes_definidos": defined_names,
            "custom_xml": custom_xml,
            "possiveis_caminhos_absolutos": absolute_path_hits,
            "observacoes": [
                "Diagnóstico somente leitura; o arquivo analisado não foi alterado.",
                "A contagem de objetos é estimada a partir de desenhos/VML.",
                "Conteúdo M do Power Query pode estar compactado no pacote Mashup e exige inspeção complementar.",
                "A quantidade de componentes VBA exige extração especializada do vbaProject.bin.",
            ],
        }


def markdown_report(data: dict[str, Any]) -> str:
    q = data["quantidades"]
    banco = data.get("banco_de_dados") or {}
    listas = data.get("listas") or {}
    lines = [
        "# Diagnóstico da Planilha",
        "",
        f"- Arquivo: `{data['arquivo']}`",
        f"- SHA-256: `{data['sha256']}`",
        f"- Tamanho: {data['tamanho_bytes']} bytes",
        f"- VBA presente: {'sim' if data['possui_vba'] else 'não'}",
        "",
        "## Inventário",
        "",
        "| Item | Quantidade |",
        "|---|---:|",
    ]
    for label, key in [
        ("Abas", "abas"), ("Tabelas", "tabelas"), ("Conexões", "conexoes"),
        ("Query tables", "query_tables"), ("Vínculos externos", "vinculos_externos"),
        ("Nomes definidos", "nomes_definidos"), ("Fórmulas", "formulas"),
        ("Ocorrências #REF!", "ocorrencias_ref"), ("Objetos estimados", "objetos_estimados"),
    ]:
        lines.append(f"| {label} | {q[key]} |")
    lines.extend([
        "",
        "## Áreas críticas",
        "",
        f"- Banco de Dados — dimensão: `{banco.get('dimensao_usada', 'não localizado')}`; células preenchidas em A1:I8: {banco.get('celulas_preenchidas_A1_I8', 'n/a')}.",
        f"- Listas — ocorrências #REF!: {listas.get('ocorrencias_ref', 'aba não localizada')}.",
        f"- Possíveis caminhos absolutos em XML legível: {len(data['possiveis_caminhos_absolutos'])}.",
        "",
        "## Abas",
        "",
        "| Aba | Estado | Dimensão | Fórmulas | #REF! | Tabelas | Objetos estimados |",
        "|---|---|---|---:|---:|---:|---:|",
    ])
    for sheet in data["abas"]:
        lines.append(
            f"| {sheet['nome']} | {sheet['estado']} | {sheet['dimensao_usada']} | "
            f"{sheet['formulas']} | {sheet['ocorrencias_ref']} | {len(sheet['tabelas'])} | "
            f"{sheet['objetos_estimados']} |"
        )
    lines.extend(["", "## Limitações", ""])
    lines.extend(f"- {item}" for item in data["observacoes"])
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnostica planilha sem modificá-la.")
    parser.add_argument("--arquivo", required=True, type=Path, help="Caminho da planilha .xlsx/.xlsm")
    parser.add_argument("--saida", type=Path, default=Path("diagnosticos"), help="Pasta separada de saída")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = inspect_workbook(args.arquivo.resolve())
        args.saida.mkdir(parents=True, exist_ok=True)
        stem = args.arquivo.stem
        json_path = args.saida / f"{stem}_diagnostico.json"
        md_path = args.saida / f"{stem}_diagnostico.md"
        json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(markdown_report(result), encoding="utf-8")
        print(f"[OK] Diagnóstico gerado: {json_path}")
        print(f"[OK] Relatório gerado: {md_path}")
        return 0
    except Exception as exc:
        print(f"[ERRO] {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

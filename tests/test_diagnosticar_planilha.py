from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.diagnosticar_planilha import inspect_workbook, markdown_report


class DiagnosticoPlanilhaTests(unittest.TestCase):
    def criar_planilha_sintetica(self, path: Path) -> None:
        parts = {
            "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>""",
            "xl/workbook.xml": """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
 <sheets>
  <sheet name="Banco de Dados" sheetId="1" r:id="rId1"/>
  <sheet name="Listas" sheetId="2" r:id="rId2"/>
 </sheets>
 <definedNames><definedName name="Quebrado">#REF!</definedName></definedNames>
</workbook>""",
            "xl/_rels/workbook.xml.rels": """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
 <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
</Relationships>""",
            "xl/worksheets/sheet1.xml": """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
 <dimension ref="A1:I58"/>
 <sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>Executor Atual</t></is></c></row></sheetData>
 <tableParts count="1"><tablePart r:id="rId1"/></tableParts>
</worksheet>""",
            "xl/worksheets/sheet2.xml": """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
 <dimension ref="A1:A2"/>
 <sheetData><row r="1"><c r="A1"><f>#REF!+1</f><v>#REF!</v></c></row></sheetData>
</worksheet>""",
            "xl/worksheets/_rels/sheet1.xml.rels": """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/table" Target="../tables/table1.xml"/>
</Relationships>""",
            "xl/tables/table1.xml": """<?xml version="1.0" encoding="UTF-8"?>
<table xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 name="tbBanco" displayName="tbBanco" ref="A1:I58"/>""",
            "xl/connections.xml": """<?xml version="1.0" encoding="UTF-8"?>
<connections xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
 <connection id="1" name="Consulta Banco" type="5"/>
</connections>""",
            "xl/vbaProject.bin": b"VBA-SINTETICO",
            "xl/externalLinks/externalLink1.xml": "<externalLink/>",
        }
        with ZipFile(path, "w") as package:
            for name, content in parts.items():
                package.writestr(name, content)

    def test_inventario_basico(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workbook = Path(temp) / "controle.xlsm"
            self.criar_planilha_sintetica(workbook)
            result = inspect_workbook(workbook)

        self.assertEqual(result["quantidades"]["abas"], 2)
        self.assertEqual(result["quantidades"]["tabelas"], 1)
        self.assertEqual(result["quantidades"]["conexoes"], 1)
        self.assertEqual(result["quantidades"]["vinculos_externos"], 1)
        self.assertTrue(result["possui_vba"])
        self.assertEqual(result["banco_de_dados"]["dimensao_usada"], "A1:I58")
        self.assertEqual(result["banco_de_dados"]["celulas_preenchidas_A1_I8"], 1)
        self.assertGreaterEqual(result["quantidades"]["ocorrencias_ref"], 3)

    def test_relatorio_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            workbook = Path(temp) / "controle.xlsm"
            self.criar_planilha_sintetica(workbook)
            report = markdown_report(inspect_workbook(workbook))

        self.assertIn("# Diagnóstico da Planilha", report)
        self.assertIn("Banco de Dados", report)
        self.assertIn("A1:I58", report)

    def test_rejeita_formato_nao_suportado(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "controle.xls"
            file.write_bytes(b"nao suportado")
            with self.assertRaises(ValueError):
                inspect_workbook(file)


if __name__ == "__main__":
    unittest.main()

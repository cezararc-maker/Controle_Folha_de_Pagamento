# Ferramentas de Diagnóstico

## Executar

No diretório raiz do repositório, com Python 3.11 ou superior:

```powershell
python .\scripts\diagnosticar_planilha.py --arquivo ".\entrada\NOME_DO_ARQUIVO.xlsm"
```

A ferramenta:

- abre o pacote Open XML somente para leitura;
- calcula SHA-256;
- inventaria abas, tabelas, conexões, vínculos, nomes, fórmulas e presença de VBA;
- mede ocupação de `A1:I8` em `Banco de Dados`;
- registra `#REF!` detectável em fórmulas/valores;
- cria JSON e Markdown em `diagnosticos/`;
- não salva nem altera a pasta de trabalho.

## Testar a ferramenta

```powershell
python -m unittest discover -s tests -v
```

## Limitações deliberadas

O script não edita Excel e não promete analisar integralmente o binário `vbaProject.bin` ou o pacote Mashup do Power Query. Esses elementos exigirão diagnóstico complementar no Excel/Windows quando a planilha real estiver disponível.

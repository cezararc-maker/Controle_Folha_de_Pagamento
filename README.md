# Controle de Folha de Pagamento

Projeto para replicação, parametrização e distribuição controlada da planilha de controle de folha.

## Situação

- Repositório oficial: `cezararc-maker/Controle_Folha_de_Pagamento`
- Branch padrão: `main`
- Branch do protótipo: `codex/prototipo-painel-banco-dados`
- Planilha-fonte no GitHub: **ainda não recebida**
- Implantação definitiva: **não aprovada**

A documentação e o diagnóstico preventivo já estão preparados. A edição de VBA, Power Query, painel, fórmulas ou objetos só começará depois que a pasta de trabalho original estiver em `entrada/` e o baseline real tiver sido registrado.

## Documentação

- [Fluxo e situação](FLUXOGRAMA_DO_PROJETO.md)
- [Diagnóstico histórico de referência](docs/DIAGNOSTICO_DE_REFERENCIA.md)
- [Especificação do protótipo](docs/ESPECIFICACAO_PROTOTIPO.md)
- [Plano de implementação](docs/PLANO_DE_IMPLEMENTACAO.md)
- [Matriz de testes](docs/MATRIZ_DE_TESTES.md)
- [Como executar o diagnóstico](docs/COMO_EXECUTAR_DIAGNOSTICO.md)
- [Como adicionar a planilha-fonte](entrada/README.md)

## Primeiro passo pendente

Adicionar a pasta de trabalho original, fechada no Excel e sem conversões, à pasta `entrada/` na branch do protótipo.

Depois disso, será executado:

```powershell
python .\scripts\diagnosticar_planilha.py --arquivo ".\entrada\NOME_DO_ARQUIVO.xlsm"
```

O script é somente leitura e gera relatórios separados em `diagnosticos/`.

## Regras de trabalho

- O GitHub é a única fonte oficial dos arquivos do projeto.
- Alterações são feitas em branch própria e submetidas para validação.
- Mudanças sensíveis exigem diagnóstico, impacto quantificado, teste e registro.
- Nenhuma versão será considerada aprovada para implantação definitiva sem validação expressa.
- Valores, fórmulas, formatos, macros, consultas, tabelas, vínculos, históricos e lançamentos fora do escopo devem ser preservados.
- Os 22 erros `#REF!` observados anteriormente na aba `Listas` são preexistentes e não serão corrigidos nesta fase.

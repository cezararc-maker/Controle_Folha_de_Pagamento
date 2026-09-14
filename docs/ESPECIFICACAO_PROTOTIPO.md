# Especificação do Protótipo — Banco de Dados

## Objetivo

Criar um painel compacto acima da tabela da aba `Banco de Dados`, parametrizar a origem da consulta e substituir o filtro literal do executor por uma seleção controlada, preservando integralmente o restante da pasta de trabalho.

## Layout alvo

| Área | Uso |
|---|---|
| `A1:I7` | Painel compacto |
| Linha 8 | Separação visual |
| Linha 9 em diante | Tabela existente do banco, deslocada com preservação de estrutura |

O layout é alvo de protótipo, não autorização para alterar a pasta sem diagnóstico real.

## Controles previstos

- Identificação do arquivo de origem.
- Seleção do executor em lista proveniente da planilha de origem.
- Ação de atualização do banco.
- Indicador de estado: pronto, processando, concluído com sucesso ou erro.
- Mensagem resumida no painel e registro técnico completo em log.
- Acesso à aba `Cadastro Empresas`.

Não serão movidas nesta fase as ações `Consultar CNPJ` e `Importar via CNPJ`.

## Contrato da consulta

A consulta deve manter:

1. Detecção automática da aba mensal mais recente cujo nome siga `MÊS AAAA`.
2. Validação explícita dos cabeçalhos necessários.
3. Exatamente estas nove colunas, nesta ordem:
   - Executor Atual
   - Situação
   - COD. Sistema
   - CNPJ/CPF/CAEPF/CEI
   - RAZÃO SOCIAL
   - DETALHES
   - ENVIAR POR EMAIL
   - PROLABORE
   - GRUPO EMPRESARIAL
4. Origem configurável, sem caminho absoluto gravado na expressão M.
5. Filtro do executor baseado no valor selecionado em lista, sem literal `CEZAR`.

## Tratamento de erros

- Nenhuma caixa modal durante atualização em segundo plano.
- O painel recebe uma mensagem curta e acionável.
- O log recebe etapa, data/hora, tipo do erro, mensagem completa e contexto disponível.
- Falha ao carregar a lista de executores deve deixar o controle desabilitado e registrar a causa; nunca exibir caixa vazia.

## Testes obrigatórios

- Comparação antes/depois de abas, tabelas, nomes, conexões, vínculos, componentes VBA e fórmulas.
- Atualização com a origem que anteriormente retornou 57 registros, quando essa massa estiver disponível no repositório.
- Seleção de executor válida e lista sem valores vazios/duplicados.
- Ausência de caminho absoluto específico do operador.
- Competência mais recente correta.
- Cabeçalhos ausentes produzem erro controlado.
- As nove colunas permanecem na ordem definida.
- Objetos homônimos do menu são validados por posição e macro vinculada.
- Os `#REF!` preexistentes na aba `Listas` não aumentam por causa do protótipo.

## Fora do escopo desta fase

- Correção dos `#REF!` preexistentes.
- Limpeza de dados para distribuição.
- Redesenho das rotinas de CNPJ.
- Implantação definitiva.

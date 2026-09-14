# Diagnóstico de Referência

> Este documento registra observações do protótipo local anterior. Elas orientam o trabalho, mas **não comprovam** o estado da futura planilha-fonte do GitHub. Todos os números deverão ser refeitos e comparados após o arquivo original ser versionado.

## Inventário anteriormente observado

| Item | Quantidade/estado observado |
|---|---|
| Abas | 18 |
| Tabelas | 6 |
| Consultas Power Query | 1 |
| Componentes VBA | 29 |
| Registros na tabela do banco | 57 |
| Executor dos registros observados | CEZAR |
| Área então ocupada no banco | `A1:I58` |
| Erros `#REF!` na aba `Listas` | 22 |
| Objetos homônimos para abrir Banco de Dados | 3 |

## Consulta observada

A consulta:

- usava caminho fixo para o arquivo de origem;
- aplicava filtro literal equivalente a `Executor Atual = CEZAR`;
- já detectava automaticamente a competência mensal mais recente;
- retornava nove colunas:
  1. Executor Atual;
  2. Situação;
  3. COD. Sistema;
  4. CNPJ/CPF/CAEPF/CEI;
  5. RAZÃO SOCIAL;
  6. DETALHES;
  7. ENVIAR POR EMAIL;
  8. PROLABORE;
  9. GRUPO EMPRESARIAL.

Em teste local não versionado, a origem parametrizada atualizou 57 registros. Esse resultado deverá ser reproduzido no arquivo oficial antes de ser aceito.

## VBA e interface observados

- As macros de CNPJ dependem da seleção na aba `Cadastro Empresas`.
- Essas macros não devem ser conectadas diretamente à tabela da aba `Banco de Dados`.
- `SincronizarEmpresasAtivas` atualiza Cadastro/Controle Mensal; não substitui a atualização do Power Query.
- Havia três objetos homônimos para abrir `Banco de Dados`; identificação apenas pelo nome é insegura. Devem ser comparados posição, tipo, ação/macro vinculada e folha hospedeira.
- A tentativa anterior de lista de executores falhou antes do carregamento.
- Uma caixa de mensagem vazia revelou falha de tratamento de erro.
- Novas rotinas não devem abrir caixas modais durante execução em segundo plano; devem registrar erro completo em painel/log.

## Hipóteses a confirmar

- O arquivo oficial é uma pasta de trabalho Open XML com macros (`.xlsm`).
- Os 29 componentes VBA ainda existem e são acessíveis.
- A consulta continua com a mesma estrutura.
- A tabela do banco ainda começa em `A1`.
- Os 22 `#REF!` continuam restritos ao problema preexistente conhecido.
- As macros e os objetos não sofreram alteração desde o protótipo local.

Nenhuma hipótese acima autoriza modificação automática.

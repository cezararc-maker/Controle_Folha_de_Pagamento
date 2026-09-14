# Matriz de Testes

| ID | Cenário | Resultado esperado | Estado |
|---|---|---|---|
| REP-001 | Repositório e branch | Repositório único; `main` como padrão; trabalho em branch própria | Concluído |
| BAS-001 | Planilha-fonte presente | Arquivo original existe em `entrada/` e não é temporário | Bloqueado |
| BAS-002 | Hash da origem | SHA-256 registrado | Bloqueado |
| BAS-003 | Inventário estrutural | Abas, tabelas, conexões, vínculos, nomes e VBA quantificados | Bloqueado |
| REF-001 | Erros preexistentes | Contagem real registrada; nenhuma correção nesta fase | Bloqueado |
| PQ-001 | Origem parametrizada | Atualiza sem caminho absoluto específico do operador | Pendente |
| PQ-002 | Mês mais recente | Seleciona corretamente aba no padrão `MÊS AAAA` | Pendente |
| PQ-003 | Cabeçalhos válidos | Prossegue e retorna nove colunas na ordem contratada | Pendente |
| PQ-004 | Cabeçalho ausente | Falha controlada e log completo, sem caixa vazia | Pendente |
| PQ-005 | Equivalência | Mesma origem produz mesma massa do baseline; referência histórica: 57 registros | Pendente |
| EXE-001 | Carregar executores | Lista distinta, ordenada e sem vazios | Pendente |
| EXE-002 | Selecionar executor | Apenas item da lista; sem entrada livre | Pendente |
| EXE-003 | Falha de lista | Controle desabilitado, painel informa erro e log detalha causa | Pendente |
| UI-001 | Impacto de `A1:I8` | Todos os conteúdos/dependências quantificados antes da edição | Pendente |
| UI-002 | Painel | Painel em `A1:I7`, linha 8 separadora e tabela desde linha 9 | Pendente |
| UI-003 | Cadastro | Painel abre `Cadastro Empresas`; ações de CNPJ continuam lá | Pendente |
| OBJ-001 | Objetos homônimos | Três objetos validados por posição e vínculo, não só pelo nome | Pendente |
| REG-001 | Preservação | Abas, tabelas, VBA, consultas, vínculos, fórmulas e históricos fora do escopo intactos | Pendente |
| REG-002 | `#REF!` | Protótipo não aumenta a contagem do baseline | Pendente |
| DST-001 | Limpeza | Matriz de limpeza definida e aprovada antes de executar | Fora desta fase |

## Regra de evidência

Cada execução futura deve registrar arquivo/hash, commit testado, ambiente do Excel, data, resultado e evidência suficiente para reprodução.

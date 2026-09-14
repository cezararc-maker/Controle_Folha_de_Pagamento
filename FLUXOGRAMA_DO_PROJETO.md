# Fluxograma do Projeto

Atualizado em: 14/09/2026  
Branch de trabalho: `codex/prototipo-painel-banco-dados`  
Pull request: [#1 — Preparar baseline e diagnóstico do protótipo](https://github.com/cezararc-maker/Controle_Folha_de_Pagamento/pull/1)  
Implantação definitiva: **NÃO APROVADA**

## Fluxo de trabalho

| Etapa | Situação | Resultado/Teste | Pendências | Aprovação definitiva |
|---|---|---|---|---|
| 0. Confirmar repositório | Concluída | Repositório único confirmado: `cezararc-maker/Controle_Folha_de_Pagamento`; padrão `main`; inicialmente vazio | Nenhuma | Não se aplica |
| 1. Criar base recuperável | Concluída | Commit inicial `e2e110b` em `main`; branch de trabalho criada | Nenhuma | Não se aplica |
| 2. Receber planilha-fonte no GitHub | Bloqueada | Nenhuma pasta de trabalho existe no repositório | Adicionar a versão original, fechada no Excel, em `entrada/` | Não |
| 3. Diagnóstico reproduzível | Ferramenta validada; fonte pendente | Compilação e 3 testes sintéticos aprovados no GitHub Actions, execução [#34878902794](https://github.com/cezararc-maker/Controle_Folha_de_Pagamento/actions/runs/34878902794) | Executar contra a planilha real e confrontar com o diagnóstico de referência | Não |
| 4. Parametrizar origem | Pendente | Sem alteração | Identificar consulta, parâmetros e fonte real; remover caminho fixo sem alterar a lógica das nove colunas | Não |
| 5. Lista de executores | Pendente | Sem alteração | Identificar tabela/coluna de origem e implementar seleção sem digitação livre | Não |
| 6. Painel `Banco de Dados` | Pendente | Sem alteração | Quantificar impacto em `A1:I8`; deslocar tabela para linha 9 preservando objetos, fórmulas, estilos e vínculos | Não |
| 7. Testes iniciais | Pendente | Sem alteração | Atualização com 57 registros; mês mais recente; cabeçalhos; nove colunas; logs sem caixas modais | Não |
| 8. Versão limpa para distribuição | Fora desta etapa | Não iniciado | Definir formalmente o que será limpo e testar em cópia própria | Não |
| 9. Validação do usuário | Pendente | PR em rascunho para revisão inicial | Validação expressa | Não |

## Conteúdo atualmente versionado

- documentação do estado, referência histórica, especificação, plano e matriz de testes;
- instruções de inclusão da planilha-fonte;
- diagnóstico Open XML somente leitura;
- testes automatizados com arquivo sintético;
- validação contínua em Python 3.11.

## Decisões preservadas

- Painel aproximado em `A1:I7`, separação na linha 8 e tabela iniciando na linha 9.
- `Consultar CNPJ` e `Importar via CNPJ` permanecem em `Cadastro Empresas`; o painel terá apenas acesso ao cadastro.
- Origem do Power Query sem caminho fixo.
- Executor escolhido em lista carregada da origem; sem digitação livre.
- Preservar detecção da aba mensal mais recente no padrão `MÊS AAAA`, validação de cabeçalhos e nove colunas de saída.
- Preservar conteúdo fora do escopo.
- Os 22 `#REF!` relatados na aba `Listas` são preexistentes, serão quantificados e documentados, mas não corrigidos nesta fase.
- Os três objetos homônimos do menu serão diferenciados por vínculo e posição, não apenas por nome.
- Erros de atualização devem aparecer no painel/log completo; rotinas em segundo plano não devem abrir caixas modais.

## Critérios mínimos do primeiro diagnóstico real

1. Hash SHA-256 e tamanho do arquivo.
2. Tipo de pasta de trabalho e presença de VBA.
3. Abas, tabelas, consultas/conexões, vínculos externos e nomes definidos.
4. Dimensão usada e ocupação de `A1:I8` em `Banco de Dados`.
5. Referência atual da tabela do banco.
6. Contagem de ocorrências `#REF!`, com separação da aba `Listas` quando tecnicamente possível.
7. Inventário de objetos/desenhos e vínculos de macro na área afetada.
8. Resultado registrado antes de qualquer edição.

## Regra de aprovação

“Teste concluído” significa apenas que a alteração passou no cenário registrado. “Aprovado para implantação definitiva” somente poderá ser marcado após manifestação expressa do usuário.

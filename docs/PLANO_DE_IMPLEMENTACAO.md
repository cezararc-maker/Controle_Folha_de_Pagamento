# Plano de Implementação

## Princípio de segurança

Cada etapa deverá produzir um commit recuperável, um diagnóstico antes/depois e um resultado de teste. Uma etapa não será misturada com correções fora do escopo.

## Etapa 1 — Baseline oficial

1. Adicionar a planilha original em `entrada/`.
2. Calcular hash SHA-256.
3. Executar o diagnóstico somente leitura.
4. Conferir o inventário real contra `DIAGNOSTICO_DE_REFERENCIA.md`.
5. Registrar diferenças sem corrigi-las.

**Saída:** baseline documentada e commit identificável.

## Etapa 2 — Parametrização da origem

1. Identificar a consulta Power Query pelo nome e conteúdo real.
2. Localizar o caminho absoluto atualmente embutido.
3. Criar parâmetro armazenado em célula/tabela nomeada adequada.
4. Alterar somente a etapa de origem da expressão M.
5. Preservar detecção do mês mais recente, validação de cabeçalhos, tipos e nove colunas.
6. Testar origem válida, origem ausente e arquivo inacessível.

**Aceite técnico:** nenhum caminho específico do operador no código da consulta; resultado equivalente ao baseline para a mesma origem.

## Etapa 3 — Executor selecionável

1. Identificar a coluna `Executor Atual` na origem real.
2. Gerar lista distinta, sem vazios e com ordenação previsível.
3. Publicar essa lista em intervalo/tabela de apoio apropriado.
4. Ligar o seletor do painel à lista usando controle compatível com Excel.
5. Substituir o literal `CEZAR` por parâmetro validado.
6. Se a lista falhar, desabilitar atualização e registrar erro completo, sem caixa modal vazia.

**Aceite técnico:** somente valores provenientes da origem podem ser selecionados.

## Etapa 4 — Painel e deslocamento da tabela

1. Inventariar valores, fórmulas, formatos, nomes, validações, objetos, linhas/colunas ocultas e vínculos existentes em `A1:I8`.
2. Identificar a tabela real por nome e referência.
3. Medir fórmulas, macros, consultas e objetos que referenciam a área.
4. Criar commit de recuperação imediatamente antes da mudança.
5. Inserir/deslocar preservando dependências; não reconstruir a tabela por cópia simples.
6. Montar painel em `A1:I7`, separação na linha 8 e tabela na linha 9.
7. Adicionar somente um acesso a `Cadastro Empresas`.
8. Não mover as ações de CNPJ.

**Aceite técnico:** conteúdo fora do escopo e todos os inventários preservados; tabela funcional na nova posição.

## Etapa 5 — Estado e log

Estados mínimos:

- Pronto;
- Carregando executores;
- Atualizando;
- Concluído;
- Erro.

O painel mostrará resumo. O log técnico deverá registrar, no mínimo:

- data/hora;
- etapa;
- executor selecionado;
- origem resolvida sem expor credenciais;
- tipo e descrição completa do erro;
- procedimento/módulo;
- número do erro VBA, quando houver;
- resultado da atualização da consulta.

Não usar caixas modais em eventos assíncronos ou de atualização.

## Etapa 6 — Regressão

Comparar antes/depois:

- 18 abas ou quantidade real do baseline;
- 6 tabelas ou quantidade real;
- 1 consulta ou quantidade real;
- 29 componentes VBA ou quantidade real;
- nomes definidos;
- conexões e vínculos;
- fórmulas;
- estilos relevantes;
- objetos e ações vinculadas;
- contagem de `#REF!`;
- resultado e ordem das nove colunas.

## Etapa futura — Distribuição limpa

Será definida separadamente. Antes de apagar qualquer conteúdo, deverá existir uma matriz explícita com:

- aba/tabela/intervalo;
- dado a limpar;
- dado a preservar;
- justificativa;
- método de teste;
- aprovação do usuário.

A limpeza jamais será aplicada sobre a planilha-fonte.

# Algoritmo para Simplificação de Gramática

Este projeto é uma implementação de um simplificador de gramáticas livres de contexto. O sistema realiza operações para simplificar gramáticas no formato de Produções Regulares (Produções no estilo "A -> aB" ou "A -> a") eliminando produções inúteis, vazias e unitárias.

A simplificação de gramáticas livres de contexto visa otimizar o parsing sem alterar o poder de geração da gramática. O processo envolve três etapas principais: eliminar produções inúteis (não alcançáveis ou que não geram terminais), eliminar produções vazias (h) e remover produções unitárias (do tipo A -> B). Essas simplificações tornam a gramática mais eficiente e fácil de processar, mantendo a mesma linguagem gerada.

## Funcionalidades
O simplificador suporta as seguintes operações:

1. **Eliminação de Produções Vazias** \
Remove produções da forma `A -> h` (onde `h` representa a cadeia vazia) e ajusta as demais produções para garantir consistência.

2. **Eliminação de Produções Unitárias** \
Remove produções unitárias da forma `A -> B`, onde `A` e `B` são variáveis.

3. **Eliminação de Produções Inúteis** \
Remove variáveis que não geram terminais ou que não são alcançáveis a partir da variável inicial.

4. **Simplificação Geral** \
Aplica todas as etapas acima sequencialmente, gerando uma gramática simplificada.

5. **Persistência**
    - Carregar gramática de um arquivo de texto.
    - Salvar gramática simplificada em um arquivo de texto.

## Formato do Arquivo de Gramática

Os arquivos de gramática devem seguir o formato:

1. Primeira linha: lista de variáveis separadas por espaço. \
Exemplo: `S A B`

2. Segunda linha: variável inicial. \
Exemplo: `S`

3. Linhas subsequentes: produções no formato variável produção. \
Exemplo:  
    ```
    S aS  
    S bA  
    A h 
    ```


# Etapa 2 – Implementação das Classes de Grafo

## Descrição

Nesta etapa foi desenvolvido um protótipo funcional em Java para a manipulação e análise de grafos. O sistema permite carregar diferentes conjuntos de dados a partir de arquivos CSV, selecionar a representação interna do grafo e executar operações básicas por meio de um menu interativo no terminal.

---

## Estrutura de Classes

O sistema é composto pelas seguintes classes:

- **AbstractGraph**  
  Classe abstrata que define a estrutura base do grafo, bem como os métodos comuns às diferentes implementações.

- **AdjacencyListGraph**  
  Implementação do grafo utilizando lista de adjacência.

- **AdjacencyMatrixGraph**  
  Implementação do grafo utilizando matriz de adjacência.

- **GraphLoader**  
  Classe responsável pela leitura dos arquivos CSV e pelo carregamento dos vértices e arestas do grafo.

- **Main**  
  Classe principal responsável pela interação com o usuário, permitindo a escolha do grafo, da representação e a execução das operações disponíveis.

- **TestAdjacencyListGraph**  
  Conjunto de testes básicos para validação da implementação utilizando lista de adjacência.

- **TestAdjacencyMatrixGraph**  
  Conjunto de testes básicos para validação da implementação utilizando matriz de adjacência.

---

## Execução do Programa

### Compilação

No diretório `src`, execute o comando:

```bash
javac -encoding UTF-8 graph/*.java

```

```bash
java graph.Main

```
---
### Seleção do Grafo
Ao iniciar o programa, o usuário pode escolher qual conjunto de dados deseja carregar:
+ Comentários
+ Closures
+ Reviews
+ Integrado

---
### Seleção da Representação
+ Matriz de Adjacência
+ Lista de Adjacência

---
### Operações Disponíveis 
+ Mostrar o grafo
+ Verificar se o grafo é vazio
+ Verificar se o grafo é completo
+ Verificar se o grafo é conexo
+ Reiniciar o programa para escolher outro grafo
+ Encerrar 

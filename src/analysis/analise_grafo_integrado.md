# Métricas de centralidade

## Grau

Foi utilizada a função `out_degree()`, passando o grafo como argumento, para obter o grau de saída de todos os vértices do grafo. O grau de saída de um vértice representa quantas interações o colaborador realizou.

Quem participa mais ativamente das revisões, discussões ou coedições é o vértice 180. Apenas 33 colaboradores tem 3 ou mais interações. Dos 287 colaboradores, 102 não realizou nenhum comentário em issues ou pull requests, não fechou issues nem revisou pull requests.

## Centralidade de intermediações

Foi utilizada a função `bridges()`, para obtermos as arestas que agem como pontes no grafo. Em seguida, obtemos dessa lista de arestas, os vértices de origem da aresta, pois esses vértices de origem correspondem as colaboradores que comentaram em pull requests ou issues, fecharam issues ou realizaram revisões em pull requests.

Existem 112 colaboradores que atuam como "pontes" entre diferentes grupos ou áreas do projeto.

## Centralidade de Proximidade

Foi utilizado a função `closeness_centrality()`, para obtermos a medida de proximidade de centralidade de todos os vértices do grafo.

Analisando os valores obtidos, vemos que nenhum vértice tem valor maior que 0.21 (de um máximo de 1). Dos 287 vértices, 155 tem valor entre 0.10 e 0.21, e 132 (46%) tem valor entre 0.00 e 0.10. Com isso, podemos concliuir que nenhum vértice tem acesso rápido aos outros vértices do grafo, e o valor de proximidade de centralidade dos vértices do grafo é muito pequeno.

## PageRank/Eigenvector centrality

Foi utilizada a função `pagerank()` para se obter os valores de PageRank de todos os vértices do grafo.

Analisando os valores obtidos, o maior é de 0.08, de um único vértice. Valores maiores que 0.0099999, tem apenas 10 vértices. Todos os outros tem valores menores que 0.01. Sendo o valor máximo de pagerank 1, podemos concluir que nenhum vértice tem uma influência significativa sobre os outros vértices do grafo. Existem poucos colaboradores influentes no repositório analisado.

# Métricas de Estrutura e Coesão

## Densidade de rede

Foi utilizada a função `density()` para obter a densidade do grafo. O valor obtido foi 0.0057, de um máximo de 1, o que significa que poucos colaboradores comentam em issues e pull requests, fazem merge de pull requests ou fecham issues, sendo o repositório pouco colaborativo.

## Coeficiente de aglomeração

Foi utilizada a função `clustering()` para obter o coeficiente de aglomeração de todos os vértices do grafo.

253 vértices tem o coeficiente de aglomeração igual a 0. Apenas 2 vértices têm o coeficiente igual a 1, que é o valor máximo possível. Considerando então que 88% dos vértices tem o coeficiente de aglomeração igual a 0, podemos concluir que o grafo tem uma estrutura simples com poucas aglomerações de vértices fortemente conectados, e que a tendência de formar clusters é baixa. Isso também significa que o repositório tem uma tendência muito baixa de formarem-se pequenos grupos de colaboradores que interagem muito entre si.

## Assortatividade

Foi utilizada a função `degree_assortativity_coefficient()` para se obter a assortatividade do grafo.

O valor obtido foi de -0.3668 (de um mínimo de -1 e máximo de 1), o que significa que vértices de graus maiores tendem a interagir com outros vértices de graus menores e vice-versa, o que se traduz para o fato de que colaboradores que interagem muito tendem a interagir com outros colaboradores que interagem pouco. Esse valor também significa que o grau de um vértice não auxilia na identificação do grau de seus vértices vizinhos.

# Métricas de comunidade

## Detecção de comunidades

Foi utilizada a função `greedy_modularity_communities()` para se obter as comunidades do grafo. Existem 28 comunidades no grafo, ou seja, 28 times informais dentro do projeto. Desses 28 times, 12 deles tem pelo menos 3 colaboradores; o maior time tem 47 colaboradores.

## Bridging ties

Foi utilizada a função `betweeness_centrality()`, que retorna o valor de betweeness centrality de todos os vértices do grafo. A betweenness centrality mede a importância de um vértice como intermediário na rede, contabilizando a fração de caminhos mínimos entre pares de vértices que passam por ele. Quanto maior esse valor, mais caminhos mínimos dependem dele, ou seja, mais ele atua como elo estrutural e maior a tendência dele ser uma ponte entre comunidades.

230 vértices obtiveram um valor de betweeness centrality de 0. 57 dos vértices tem valor maior que 0, ou seja, existem no máximo 57 pontes no grafo. Desses 57 vértices, 4 deles tem um valor maior que 1. Provavelmente existem poucas pontes no grafo.

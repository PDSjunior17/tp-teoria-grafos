import networkx as nx
G = nx.read_gexf("data/processed/vercel_next.js_integrated.gexf")

# # Métrica centralidade 1 - Grau

var = list(G.out_degree(G))

print("\nLista de vértices do grafo, com seus respectivos graus, em ordem decrescente:")

sorted_data = sorted(var, key=lambda x: x[1], reverse=True)
print(sorted_data)

biggest_degree_vertex = 0
biggest_degree = var[0][1]
for _, degree in var:
    if degree > biggest_degree:
        biggest_degree = degree
        biggest_degree_vertex = _

print("\n O maior grau do grafo é igual a", biggest_degree, "\b, correspondente ao nodo", biggest_degree_vertex, "que representa o colaborador icyJoseph.")

# Métrica centralidade 2

var1 = list(nx.bridges(G.to_undirected()))

print("\nArestas que atuam como pontes no grafo:\n", var1)

bridge_repetition_checker = [var1[0][0]]
for bridge, _ in var1:
    if bridge not in bridge_repetition_checker:
        bridge_repetition_checker.append(bridge)

print("\nOs vértices que representam colaboradores que atuam como \"pontes\" no projeto são:\n", bridge_repetition_checker, "\n")

# Métrica centralidade 3

print("Vértices e seus respectivos valores de proximidade:\n", nx.closeness_centrality(G))

dict_closeness = nx.closeness_centrality(G)

maximum_value = max(dict_closeness.values())

print("\nO maior valor de centralidade de proximidade no grafo é", maximum_value, "correspondente ao colaborador icyJoseph, o vértice 180.")

# Métrica centralidade 4

var2 = nx.pagerank(G)

# print(var2)

print("\nOs vértices e seus respectivos valores de PageRank são:\n")

for key, value in var2.items():
    print(f"{key}: {value}")

# Métricas de Estrutura e Coesão 1

print("\nO coeficiente de aglomeração do grafo é igual a", nx.density(G))

# Métricas de Estrutura e Coesão 2

var3 = nx.clustering(G)

print("\nOs vértices e seus respectivos valores de coeficiente de aglomeração são:")

print(var3)

print("\n", list(var3.values()).count(0), "vértices tem o valor igual a 0. O valor mínimo e máximo dentre os valores encontrados são, respectivamente:", min(var3.values()), "e", max(var3.values()))

# Métricas de Estrutura e Coesão 3

var4 = nx.degree_assortativity_coefficient(G)

print("\n O coeficiente de assortatividade do grafo é", var4)

# Métricas de Comunidade 1

var5 = nx.community.greedy_modularity_communities(G)
# print("\n", var5)

print("\n As comunidades detectadas no grafo são:\n")

for frozenset in var5:
    print(frozenset)

# # Métricas de Comunidade 2

var6 = nx.betweenness_centrality(G)

more_than_zero_values = {k: v for k, v in var6.items() if v != 0}

total_zero_values = 287 - len(more_than_zero_values)

print("\nExistem", total_zero_values, "vértices que tem o valor de betweeness centrality igual a 0.")
print("\nOs possíveis bridging ties no grafo são:\n", more_than_zero_values)

# import networkx as nx
# import matplotlib.pyplot as plt
# pos = nx.spring_layout(G)
# plt.figure(figsize=(10, 8))
# nx.draw(G, pos,
#         with_labels=True,
#         node_color='skyblue',
#         node_size=500,
#         edge_color='gray',
#         font_size=10)
# plt.title("GEXF Graph Visualization")
# plt.show()

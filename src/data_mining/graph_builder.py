"""
Módulo para construção dos grafos a partir dos dados coletados
Trabalho Prático - Teoria de Grafos e Computabilidade
"""

import json
import os
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class GraphBuilder:
    """Classe para construir grafos a partir dos dados do GitHub"""
    
    def __init__(self, data_file: str):
        """
        Inicializa o construtor de grafos
        
        Args:
            data_file: Caminho para o arquivo JSON com os dados coletados
        """
        with open(data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.users = self.data['users']
        self.user_to_id = {user: i for i, user in enumerate(self.users)}
        self.id_to_user = {i: user for i, user in enumerate(self.users)}
        
        # Grafos separados
        self.graph_comments = defaultdict(lambda: defaultdict(int))
        self.graph_closures = defaultdict(lambda: defaultdict(int))
        self.graph_reviews = defaultdict(lambda: defaultdict(int))
        
        # Grafo integrado
        self.graph_integrated = defaultdict(lambda: defaultdict(float))
    
    def build_separate_graphs(self):
        """Constrói os 3 grafos separados conforme especificação"""
        
        print("\n=== Construindo Grafos Separados ===")
        
        # Grafo 1: Comentários em issues e PRs
        print("Grafo 1: Comentários...")
        for commenter, author in self.data['interactions']['issue_comments']:
            u = self.user_to_id[commenter]
            v = self.user_to_id[author]
            self.graph_comments[u][v] += 1
        
        for commenter, author in self.data['interactions']['pr_comments']:
            u = self.user_to_id[commenter]
            v = self.user_to_id[author]
            self.graph_comments[u][v] += 1
        
        # Grafo 2: Fechamento de issues
        print("Grafo 2: Fechamentos de issues...")
        for closer, author in self.data['interactions']['issue_closures']:
            u = self.user_to_id[closer]
            v = self.user_to_id[author]
            self.graph_closures[u][v] += 1
        
        # Grafo 3: Reviews, Approvals e Merges de PRs
        print("Grafo 3: Reviews/Approvals/Merges...")
        for reviewer, author in self.data['interactions']['pr_reviews']:
            u = self.user_to_id[reviewer]
            v = self.user_to_id[author]
            self.graph_reviews[u][v] += 1
        
        for approver, author in self.data['interactions']['pr_approvals']:
            u = self.user_to_id[approver]
            v = self.user_to_id[author]
            self.graph_reviews[u][v] += 1
        
        for merger, author in self.data['interactions']['pr_merges']:
            u = self.user_to_id[merger]
            v = self.user_to_id[author]
            self.graph_reviews[u][v] += 1
        
        print(f"✓ Grafo 1 (Comentários): {self._count_edges(self.graph_comments)} arestas")
        print(f"✓ Grafo 2 (Fechamentos): {self._count_edges(self.graph_closures)} arestas")
        print(f"✓ Grafo 3 (Reviews): {self._count_edges(self.graph_reviews)} arestas")
    
    def build_integrated_graph(self, weights: Dict[str, float] = None):
        """
        Constrói o grafo integrado com pesos ponderados
        
        Args:
            weights: Dicionário com os pesos para cada tipo de interação
        """
        if weights is None:
            weights = {
                'issue_comment': 2.0,
                'pr_comment': 2.0,
                'issue_opened': 3.0,
                'review': 4.0,
                'approval': 4.0,
                'merge': 5.0
            }
        
        print("\n=== Construindo Grafo Integrado ===")
        print(f"Pesos configurados: {weights}")
        
        # Comentários em issues (peso 2)
        for commenter, author in self.data['interactions']['issue_comments']:
            u = self.user_to_id[commenter]
            v = self.user_to_id[author]
            self.graph_integrated[u][v] += weights['issue_comment']
        
        # Comentários em PRs (peso 2)
        for commenter, author in self.data['interactions']['pr_comments']:
            u = self.user_to_id[commenter]
            v = self.user_to_id[author]
            self.graph_integrated[u][v] += weights['pr_comment']
        
        # Issues comentadas (peso 3 - autor da issue recebe interação)
        for commenter, author in self.data['interactions']['issue_comments']:
            u = self.user_to_id[author]
            v = self.user_to_id[commenter]
            self.graph_integrated[u][v] += weights['issue_opened']
        
        # Reviews (peso 4)
        for reviewer, author in self.data['interactions']['pr_reviews']:
            u = self.user_to_id[reviewer]
            v = self.user_to_id[author]
            self.graph_integrated[u][v] += weights['review']
        
        # Approvals (peso 4)
        for approver, author in self.data['interactions']['pr_approvals']:
            u = self.user_to_id[approver]
            v = self.user_to_id[author]
            self.graph_integrated[u][v] += weights['approval']
        
        # Merges (peso 5)
        for merger, author in self.data['interactions']['pr_merges']:
            u = self.user_to_id[merger]
            v = self.user_to_id[author]
            self.graph_integrated[u][v] += weights['merge']
        
        print(f"✓ Grafo Integrado: {self._count_edges(self.graph_integrated)} arestas")
    
    def _count_edges(self, graph: Dict) -> int:
        """Conta o número de arestas em um grafo"""
        count = 0
        for u in graph:
            count += len(graph[u])
        return count
    
    def export_to_gexf(self, output_dir: str = "data/processed"):
        """
        Exporta os grafos para formato GEXF (compatível com GEPHI)
        
        Args:
            output_dir: Diretório para salvar os arquivos
        """
        os.makedirs(output_dir, exist_ok=True)
        
        repo_name = self.data['repository'].replace('/', '_')
        
        # Exportar grafo de comentários
        self._export_graph_gexf(
            self.graph_comments,
            f"{output_dir}/{repo_name}_comments.gexf",
            "Comentários em Issues e PRs"
        )
        
        # Exportar grafo de fechamentos
        self._export_graph_gexf(
            self.graph_closures,
            f"{output_dir}/{repo_name}_closures.gexf",
            "Fechamentos de Issues"
        )
        
        # Exportar grafo de reviews
        self._export_graph_gexf(
            self.graph_reviews,
            f"{output_dir}/{repo_name}_reviews.gexf",
            "Reviews/Approvals/Merges"
        )
        
        # Exportar grafo integrado
        self._export_graph_gexf(
            self.graph_integrated,
            f"{output_dir}/{repo_name}_integrated.gexf",
            "Grafo Integrado Ponderado"
        )
        
        print(f"\n✓ Grafos exportados para: {output_dir}/")
    
    def _export_graph_gexf(self, graph: Dict, filename: str, description: str):
        """Exporta um grafo individual para formato GEXF"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">\n')
            f.write(f'  <meta lastmodifieddate="{self.data["collection_date"]}">\n')
            f.write(f'    <creator>GitHub Data Collector</creator>\n')
            f.write(f'    <description>{description}</description>\n')
            f.write('  </meta>\n')
            f.write('  <graph mode="static" defaultedgetype="directed">\n')
            
            # Nós
            f.write('    <nodes>\n')
            for user_id, username in self.id_to_user.items():
                f.write(f'      <node id="{user_id}" label="{username}"/>\n')
            f.write('    </nodes>\n')
            
            # Arestas
            f.write('    <edges>\n')
            edge_id = 0
            for u in graph:
                for v in graph[u]:
                    weight = graph[u][v]
                    f.write(f'      <edge id="{edge_id}" source="{u}" target="{v}" weight="{weight}"/>\n')
                    edge_id += 1
            f.write('    </edges>\n')
            
            f.write('  </graph>\n')
            f.write('</gexf>\n')
        
        print(f"  Exportado: {filename}")
    
    def export_to_csv(self, output_dir: str = "data/processed"):
        """
        Exporta os grafos para formato CSV (alternativa ao GEXF)
        
        Args:
            output_dir: Diretório para salvar os arquivos
        """
        os.makedirs(output_dir, exist_ok=True)
        
        repo_name = self.data['repository'].replace('/', '_')
        
        graphs = [
            (self.graph_comments, "comments"),
            (self.graph_closures, "closures"),
            (self.graph_reviews, "reviews"),
            (self.graph_integrated, "integrated")
        ]
        
        for graph, name in graphs:
            filename = f"{output_dir}/{repo_name}_{name}.csv"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Source,Target,Weight\n")
                for u in graph:
                    for v in graph[u]:
                        source = self.id_to_user[u]
                        target = self.id_to_user[v]
                        weight = graph[u][v]
                        f.write(f"{source},{target},{weight}\n")
            
            print(f"  Exportado: {filename}")
    
    def get_graph_statistics(self):
        """Retorna estatísticas sobre os grafos construídos"""
        
        stats = {
            'total_nodes': len(self.users),
            'graph_comments': {
                'edges': self._count_edges(self.graph_comments),
                'max_weight': self._get_max_weight(self.graph_comments)
            },
            'graph_closures': {
                'edges': self._count_edges(self.graph_closures),
                'max_weight': self._get_max_weight(self.graph_closures)
            },
            'graph_reviews': {
                'edges': self._count_edges(self.graph_reviews),
                'max_weight': self._get_max_weight(self.graph_reviews)
            },
            'graph_integrated': {
                'edges': self._count_edges(self.graph_integrated),
                'max_weight': self._get_max_weight(self.graph_integrated)
            }
        }
        
        return stats
    
    def _get_max_weight(self, graph: Dict) -> float:
        """Retorna o peso máximo de uma aresta no grafo"""
        max_w = 0
        for u in graph:
            for v in graph[u]:
                max_w = max(max_w, graph[u][v])
        return max_w


def main():
    """Função principal para construir os grafos"""
    
    # CONFIGURE AQUI O ARQUIVO DE DADOS
    DATA_FILE = "data/raw/facebook_react_data.json"  # Ajuste conforme necessário
    
    print("="*60)
    print("Graph Builder - Teoria de Grafos")
    print("="*60)
    
    if not os.path.exists(DATA_FILE):
        print(f"ERRO: Arquivo {DATA_FILE} não encontrado!")
        print("Execute primeiro o github_data_collector.py")
        return
    
    # Construir grafos
    builder = GraphBuilder(DATA_FILE)
    builder.build_separate_graphs()
    builder.build_integrated_graph()
    
    # Exportar para GEPHI
    builder.export_to_gexf()
    builder.export_to_csv()
    
    # Mostrar estatísticas
    stats = builder.get_graph_statistics()
    print("\n=== ESTATÍSTICAS DOS GRAFOS ===")
    print(f"Total de nós: {stats['total_nodes']}")
    print(f"\nGrafo 1 (Comentários):")
    print(f"  Arestas: {stats['graph_comments']['edges']}")
    print(f"  Peso máximo: {stats['graph_comments']['max_weight']}")
    print(f"\nGrafo 2 (Fechamentos):")
    print(f"  Arestas: {stats['graph_closures']['edges']}")
    print(f"  Peso máximo: {stats['graph_closures']['max_weight']}")
    print(f"\nGrafo 3 (Reviews):")
    print(f"  Arestas: {stats['graph_reviews']['edges']}")
    print(f"  Peso máximo: {stats['graph_reviews']['max_weight']}")
    print(f"\nGrafo Integrado:")
    print(f"  Arestas: {stats['graph_integrated']['edges']}")
    print(f"  Peso máximo: {stats['graph_integrated']['max_weight']}")
    
    print("\n✓ Grafos construídos e exportados com sucesso!")
    print("Você pode visualizar os arquivos .gexf no GEPHI")
    print("Próximo passo: Implementar a Etapa 2 (estruturas de grafos)")


if __name__ == "__main__":
    main()

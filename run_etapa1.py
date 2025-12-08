"""
Script principal para executar a Etapa 1 completa
Trabalho Prático - Teoria de Grafos e Computabilidade
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_mining.github_data_collector import GitHubDataCollector
from data_mining.graph_builder import GraphBuilder


def print_banner():
    """Imprime o banner do programa"""
    print("="*70)
    print(" "*10 + "TRABALHO PRÁTICO - TEORIA DE GRAFOS")
    print(" "*15 + "ETAPA 1: Coleta e Modelagem")
    print("="*70)


def load_config():
    """Carrega configurações do arquivo config.py"""
    try:
        import config
        return config
    except ImportError:
        print("\n⚠️  ERRO: Arquivo config.py não encontrado!")
        print("\nPor favor:")
        print(" Crie config.py e preencha suas configurações")
        sys.exit(1)


def validate_config(config):
    """Valida as configurações"""
    if not hasattr(config, 'REPO_OWNER') or not config.REPO_OWNER:
        print("⚠️  ERRO: REPO_OWNER não configurado em config.py")
        sys.exit(1)
    
    if not hasattr(config, 'REPO_NAME') or not config.REPO_NAME:
        print("⚠️  ERRO: REPO_NAME não configurado em config.py")
        sys.exit(1)
    
    if not hasattr(config, 'GITHUB_TOKEN') or not config.GITHUB_TOKEN:
        print("\n⚠️  AVISO: Token do GitHub não configurado")
        print("Você terá limite de 60 requisições por hora")
        print("Recomendamos criar um token em: https://github.com/settings/tokens")
        
        resposta = input("\nContinuar mesmo assim? (s/n): ")
        if resposta.lower() != 's':
            sys.exit(0)


def collect_data(config):
    """Executa a coleta de dados do GitHub"""
    print("\n" + "="*70)
    print("FASE 1: COLETA DE DADOS DO GITHUB")
    print("="*70)
    
    collector = GitHubDataCollector(
        repo_owner=config.REPO_OWNER,
        repo_name=config.REPO_NAME,
        token=config.GITHUB_TOKEN
    )
    
    print(f"\nRepositório: {config.REPO_OWNER}/{config.REPO_NAME}")
    print(f"Limite de issues: {config.MAX_ISSUES}")
    print(f"Limite de PRs: {config.MAX_PULL_REQUESTS}")
    
    # Coletar dados
    collector.collect_issues_data(max_issues=config.MAX_ISSUES)
    collector.collect_pull_requests_data(max_prs=config.MAX_PULL_REQUESTS)
    
    # Salvar dados
    data_file = collector.save_data(output_dir=config.DATA_DIR)
    
    # Estatísticas
    stats = collector.get_statistics()
    print("\n" + "-"*70)
    print("ESTATÍSTICAS DA COLETA:")
    print("-"*70)
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    return data_file


def build_graphs(config, data_file):
    """Constrói os grafos a partir dos dados coletados"""
    print("\n" + "="*70)
    print("FASE 2: CONSTRUÇÃO DOS GRAFOS")
    print("="*70)
    
    builder = GraphBuilder(data_file)
    
    # Construir grafos separados
    print("\n1. Construindo grafos separados...")
    builder.build_separate_graphs()
    
    # Construir grafo integrado
    print("\n2. Construindo grafo integrado...")
    builder.build_integrated_graph(weights=config.WEIGHTS)
    
    # Exportar para GEPHI
    print("\n3. Exportando para GEPHI...")
    builder.export_to_gexf(output_dir=config.PROCESSED_DIR)
    
    # Exportar para CSV (alternativa)
    print("\n4. Exportando para CSV...")
    builder.export_to_csv(output_dir=config.PROCESSED_DIR)
    
    # Estatísticas dos grafos
    stats = builder.get_graph_statistics()
    print("\n" + "-"*70)
    print("ESTATÍSTICAS DOS GRAFOS:")
    print("-"*70)
    print(f"  Total de nós (usuários): {stats['total_nodes']}")
    print(f"\n  Grafo 1 - Comentários:")
    print(f"    Arestas: {stats['graph_comments']['edges']}")
    print(f"    Peso máximo: {stats['graph_comments']['max_weight']}")
    print(f"\n  Grafo 2 - Fechamentos:")
    print(f"    Arestas: {stats['graph_closures']['edges']}")
    print(f"    Peso máximo: {stats['graph_closures']['max_weight']}")
    print(f"\n  Grafo 3 - Reviews/Approvals/Merges:")
    print(f"    Arestas: {stats['graph_reviews']['edges']}")
    print(f"    Peso máximo: {stats['graph_reviews']['max_weight']}")
    print(f"\n  Grafo Integrado:")
    print(f"    Arestas: {stats['graph_integrated']['edges']}")
    print(f"    Peso máximo: {stats['graph_integrated']['max_weight']}")


def main():
    """Função principal"""
    print_banner()
    
    # Carregar configurações
    config = load_config()
    validate_config(config)
    
    # Executar coleta
    try:
        data_file = collect_data(config)
    except Exception as e:
        print(f"\n❌ ERRO na coleta de dados: {e}")
        sys.exit(1)
    
    # Construir grafos
    try:
        build_graphs(config, data_file)
    except Exception as e:
        print(f"\n❌ ERRO na construção dos grafos: {e}")
        sys.exit(1)
    
    # Finalização
    print("\n" + "="*70)
    print("✅ ETAPA 1 CONCLUÍDA COM SUCESSO!")
    print("="*70)
    print("\nPróximos passos:")
    print("Visualize os grafos no GEPHI usando os arquivos .gexf")
    print(f"Localização: {config.PROCESSED_DIR}/")
    print("Analise os dados em formato CSV se preferir")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

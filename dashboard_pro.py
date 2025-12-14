import json
import os
import glob
import webbrowser
from collections import defaultdict, Counter
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÕES E ESTILOS
# ==============================================================================
CONFIG = {
    "SEARCH_PATH": "data/raw/*.json",
    "OUTPUT_FILE": "dashboard_pro.html",
    "MAX_GRAPH_NODES": 100,  # Limite para não travar o navegador
    "WEIGHTS": {
        'issue_comments': 1,
        'pr_comments': 2,
        'pr_reviews': 5,
        'pr_approvals': 6,
        'pr_merges': 10,
        'issue_closures': 3
    }
}

class ProfessionalDashboard:
    def __init__(self):
        self.data = self._load_latest_data()
        self.stats = self.data.get('statistics', {})
        self.interactions = self.data.get('interactions', {})
        self.nodes = {}
        self.edges = []
        
        print("⚙️  Processando métricas de grafos...")
        self._process_graph_data()

    def _load_latest_data(self):
        """Encontra automaticamente o arquivo JSON mais recente."""
        files = glob.glob(CONFIG["SEARCH_PATH"])
        if not files:
            print(f"❌ ERRO CRÍTICO: Nenhum arquivo encontrado em '{CONFIG['SEARCH_PATH']}'")
            print("   Execute 'run_etapa1.py' primeiro para coletar os dados.")
            exit(1)
        
        latest_file = max(files, key=os.path.getctime)
        print(f"✅ Arquivo de dados detectado: {latest_file}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _process_graph_data(self):
        """Processa nós, arestas e métricas de centralidade."""
        degree_map = defaultdict(int)
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        interaction_types = defaultdict(int)
        
        # 1. Construir arestas e calcular graus
        temp_edges = defaultdict(int)
        
        for int_type, int_list in self.interactions.items():
            weight = CONFIG["WEIGHTS"].get(int_type, 1)
            interaction_types[int_type] = len(int_list)
            
            for source, target in int_list:
                if not source or not target or source == 'repository' or target == 'repository':
                    continue
                
                # Grafos direcionados
                key = (source, target)
                temp_edges[key] += weight
                
                degree_map[source] += 1
                degree_map[target] += 1
                out_degree[source] += 1
                in_degree[target] += 1

        # 2. Filtrar Top Nodes (para performance do navegador)
        top_users = dict(sorted(degree_map.items(), key=lambda x: x[1], reverse=True)[:CONFIG["MAX_GRAPH_NODES"]])
        allowed_users = set(top_users.keys())

        # 3. Preparar Nós para Vis.js
        self.js_nodes = []
        for user, degree in top_users.items():
            # Tenta identificar "papel" baseado no comportamento
            role = "Colaborador"
            if out_degree[user] > in_degree[user] * 2: role = "Ativo (Gera demanda)"
            if in_degree[user] > out_degree[user] * 2: role = "Referência (Resolve demanda)"
            
            self.js_nodes.append({
                'id': user,
                'label': user,
                'value': degree, # Tamanho do nó
                'title': f"<b>{user}</b><br>Grau Total: {degree}<br>Role: {role}",
                'group': 'hub' if degree > 20 else 'contributor'
            })

        # 4. Preparar Arestas para Vis.js
        self.js_edges = []
        for (src, tgt), w in temp_edges.items():
            if src in allowed_users and tgt in allowed_users:
                self.js_edges.append({
                    'from': src,
                    'to': tgt,
                    'value': w,
                    'title': f"Peso: {w}"
                })

        # 5. Dados para Gráficos
        self.chart_data = {
            'types_labels': list(interaction_types.keys()),
            'types_values': list(interaction_types.values()),
            'top_active_labels': list(out_degree.keys())[:10],
            'top_active_values': list(out_degree.values())[:10],
            'top_popular_labels': list(in_degree.keys())[:10],
            'top_popular_values': list(in_degree.values())[:10]
        }

    def generate_html(self):
        """Gera o código HTML/JS completo."""
        
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics de Grafo GitHub - {self.data.get('repository')}</title>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --primary: #6366f1;
            --accent: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            padding-bottom: 50px;
        }}

        /* Header */
        header {{
            background: linear-gradient(135deg, var(--primary), var(--accent));
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }}
        
        h1 {{ font-weight: 800; letter-spacing: -1px; margin-bottom: 10px; }}
        .badge {{ background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; }}

        /* Layout Grid */
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 0 20px;
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 25px;
        }}

        /* Cards */
        .card {{
            background-color: var(--card-bg);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.05);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }}

        .card h2 {{ font-size: 1.1rem; color: var(--text-muted); margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }}
        .metric-big {{ font-size: 2.5rem; font-weight: 700; color: var(--primary); }}

        /* Sidebar Controls */
        .sidebar {{ grid-column: 1; }}
        .main-content {{ grid-column: 2; }}

        .control-group {{ margin-bottom: 20px; }}
        .control-group label {{ display: block; margin-bottom: 8px; font-size: 0.9rem; }}
        input[type="range"] {{ width: 100%; accent-color: var(--primary); }}

        /* Network Graph */
        #network {{
            width: 100%;
            height: 600px;
            background: #111;
            border-radius: 12px;
            border: 1px solid #333;
        }}

        /* Charts */
        .charts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }}

        footer {{ text-align: center; color: var(--text-muted); margin-top: 50px; font-size: 0.8rem; }}

        @media (max-width: 1000px) {{
            .container {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

    <header>
        <h1>Dashboard de Análise de Grafos</h1>
        <p>Repositório: <strong>{self.data.get('repository')}</strong> <span class="badge">DADOS REAIS</span></p>
    </header>

    <div class="container">
        <aside class="sidebar">
            <div class="card">
                <h2>Resumo Global</h2>
                <div style="margin-bottom: 15px;">
                    <div class="metric-big">{self.stats.get('total_users')}</div>
                    <div style="color: var(--text-muted)">Nós (Usuários)</div>
                </div>
                <div>
                    <div class="metric-big">{sum(self.chart_data['types_values'])}</div>
                    <div style="color: var(--text-muted)">Arestas (Interações)</div>
                </div>
            </div>

            <div class="card">
                <h2>🔧 Filtros de Visualização</h2>
                <div class="control-group">
                    <label>Física do Grafo (Estabilidade)</label>
                    <input type="checkbox" id="physicsToggle" checked onchange="togglePhysics()"> Ativar Simulação
                </div>
                <div class="control-group">
                    <label>Filtrar por Peso Mínimo: <span id="weightVal">0</span></label>
                    <input type="range" id="weightFilter" min="0" max="10" value="0" step="1" oninput="filterNetwork()">
                </div>
                <p style="font-size: 0.8rem; color: #666;">Use os filtros para limpar o grafo e focar nas conexões mais fortes.</p>
            </div>

            <div class="card">
                <h2>📊 Distribuição</h2>
                <canvas id="typeChart"></canvas>
            </div>
        </aside>

        <main class="main-content">
            <div class="card">
                <h2>🕸️ Rede de Colaboração (Top {CONFIG['MAX_GRAPH_NODES']} Hubs)</h2>
                <div id="network"></div>
            </div>

            <div class="charts-grid">
                <div class="card">
                    <h2>🏆 Top 10 Mais Ativos (Out-Degree)</h2>
                    <canvas id="activeChart"></canvas>
                </div>
                <div class="card">
                    <h2>⭐ Top 10 Mais Populares (In-Degree)</h2>
                    <canvas id="popularChart"></canvas>
                </div>
            </div>
        </main>
    </div>

    <footer>
        Gerado automaticamente por Python Graph Analysis Tool • {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </footer>

    <script>
        // --- DADOS INJETADOS PELO PYTHON ---
        const rawNodes = {json.dumps(self.js_nodes)};
        const rawEdges = {json.dumps(self.js_edges)};
        const chartData = {json.dumps(self.chart_data)};

        // --- CONFIGURAÇÃO DO GRAFO (VIS.JS) ---
        const nodes = new vis.DataSet(rawNodes);
        const edges = new vis.DataSet(rawEdges);
        const container = document.getElementById('network');
        
        const data = {{ nodes: nodes, edges: edges }};
        const options = {{
            nodes: {{
                shape: 'dot',
                font: {{ color: '#fff', size: 14 }},
                borderWidth: 2,
                shadow: true
            }},
            edges: {{
                width: 1,
                color: {{ color: '#555', highlight: '#8b5cf6', opacity: 0.6 }},
                arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }},
                smooth: {{ type: 'continuous' }}
            }},
            physics: {{
                enabled: true,
                forceAtlas2Based: {{
                    gravitationalConstant: -26,
                    centralGravity: 0.005,
                    springLength: 230,
                    springConstant: 0.18
                }},
                maxVelocity: 146,
                solver: 'forceAtlas2Based',
                timestep: 0.35,
                stabilization: {{ iterations: 150 }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                hideEdgesOnDrag: true
            }}
        }};

        const network = new vis.Network(container, data, options);

        // Funções de Interatividade
        function togglePhysics() {{
            const status = document.getElementById('physicsToggle').checked;
            network.setOptions({{ physics: {{ enabled: status }} }});
        }}

        function filterNetwork() {{
            const minWeight = parseInt(document.getElementById('weightFilter').value);
            document.getElementById('weightVal').innerText = minWeight;
            
            const newEdges = rawEdges.filter(e => e.value >= minWeight);
            edges.clear();
            edges.add(newEdges);
        }}

        // Evento de Clique no Nó
        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                const nodeId = params.nodes[0];
                const node = nodes.get(nodeId);
                console.log('Nó selecionado:', node);
                // Você poderia adicionar lógica aqui para mostrar detalhes laterais
            }}
        }});

        // --- CHART.JS CONFIG ---
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.borderColor = '#334155';

        // 1. Gráfico de Pizza (Tipos)
        new Chart(document.getElementById('typeChart'), {{
            type: 'doughnut',
            data: {{
                labels: chartData.types_labels,
                datasets: [{{
                    data: chartData.types_values,
                    backgroundColor: ['#6366f1', '#8b5cf6', '#ec4899', '#14b8a6', '#f59e0b'],
                    borderWidth: 0
                }}]
            }},
            options: {{ plugins: {{ legend: {{ display: false }} }} }}
        }});

        // 2. Gráfico Barras (Ativos)
        new Chart(document.getElementById('activeChart'), {{
            type: 'bar',
            data: {{
                labels: chartData.top_active_labels,
                datasets: [{{
                    label: 'Interações',
                    data: chartData.top_active_values,
                    backgroundColor: '#6366f1',
                    borderRadius: 5
                }}]
            }},
            options: {{ indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
        }});

        // 3. Gráfico Barras (Populares)
        new Chart(document.getElementById('popularChart'), {{
            type: 'bar',
            data: {{
                labels: chartData.top_popular_labels,
                datasets: [{{
                    label: 'Recebidas',
                    data: chartData.top_popular_values,
                    backgroundColor: '#14b8a6',
                    borderRadius: 5
                }}]
            }},
            options: {{ indexAxis: 'y', plugins: {{ legend: {{ display: false }} }} }}
        }});

    </script>
</body>
</html>
        """
        
        with open(CONFIG["OUTPUT_FILE"], 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\nSUCESSO! Dashboard gerado em: {os.path.abspath(CONFIG['OUTPUT_FILE'])}")
        webbrowser.open(f"file://{os.path.abspath(CONFIG['OUTPUT_FILE'])}")

if __name__ == "__main__":
    print("="*50)
    print("      DASHBOARD GENERATOR PRO - TEORIA DOS GRAFOS")
    print("="*50)
    try:
        app = ProfessionalDashboard()
        app.generate_html()
    except Exception as e:
        print(f"\nErro durante a execução: {e}")

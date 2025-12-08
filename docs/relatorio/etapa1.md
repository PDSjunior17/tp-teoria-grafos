# RELATÓRIO TÉCNICO - ETAPA 1
# MODELAGEM E PLANEJAMENTO DA SOLUÇÃO

## 1. Descrição do Problema

O presente trabalho tem como objetivo o desenvolvimento de uma ferramenta computacional fundamentada na Teoria dos Grafos para a análise de interações sociais e técnicas em projetos de desenvolvimento de software de código aberto (Open Source).

Repositórios de software, como os hospedados no GitHub, são ecossistemas complexos onde a colaboração ocorre através de diversas camadas de interação: report de bugs (issues), propostas de código (pull requests), revisões de código (code reviews) e discussões gerais. Compreender a dinâmica dessas interações é essencial para identificar padrões de liderança, núcleos de colaboração e a saúde geral da comunidade.

O problema central consiste em extrair dados não estruturados ou semi-estruturados da API do GitHub, transformá-los em modelos matemáticos formais (grafos) e implementar algoritmos para extração de métricas de centralidade e comunidade, permitindo uma análise quantitativa da rede de colaboradores.

## 2. Justificativa da Escolha do Repositório

Para a realização deste estudo, foi selecionado o repositório **vercel/next.js**.

**Dados do Repositório:**
* **Proprietário:** Vercel
* **Projeto:** Next.js
* **URL:** https://github.com/vercel/next.js

**Critérios de Escolha:**
1.  **Relevância e Popularidade:** O repositório possui mais de 120.000 estrelas, superando amplamente o requisito mínimo de 5.000 estrelas estipulado na especificação do trabalho.
2.  **Alta Densidade de Interações:** Diferentemente de repositórios focados apenas em arquivamento de código, o Next.js é um framework web ativo com um alto volume de discussões diárias, revisões de código e merges, o que favorece a criação de grafos conexos e não-triviais.
3.  **Estrutura de Comunidade Mista:** O projeto envolve tanto desenvolvedores corporativos (funcionários da Vercel) quanto contribuidores da comunidade global, permitindo análises interessantes sobre centralidade e hierarquia.

## 3. Estratégia de Coleta de Dados

A coleta de dados foi implementada utilizando a linguagem **Python** e a biblioteca `requests` para consumo da API REST do GitHub (v3).

**Mecanismo de Coleta:**
O script de mineração (`github_data_collector.py`) realiza requisições paginadas aos endpoints de *Issues* e *Pull Requests*. Para contornar as limitações de taxa da API (Rate Limiting), utiliza-se um Token de Autenticação pessoal, permitindo até 5.000 requisições por hora.

**Dados Extraídos:**
Foram coletadas as seguintes entidades e suas relações:
* **Usuários:** Identificados pelo login único do GitHub (nós do grafo).
* **Issues:** Autor da abertura, autores de comentários e usuário responsável pelo fechamento.
* **Pull Requests (PRs):** Autor da proposta, autores de comentários, revisores de código (reviewers), usuários que aprovaram as mudanças e o usuário responsável pelo merge final.

**Tratamento de Dados:**
* Amostragem definida para as últimas 800 issues e 800 pull requests para garantir um recorte temporal significativo.
* Tratamento de exceções para usuários deletados (ghost users).
* Busca individual por dados de merge quando não disponíveis na listagem padrão.

## 4. Proposta de Modelagem dos Grafos

A modelagem segue a definição de **Grafos Direcionados (Digrafos)**, onde $G = (V, E)$.
* $V$ (Vértices): Conjunto de usuários do GitHub.
* $E$ (Arestas): Conjunto de pares ordenados $(u, v)$ representando que o usuário $u$ interagiu com um artefato criado ou gerenciado pelo usuário $v$.

Conforme especificado, a modelagem foi dividida em duas fases:

### 4.1. Grafos Separados (Sem Pesos)

Foram modelados três grafos distintos para analisar interações isoladas:

1.  **Grafo de Comentários ($G_c$):**
    * Aresta $(u, v)$ existe se o usuário $u$ comentou em uma issue ou pull request criada pelo usuário $v$.
    * Representa a camada de discussão e suporte.

2.  **Grafo de Fechamentos ($G_f$):**
    * Aresta $(u, v)$ existe se o usuário $u$ fechou uma issue criada pelo usuário $v$.
    * Representa a relação de moderação e resolução de problemas.

3.  **Grafo de Revisões e Merges ($G_r$):**
    * Aresta $(u, v)$ existe se o usuário $u$ realizou um review, aprovou ou realizou o merge de um pull request do usuário $v$.
    * Representa a colaboração técnica direta e controle de qualidade.

### 4.2. Grafo Integrado Ponderado ($G_i$)

Este grafo unifica todas as interações anteriores em uma única estrutura ponderada. As arestas múltiplas entre dois usuários são colapsadas em uma única aresta com peso acumulado $W(u, v)$.

**Tabela de Pesos:**

| Tipo de Interação | Peso | Justificativa |
| :--- | :---: | :--- |
| Comentário em Issue/PR | 2.0 | Interação básica de comunicação. |
| Abertura de Issue Comentada | 3.0 | Valorização da iniciativa de reportar problemas que geram discussão. |
| Review / Aprovação de PR | 4.0 | Contribuição técnica que exige análise de código. |
| Merge de Pull Request | 5.0 | Ação de maior autoridade e impacto no código fonte. |

A fórmula para o peso da aresta entre $u$ e $v$ é dada por:
$$W(u,v) = \sum (n_{com} \times 2) + (n_{iss} \times 3) + (n_{rev} \times 4) + (n_{merge} \times 5)$$

## 5. Plano de Desenvolvimento da Solução

O desenvolvimento está estruturado nas seguintes fases, alinhadas com as Etapas do trabalho prático:

**Fase 1: Coleta e Modelagem (Concluída)**
* Implementação do script de mineração de dados (`github_data_collector.py`).
* Implementação do construtor de grafos (`graph_builder.py`).
* Exportação dos dados para formato GEXF (Gephi) e CSV para validação visual preliminar.

**Fase 2: Implementação da Estrutura de Grafos (Em Progresso)**
* Criação da classe abstrata `AbstractGraph` definindo a API padrão.
* Implementação das estruturas de dados concretas:
    * `AdjacencyMatrixGraph`: Representação densa usando matriz $N \times N$.
    * `AdjacencyListGraph`: Representação esparsa usando listas de adjacência (foco em performance para o grafo do Next.js).
* Implementação dos algoritmos fundamentais: verificação de adjacência, cálculo de graus de entrada/saída e sucessores/predecessores.

**Fase 3: Algoritmos Avançados e Métricas**
* Implementação de algoritmos de busca (BFS/DFS) para verificação de conectividade (`isConnected`).
* Cálculo de métricas de centralidade (Degree, Closeness, Betweenness).
* Detecção de comunidades.

**Fase 4: Análise e Relatório Final**
* Processamento do grafo integrado utilizando a ferramenta desenvolvida.
* Visualização final no software Gephi.
* Redação do relatório final em LaTeX contendo a análise dos dados obtidos.

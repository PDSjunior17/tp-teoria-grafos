"""
Módulo para coleta de dados de repositórios GitHub
Trabalho Prático - Teoria de Grafos e Computabilidade
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple
import os


class GitHubDataCollector:
    """Classe para coletar dados de interações de um repositório GitHub"""
    
    def __init__(self, repo_owner: str, repo_name: str, token: str = None):
        """
        Inicializa o coletor de dados
        
        Args:
            repo_owner: Proprietário do repositório
            repo_name: Nome do repositório 
            token: Token de autenticação do GitHub 
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        if token:
            self.headers["Authorization"] = f"token {token}"
        
        # Estruturas para armazenar dados
        self.users = set()
        self.issue_comments = []  # (comentador, autor_issue)
        self.issue_closures = []  # (quem_fechou, autor_issue)
        self.pr_reviews = []      # (revisor, autor_pr)
        self.pr_approvals = []    # (aprovador, autor_pr)
        self.pr_merges = []       # (quem_fez_merge, autor_pr)
        self.pr_comments = []     # (comentador, autor_pr)
    
    def _make_request(self, endpoint: str, params: Dict = None, limit: int = None) -> List[Dict]:
        """
        Faz requisição à API do GitHub com tratamento de paginação e limite
        
        Args:
            endpoint: Endpoint da API
            params: Parâmetros da requisição
            limit: Número máximo de itens a coletar antes de parar
            
        Returns:
            Lista com todos os resultados paginados
        """
        if params is None:
            params = {}
        
        params['per_page'] = 100  # Máximo permitido
        
        url = f"{self.base_url}{endpoint}"
        all_results = []
        
        while url:
            # VERIFICAÇÃO DE PARADA: Se já temos o suficiente, para o loop
            if limit and len(all_results) >= limit:
                break

            print(f"Requisitando: {url}")
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 403:
                    print("Rate limit atingido. Aguardando...")
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    sleep_time = max(reset_time - time.time(), 0) + 10
                    time.sleep(sleep_time)
                    continue
                
                if response.status_code != 200:
                    print(f"Erro {response.status_code}: {response.text}")
                    break
                
                data = response.json()
                if not data: # Lista vazia, acabou
                    break
                    
                all_results.extend(data)
                
                # Verificar se há próxima página
                if 'Link' in response.headers:
                    links = response.headers['Link'].split(',')
                    url = None
                    for link in links:
                        if 'rel="next"' in link:
                            url = link[link.find('<')+1:link.find('>')]
                            params = None  # Já está na URL
                            break
                else:
                    url = None
                
                # Pequeno delay para não sobrecarregar a API
                time.sleep(0.5)
            
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição: {e}")
                break
        
        return all_results
    
    def collect_issues_data(self, max_issues: int = 500):
        """
        Coleta dados de issues (comentários e fechamentos)
        
        Args:
            max_issues: Número máximo de issues para processar
        """
        print("\n=== Coletando Issues ===")
        endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/issues"
        params = {
            'state': 'all',
            'sort': 'created',
            'direction': 'desc'
        }
        
        # Passamos o limit aqui para parar de baixar quando atingir o max
        issues = self._make_request(endpoint, params, limit=max_issues)
        issues = issues[:max_issues]
        
        print(f"Total de issues encontradas: {len(issues)}")
        
        for i, issue in enumerate(issues):
            if 'pull_request' in issue:  # Pular PRs
                continue
            
            # Proteção caso user seja null (ghost user)
            if not issue.get('user'):
                continue

            issue_author = issue['user']['login']
            self.users.add(issue_author)
            issue_number = issue['number']
            
            print(f"Processando issue #{issue_number} ({i+1}/{len(issues)})")
            
            # Coletar comentários
            if issue['comments'] > 0:
                comments_endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/comments"
                comments = self._make_request(comments_endpoint)
                
                for comment in comments:
                    if comment.get('user'):
                        commenter = comment['user']['login']
                        self.users.add(commenter)
                        if commenter != issue_author:
                            self.issue_comments.append((commenter, issue_author))
            
            # Verificar fechamento
            if issue['state'] == 'closed' and issue['closed_by']:
                closer = issue['closed_by']['login']
                self.users.add(closer)
                if closer != issue_author:
                    self.issue_closures.append((closer, issue_author))
    
    def collect_pull_requests_data(self, max_prs: int = 500):
        """
        Coleta dados de pull requests (comentários, reviews, approvals, merges)
        Args:
            max_prs: Número máximo de PRs para processar
        """
        print("\n=== Coletando Pull Requests ===")
        endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/pulls"
        params = {
            'state': 'all',
            'sort': 'created',
            'direction': 'desc'
        }
        
        # Passamos o limit aqui também
        prs = self._make_request(endpoint, params, limit=max_prs)
        prs = prs[:max_prs]
        
        print(f"Total de PRs encontrados: {len(prs)}")
        
        for i, pr in enumerate(prs):
            # Garante que temos o login do autor
            if not pr.get('user'):
                continue

            pr_author = pr['user']['login']
            self.users.add(pr_author)
            pr_number = pr['number']
            
            print(f"Processando PR #{pr_number} ({i+1}/{len(prs)})")
            
            # 1. Coletar comentários
            # Usamos .get() para evitar o erro KeyError: 'comments'
            if pr.get('comments', 0) > 0:
                comments_endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/issues/{pr_number}/comments"
                comments = self._make_request(comments_endpoint)
                
                for comment in comments:
                    if comment.get('user'):
                        commenter = comment['user']['login']
                        self.users.add(commenter)
                        if commenter != pr_author:
                            self.pr_comments.append((commenter, pr_author))
            
            # 2. Coletar reviews
            reviews_endpoint = f"/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}/reviews"
            reviews = self._make_request(reviews_endpoint)
            
            for review in reviews:
                if review.get('user'):
                    reviewer = review['user']['login']
                    self.users.add(reviewer)
                    
                    if reviewer != pr_author:
                        self.pr_reviews.append((reviewer, pr_author))
                        
                        # Verificar aprovação
                        if review['state'] == 'APPROVED':
                            self.pr_approvals.append((reviewer, pr_author))
            
            # 3. Verificar merge
            if pr.get('merged_at'):
                # Tenta pegar quem fez o merge direto do objeto (se existir)
                merger_data = pr.get('merged_by')
                
                # Se não existir no objeto da lista, temos que buscar o PR individualmente
                if not merger_data:
                    try:
                        single_pr_url = f"/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}"
                        # Fazemos uma request única sem usar o _make_request para não pegar paginação
                        resp = requests.get(f"{self.base_url}{single_pr_url}", headers=self.headers)
                        if resp.status_code == 200:
                            single_pr = resp.json()
                            merger_data = single_pr.get('merged_by')
                    except:
                        pass # Se falhar, ignoramos o merge para não parar o script

                if merger_data and merger_data.get('login'):
                    merger = merger_data['login']
                    self.users.add(merger)
                    if merger != pr_author:
                        self.pr_merges.append((merger, pr_author))
    
    def save_data(self, output_dir: str = "data/raw"):
        """
        Salva os dados coletados em arquivos JSON
        
        Args:
            output_dir: Diretório para salvar os arquivos
        """
        os.makedirs(output_dir, exist_ok=True)
        
        data = {
            'repository': f"{self.repo_owner}/{self.repo_name}",
            'collection_date': datetime.now().isoformat(),
            'users': list(self.users),
            'interactions': {
                'issue_comments': self.issue_comments,
                'issue_closures': self.issue_closures,
                'pr_comments': self.pr_comments,
                'pr_reviews': self.pr_reviews,
                'pr_approvals': self.pr_approvals,
                'pr_merges': self.pr_merges
            },
            'statistics': {
                'total_users': len(self.users),
                'total_issue_comments': len(self.issue_comments),
                'total_issue_closures': len(self.issue_closures),
                'total_pr_comments': len(self.pr_comments),
                'total_pr_reviews': len(self.pr_reviews),
                'total_pr_approvals': len(self.pr_approvals),
                'total_pr_merges': len(self.pr_merges)
            }
        }
        
        filename = f"{output_dir}/{self.repo_owner}_{self.repo_name}_data.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== Dados salvos em: {filename} ===")
        print(f"Total de usuários: {len(self.users)}")
        print(f"Total de interações coletadas: {sum([
            len(self.issue_comments),
            len(self.issue_closures),
            len(self.pr_comments),
            len(self.pr_reviews),
            len(self.pr_approvals),
            len(self.pr_merges)
        ])}")
        
        return filename
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas sobre os dados coletados"""
        return {
            'total_users': len(self.users),
            'total_issue_comments': len(self.issue_comments),
            'total_issue_closures': len(self.issue_closures),
            'total_pr_comments': len(self.pr_comments),
            'total_pr_reviews': len(self.pr_reviews),
            'total_pr_approvals': len(self.pr_approvals),
            'total_pr_merges': len(self.pr_merges)
        }


def main():

if __name__ == "__main__":
    main()

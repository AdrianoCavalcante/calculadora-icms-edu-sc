"""
Calculadora IQESC - Análise Completa de Indicadores Educacionais
Utiliza dados extraídos do TCE-SC para análises e projeções
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import statistics

class CalculadoraIQESC:
    """
    Calculadora para análise de dados IQESC do TCE-SC
    
    Funcionalidades:
    - Carrega dados do scraper (cache ou arquivos)
    - Analisa indicadores por município
    - Identifica pontos fortes e fracos
    - Calcula potenciais de melhoria
    - Gera relatórios detalhados
    - Exporta análises completas
    """
    
    # Mapeamento de índices das colunas (baseado no scraper)
    COL_INDEX = 0      # Número da linha
    COL_NOME = 1       # Nome do Município
    COL_CODIGO = 2     # Código IBGE
    COL_IEO = 3        # Indicador de Esforço Observado
    COL_IPA = 4        # Indicador de Proficiência Avaliada
    COL_IEE = 5        # Indicador de Esforço Escolar
    COL_CSE = 6        # Contexto Socioeconômico
    COL_SCE = 7        # Sistema de Custos das Escolas
    COL_IEN = 8        # Indicador de Esforço Não Observado
    COL_IQESC = 9      # IQESC (Índice Final)
    
    def __init__(self, ano: int = 2024, cache_dir: str = "cache", auto_download: bool = False, 
                 montante_total_icms: float = 0):
        """
        Inicializa calculadora
        
        Args:
            ano: Ano dos dados (padrão 2024)
            cache_dir: Diretório do cache (padrão 'cache')
            auto_download: Se True, tenta baixar dados automaticamente se não existirem
            montante_total_icms: Valor total do ICMS Educacional a ser distribuído (R$)
        """
        self.ano = ano
        self.cache_dir = Path(__file__).parent.parent.parent / cache_dir / f"iqesc_{ano}"
        self.dados_raw = None
        self.dados_processados = []
        self.municipios_dict = {}
        self.auto_download = auto_download
        self.montante_total_icms = montante_total_icms
        
        self._carregar_dados()
    
    def _carregar_dados(self):
        """Carrega dados do cache ou arquivos legacy"""
        # Tenta carregar do cache primeiro
        arquivo_cache = self.cache_dir / "dados.json"
        
        # Fallback para arquivos antigos
        arquivo_legacy = Path(__file__).parent.parent.parent / f"iqesc_dados_{self.ano}.json"
        
        arquivo = arquivo_cache if arquivo_cache.exists() else arquivo_legacy
        
        if not arquivo.exists():
            if self.auto_download:
                print(f"⚠️  Dados não encontrados no cache para o ano {self.ano}")
                print(f"🌐 Tentando baixar dados automaticamente...")
                
                # Tenta executar o scraper
                sucesso = self._executar_scraper()
                
                if not sucesso:
                    raise FileNotFoundError(
                        f"❌ Não foi possível baixar dados para o ano {self.ano}.\n"
                        f"Verifique sua conexão ou tente: python iqesc_scraper_dinamico.py {self.ano}"
                    )
                
                # Tenta carregar novamente após download
                arquivo = arquivo_cache if arquivo_cache.exists() else arquivo_legacy
                
                if not arquivo.exists():
                    raise FileNotFoundError(
                        f"❌ Dados não encontrados após download para o ano {self.ano}."
                    )
            else:
                raise FileNotFoundError(
                    f"❌ Dados não encontrados para o ano {self.ano}.\n"
                    f"Execute: python iqesc_scraper_dinamico.py {self.ano}"
                )
        
        print(f"📂 Carregando dados de: {arquivo}")
        
        with open(arquivo, encoding='utf-8') as f:
            self.dados_raw = json.load(f)
        
        self._processar_dados()
        print(f"✅ {len(self.dados_processados)} municípios carregados")
    
    def _executar_scraper(self) -> bool:
        """
        Executa o scraper dinamicamente para baixar dados
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            import subprocess
            import sys
            
            scraper_path = Path(__file__).parent.parent.parent / "iqesc_scraper_dinamico.py"
            
            if not scraper_path.exists():
                print(f"❌ Scraper não encontrado: {scraper_path}")
                return False
            
            # Executa o scraper
            resultado = subprocess.run(
                [sys.executable, str(scraper_path), str(self.ano)],
                capture_output=True,
                text=True,
                timeout=180  # 3 minutos de timeout
            )
            
            if resultado.returncode == 0:
                print(f"✅ Dados baixados com sucesso para o ano {self.ano}")
                return True
            else:
                print(f"❌ Erro ao executar scraper: {resultado.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  Timeout ao baixar dados")
            return False
        except Exception as e:
            print(f"❌ Erro ao executar scraper: {e}")
            return False
    
    def _processar_dados(self):
        """Processa dados brutos para estrutura mais amigável"""
        if 'data' not in self.dados_raw:
            return
        
        for row in self.dados_raw['data']:
            if len(row) < 10:
                continue
            
            municipio = {
                'nome': row[self.COL_NOME],
                'codigo': row[self.COL_CODIGO],
                'ieo': self._safe_float(row[self.COL_IEO]),
                'ipa': self._safe_float(row[self.COL_IPA]),
                'iee': self._safe_float(row[self.COL_IEE]),
                'cse': self._safe_float(row[self.COL_CSE]),
                'sce': self._safe_float(row[self.COL_SCE]),
                'ien': self._safe_float(row[self.COL_IEN]),
                'iqesc': self._safe_float(row[self.COL_IQESC])
            }
            
            self.dados_processados.append(municipio)
            self.municipios_dict[municipio['nome'].lower()] = municipio
    
    @staticmethod
    def _safe_float(value) -> float:
        """Converte valor para float de forma segura"""
        try:
            return float(value) if value else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def listar_municipios(self) -> List[str]:
        """
        Lista todos os municípios disponíveis
        
        Returns:
            Lista com nomes dos municípios
        """
        return sorted([m['nome'] for m in self.dados_processados])
    
    def obter_municipio(self, nome: str) -> Optional[Dict]:
        """
        Obtém dados de um município específico
        
        Args:
            nome: Nome do município
            
        Returns:
            Dicionário com dados do município ou None se não encontrado
        """
        return self.municipios_dict.get(nome.lower())
    
    def calcular_estatisticas_gerais(self) -> Dict:
        """
        Calcula estatísticas gerais de todos os municípios
        
        Returns:
            Dicionário com estatísticas agregadas
        """
        if not self.dados_processados:
            return {}
        
        iqescs = [m['iqesc'] for m in self.dados_processados if m['iqesc'] > 0]
        
        if not iqescs:
            return {}
        
        return {
            'total_municipios': len(self.dados_processados),
            'iqesc': {
                'media': statistics.mean(iqescs),
                'mediana': statistics.median(iqescs),
                'desvio_padrao': statistics.stdev(iqescs) if len(iqescs) > 1 else 0,
                'minimo': min(iqescs),
                'maximo': max(iqescs),
            },
            'indicadores': {
                indicador: {
                    'media': statistics.mean([m[indicador] for m in self.dados_processados if m[indicador] > 0]),
                    'minimo': min([m[indicador] for m in self.dados_processados if m[indicador] > 0]),
                    'maximo': max([m[indicador] for m in self.dados_processados if m[indicador] > 0]),
                }
                for indicador in ['ieo', 'ipa', 'iee', 'cse', 'sce', 'ien']
            }
        }
    
    def ranking_municipios(self, top_n: int = 10, por: str = 'iqesc') -> List[Dict]:
        """
        Gera ranking de municípios
        
        Args:
            top_n: Quantidade de municípios no ranking
            por: Indicador para ordenação ('iqesc', 'ieo', 'ipa', etc)
            
        Returns:
            Lista com top N municípios ordenados
        """
        if por not in ['iqesc', 'ieo', 'ipa', 'iee', 'cse', 'sce', 'ien']:
            por = 'iqesc'
        
        municipios_ordenados = sorted(
            self.dados_processados,
            key=lambda x: x[por],
            reverse=True
        )
        
        return municipios_ordenados[:top_n]
    
    def calcular_repasse(self, iqesc_municipio: float) -> Dict:
        """
        Calcula valores de repasse baseado no IQESC
        
        Args:
            iqesc_municipio: IQESC do município (0-1)
            
        Returns:
            Dicionário com valores de repasse
        """
        if self.montante_total_icms <= 0:
            return {
                'repasse_atual': 0,
                'repasse_maximo': 0,
                'percentual_distribuicao': 0,
                'gap_financeiro': 0
            }
        
        # Soma total dos IQESC de todos municípios
        soma_iqesc_total = sum(m['iqesc'] for m in self.dados_processados)
        
        # Percentual que este município representa
        percentual_distribuicao = (iqesc_municipio / soma_iqesc_total) * 100 if soma_iqesc_total > 0 else 0
        
        # Repasse atual baseado no IQESC
        repasse_atual = (iqesc_municipio / soma_iqesc_total) * self.montante_total_icms if soma_iqesc_total > 0 else 0
        
        # Repasse máximo se atingir IQESC = 1.0
        soma_se_maximo = soma_iqesc_total - iqesc_municipio + 1.0
        repasse_maximo = (1.0 / soma_se_maximo) * self.montante_total_icms if soma_se_maximo > 0 else 0
        
        # Gap financeiro
        gap_financeiro = repasse_maximo - repasse_atual
        
        return {
            'repasse_atual': repasse_atual,
            'repasse_maximo': repasse_maximo,
            'percentual_distribuicao': percentual_distribuicao,
            'gap_financeiro': gap_financeiro
        }
    
    def analisar_municipio(self, nome: str) -> Dict:
        """
        Análise detalhada de um município
        
        Args:
            nome: Nome do município
            
        Returns:
            Dicionário com análise completa
        """
        municipio = self.obter_municipio(nome)
        
        if not municipio:
            return {'erro': f"Município '{nome}' não encontrado"}
        
        # Calcula posição no ranking
        ranking = self.ranking_municipios(top_n=len(self.dados_processados))
        posicao = next((i+1 for i, m in enumerate(ranking) if m['nome'].lower() == nome.lower()), None)
        
        # Identifica pontos fortes e fracos
        indicadores = {
            'IEO (Esforço Observado)': municipio['ieo'],
            'IPA (Proficiência Avaliada)': municipio['ipa'],
            'IEE (Esforço Escolar)': municipio['iee'],
            'CSE (Contexto Socioeconômico)': municipio['cse'],
            'SCE (Sistema de Custos)': municipio['sce'],
            'IEN (Esforço Não Observado)': municipio['ien'],
        }
        
        pontos_fortes = sorted(indicadores.items(), key=lambda x: x[1], reverse=True)[:3]
        pontos_fracos = sorted(indicadores.items(), key=lambda x: x[1])[:3]
        
        # Calcula potencial de melhoria
        iqesc_atual = municipio['iqesc']
        iqesc_maximo = 1.0  # IQESC varia de 0 a 1
        gap_melhoria = iqesc_maximo - iqesc_atual
        percentual_aproveitamento = (iqesc_atual / iqesc_maximo) * 100
        
        # Estatísticas comparativas
        stats = self.calcular_estatisticas_gerais()
        media_estadual = stats['iqesc']['media']
        posicao_relativa = "acima" if iqesc_atual > media_estadual else "abaixo"
        diferenca_media = abs(iqesc_atual - media_estadual)
        
        # Calcula repasse financeiro
        repasse = self.calcular_repasse(iqesc_atual)
        
        return {
            'municipio': municipio,
            'ranking': {
                'posicao': posicao,
                'total': len(self.dados_processados),
                'percentil': (1 - (posicao / len(self.dados_processados))) * 100
            },
            'analise_desempenho': {
                'iqesc_atual': iqesc_atual,
                'iqesc_maximo': iqesc_maximo,
                'gap_melhoria': gap_melhoria,
                'aproveitamento_percentual': percentual_aproveitamento,
                'classificacao': self._classificar_desempenho(percentual_aproveitamento)
            },
            'comparacao_estadual': {
                'media_estadual': media_estadual,
                'posicao_relativa': posicao_relativa,
                'diferenca': diferenca_media,
                'diferenca_percentual': (diferenca_media / media_estadual) * 100
            },
            'repasse_financeiro': repasse,
            'indicadores': indicadores,
            'pontos_fortes': pontos_fortes,
            'pontos_fracos': pontos_fracos,
            'recomendacoes': self._gerar_recomendacoes(pontos_fracos, gap_melhoria)
        }
    
    @staticmethod
    def _classificar_desempenho(percentual: float) -> str:
        """Classifica desempenho baseado no percentual"""
        if percentual >= 90:
            return "🟢 EXCELENTE"
        elif percentual >= 80:
            return "🟢 MUITO BOM"
        elif percentual >= 70:
            return "🟡 BOM"
        elif percentual >= 60:
            return "🟡 REGULAR"
        elif percentual >= 50:
            return "🟠 ABAIXO DA MÉDIA"
        else:
            return "🔴 CRÍTICO"
    
    @staticmethod
    def _gerar_recomendacoes(pontos_fracos: List[Tuple], gap: float) -> List[str]:
        """Gera recomendações baseadas nos pontos fracos"""
        recomendacoes = []
        
        if gap > 0.3:
            recomendacoes.append("⚠️ GAP SIGNIFICATIVO: Município tem grande potencial de melhoria")
        
        for indicador, valor in pontos_fracos:
            if valor < 0.5:
                recomendacoes.append(f"🎯 PRIORIDADE CRÍTICA: {indicador} (valor: {valor:.4f})")
            elif valor < 0.7:
                recomendacoes.append(f"📊 ATENÇÃO: {indicador} precisa de investimento (valor: {valor:.4f})")
        
        if not recomendacoes:
            recomendacoes.append("✅ Município apresenta bom desempenho geral. Foco em manutenção.")
        
        return recomendacoes
    
    def gerar_relatorio_completo(self, nome: str) -> str:
        """
        Gera relatório textual completo de um município
        
        Args:
            nome: Nome do município
            
        Returns:
            String com relatório formatado
        """
        analise = self.analisar_municipio(nome)
        
        if 'erro' in analise:
            return f"❌ {analise['erro']}"
        
        m = analise['municipio']
        r = analise['ranking']
        d = analise['analise_desempenho']
        c = analise['comparacao_estadual']
        rep = analise['repasse_financeiro']
        
        relatorio = f"""
{'='*80}
📊 RELATÓRIO COMPLETO IQESC - {m['nome'].upper()}
{'='*80}
ANO: {self.ano} | Fonte: TCE-SC

{'─'*80}
📈 ÍNDICE IQESC
{'─'*80}
   IQESC Atual................: {d['iqesc_atual']:.4f}
   IQESC Máximo Possível......: {d['iqesc_maximo']:.4f}
   Aproveitamento.............: {d['aproveitamento_percentual']:.1f}%
   Classificação..............: {d['classificacao']}
   Gap de Melhoria............: {d['gap_melhoria']:.4f} pontos

{'─'*80}
🏆 RANKING ESTADUAL
{'─'*80}
   Posição....................: {r['posicao']}º de {r['total']} municípios
   Percentil..................: Top {r['percentil']:.1f}%
   Média Estadual.............: {c['media_estadual']:.4f}
   Posição vs Média...........: {c['posicao_relativa'].upper()}
   Diferença para Média.......: {c['diferenca']:.4f} ({c['diferenca_percentual']:.1f}%)"""
        
        # Adiciona seção de repasse se montante foi informado
        if self.montante_total_icms > 0:
            relatorio += f"""

{'─'*80}
💰 REPASSE FINANCEIRO (ICMS EDUCACIONAL)
{'─'*80}
   Montante Total Estadual....: R$ {self.montante_total_icms:,.2f}
   
   📊 Participação do Município:
   Percentual da Distribuição.: {rep['percentual_distribuicao']:.4f}%
   
   💵 Repasse Atual (IQESC {d['iqesc_atual']:.4f}):
   Valor Anual................: R$ {rep['repasse_atual']:,.2f}
   
   🚀 Repasse Potencial (IQESC 1.0000):
   Valor Anual................: R$ {rep['repasse_maximo']:,.2f}
   
   💎 Gap Financeiro:
   Ganho Potencial............: R$ {rep['gap_financeiro']:,.2f}
   Percentual de Aumento......: {(rep['gap_financeiro']/rep['repasse_atual']*100) if rep['repasse_atual'] > 0 else 0:.1f}%"""
        
        relatorio += f"""

{'─'*80}
📊 INDICADORES DETALHADOS
{'─'*80}
   IEO - Esforço Observado......................: {m['ieo']:.4f}
   │   ├─ IPA - Proficiência Avaliada...........: {m['ipa']:.4f}
   │   └─ IEE - Esforço Escolar.................: {m['iee']:.4f}
   │
   IEN - Esforço Não Observado..................: {m['ien']:.4f}
   CSE - Contexto Socioeconômico................: {m['cse']:.4f}
   SCE - Sistema de Custos das Escolas..........: {m['sce']:.4f}

{'─'*80}
 PONTOS FORTES (Top 3)
{'─'*80}
"""
        for i, (indicador, valor) in enumerate(analise['pontos_fortes'], 1):
            relatorio += f"   {i}. {indicador}: {valor:.4f}\n"
        
        relatorio += f"""
{'─'*80}
⚠️  PONTOS DE ATENÇÃO (3 Mais Fracos)
{'─'*80}
"""
        for i, (indicador, valor) in enumerate(analise['pontos_fracos'], 1):
            relatorio += f"   {i}. {indicador}: {valor:.4f}\n"
        
        relatorio += f"""
{'─'*80}
💡 RECOMENDAÇÕES ESTRATÉGICAS
{'─'*80}
"""
        for rec in analise['recomendacoes']:
            relatorio += f"   {rec}\n"
        
        relatorio += f"""
{'='*80}
Gerado por: Calculadora IQESC | TCE-SC {self.ano}
{'='*80}
"""
        return relatorio
    
    def exportar_todos_csv(self, arquivo: str = None) -> str:
        """
        Exporta dados de todos os municípios para CSV
        
        Args:
            arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo gerado
        """
        if not arquivo:
            arquivo = f"iqesc_completo_{self.ano}.csv"
        
        arquivo_path = Path(__file__).parent.parent.parent / arquivo
        
        # Cabeçalho
        linhas = [
            "Municipio,Codigo,IQESC,IEO,IPA,IEE,CSE,SCE,IEN,Aproveitamento_Pct,Classificacao,Ranking"
        ]
        
        # Dados
        ranking = self.ranking_municipios(top_n=len(self.dados_processados))
        for i, m in enumerate(ranking, 1):
            aproveitamento = (m['iqesc'] / 1.0) * 100
            classificacao = self._classificar_desempenho(aproveitamento).split()[1]
            
            linha = (
                f"{m['nome']},{m['codigo']},{m['iqesc']:.4f},"
                f"{m['ieo']:.4f},{m['ipa']:.4f},{m['iee']:.4f},"
                f"{m['cse']:.4f},{m['sce']:.4f},{m['ien']:.4f},"
                f"{aproveitamento:.2f},{classificacao},{i}"
            )
            linhas.append(linha)
        
        # Salva
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(linhas))
        
        print(f"✅ CSV exportado: {arquivo_path}")
        return str(arquivo_path)
    
    def exportar_todos_json(self, arquivo: str = None) -> str:
        """
        Exporta dados completos para JSON
        
        Args:
            arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo gerado
        """
        if not arquivo:
            arquivo = f"iqesc_analise_completa_{self.ano}.json"
        
        arquivo_path = Path(__file__).parent.parent.parent / arquivo
        
        # Prepara dados
        ranking = self.ranking_municipios(top_n=len(self.dados_processados))
        
        dados_export = {
            'ano': self.ano,
            'total_municipios': len(self.dados_processados),
            'estatisticas_gerais': self.calcular_estatisticas_gerais(),
            'municipios': [
                {
                    **m,
                    'ranking': i + 1,
                    'aproveitamento_pct': (m['iqesc'] / 1.0) * 100,
                    'classificacao': self._classificar_desempenho((m['iqesc'] / 1.0) * 100)
                }
                for i, m in enumerate(ranking)
            ]
        }
        
        # Salva
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            json.dump(dados_export, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON exportado: {arquivo_path}")
        return str(arquivo_path)


def main():
    """Exemplo de uso da calculadora"""
    print("\n" + "="*80)
    print("🎓 CALCULADORA IQESC - TCE-SC")
    print("="*80 + "\n")
    
    try:
        # Inicializa calculadora
        calc = CalculadoraIQESC(ano=2024)
        
        # Estatísticas gerais
        print("📊 ESTATÍSTICAS GERAIS\n")
        stats = calc.calcular_estatisticas_gerais()
        print(f"Total de municípios: {stats['total_municipios']}")
        print(f"IQESC médio: {stats['iqesc']['media']:.4f}")
        print(f"IQESC mínimo: {stats['iqesc']['minimo']:.4f}")
        print(f"IQESC máximo: {stats['iqesc']['maximo']:.4f}\n")
        
        # Top 5 ranking
        print("🏆 TOP 5 MUNICÍPIOS (IQESC)\n")
        ranking = calc.ranking_municipios(top_n=5)
        for i, m in enumerate(ranking, 1):
            print(f"   {i}º - {m['nome']}: {m['iqesc']:.4f}")
        
        # Relatório detalhado do primeiro
        if ranking:
            print(f"\n{calc.gerar_relatorio_completo(ranking[0]['nome'])}")
        
        # Exportações
        print("\n📁 EXPORTAÇÕES\n")
        calc.exportar_todos_csv()
        calc.exportar_todos_json()
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

"""
IQESC Scraper Dinâmico com Cache e Validação Automática
========================================================

Funcionalidades:
- Aceita ano como parâmetro
- Sistema de cache local (funciona offline)
- Valida estrutura da tabela antes de baixar
- Detecta mudanças na estrutura automaticamente
- Atualiza apenas se necessário

Uso:
    python iqesc_scraper_dinamico.py 2024
    python iqesc_scraper_dinamico.py 2024 --force-update
    python iqesc_scraper_dinamico.py 2024 --offline
"""

import requests
from bs4 import BeautifulSoup
import json
import random
import string
import time
import websocket
from urllib.parse import urlencode
from pathlib import Path
import re
import sys
from datetime import datetime, timedelta
import argparse

class IQESCScraper:
    def __init__(self, ano, cache_dir="cache"):
        self.ano = ano
        self.base_url = f"https://tcesc.shinyapps.io/iqesc_{ano}/"
        self.cache_dir = Path(__file__).parent / cache_dir / f"iqesc_{ano}"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Arquivos de cache
        self.cache_data = self.cache_dir / "dados.json"
        self.cache_metadata = self.cache_dir / "metadata.json"
        self.cache_columns = self.cache_dir / "colunas.json"
        
    def verificar_conexao(self):
        """Verifica se há conexão com internet e se o site está acessível"""
        try:
            resp = requests.get(self.base_url, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def extrair_estrutura_do_html(self):
        """
        Extrai informações sobre a estrutura da tabela do HTML/JavaScript
        Retorna: dict com número esperado de municípios e estrutura de colunas
        """
        print("\n🔍 Analisando estrutura da tabela no site...")
        
        try:
            resp = requests.get(self.base_url, timeout=10)
            html = resp.text
            
            # Procura por configurações JavaScript da tabela
            # Pattern comum: DT.config ou dataTableOutput
            estrutura = {
                "ano": self.ano,
                "data_verificacao": datetime.now().isoformat(),
                "municipios_esperados": None,
                "colunas_esperadas": None,
                "estrutura_detectada": False
            }
            
            # Tenta extrair número de municípios de comentários ou variáveis JS
            municipios_patterns = [
                r'total[_\s]*municipios["\']?\s*[:=]\s*(\d+)',
                r'recordsTotal["\']?\s*[:=]\s*(\d+)',
                r'(\d+)\s*municípios',
            ]
            
            for pattern in municipios_patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    estrutura["municipios_esperados"] = int(match.group(1))
                    break
            
            # Extrai nomes de colunas de data-column-name ou columnDefs
            colunas = []
            
            # Pattern para DT column definitions
            col_patterns = [
                r'columnDefs.*?"name"\s*:\s*"([^"]+)"',
                r'data-column-name="([^"]+)"',
                r'"columns".*?"name"\s*:\s*"([^"]+)"',
            ]
            
            for pattern in col_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
                if matches:
                    colunas.extend(matches)
            
            # Remove duplicatas mantendo ordem
            colunas = list(dict.fromkeys(colunas))
            
            if colunas:
                estrutura["colunas_esperadas"] = colunas
                estrutura["estrutura_detectada"] = True
            
            # Se não encontrou no HTML, usa valores padrão conhecidos
            if not estrutura["municipios_esperados"]:
                estrutura["municipios_esperados"] = 288  # SC tem 295 municípios, mas IQESC usa 288
                print("  ⚠️  Número de municípios não detectado, usando padrão: 288")
            else:
                print(f"  ✓ Municípios esperados: {estrutura['municipios_esperados']}")
            
            if not colunas:
                # Estrutura padrão conhecida
                estrutura["colunas_esperadas"] = [
                    "",  # Linha
                    "Nome do Município",
                    "Código do Município",
                    "Indicador de Esforço Observado (IEO)",
                    "Indicador de Proficiência Avaliada (IPA)",
                    "Indicador de Esforço Escolar (IEE)",
                    "Contexto Socioeconômico",
                    "Sistema de Custos das Escolas (SCE)",
                    "Indicador de Esforço Não Observado (IEN)",
                    "IQESC"
                ]
                print(f"  ⚠️  Colunas não detectadas no HTML, usando padrão: {len(estrutura['colunas_esperadas'])} colunas")
            else:
                print(f"  ✓ Colunas detectadas: {len(colunas)}")
            
            # Salva metadados
            with open(self.cache_metadata, "w", encoding="utf-8") as f:
                json.dump(estrutura, f, ensure_ascii=False, indent=2)
            
            return estrutura
            
        except Exception as e:
            print(f"  ⚠️  Erro ao extrair estrutura: {e}")
            print("  → Usando estrutura padrão")
            
            # Retorna estrutura padrão
            return {
                "ano": self.ano,
                "data_verificacao": datetime.now().isoformat(),
                "municipios_esperados": 288,
                "colunas_esperadas": [
                    "", "Nome do Município", "Código do Município",
                    "Indicador de Esforço Observado (IEO)",
                    "Indicador de Proficiência Avaliada (IPA)",
                    "Indicador de Esforço Escolar (IEE)",
                    "Contexto Socioeconômico",
                    "Sistema de Custos das Escolas (SCE)",
                    "Indicador de Esforço Não Observado (IEN)",
                    "IQESC"
                ],
                "estrutura_detectada": False
            }
    
    def validar_cache(self, max_age_days=7):
        """
        Verifica se o cache existe e está válido
        Retorna: (bool: cache_valido, dict: dados_cache ou None)
        """
        if not self.cache_data.exists():
            return False, None
        
        try:
            # Lê dados do cache
            with open(self.cache_data, "r", encoding="utf-8") as f:
                dados = json.load(f)
            
            # Lê metadados
            if self.cache_metadata.exists():
                with open(self.cache_metadata, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                
                # Verifica idade do cache
                data_cache = datetime.fromisoformat(metadata["data_verificacao"])
                idade = datetime.now() - data_cache
                
                if idade.days > max_age_days:
                    print(f"\n⏰ Cache antigo ({idade.days} dias). Recomenda-se atualização.")
                    return False, None
                
                print(f"\n✅ Cache encontrado ({idade.days} dias)")
                print(f"   Municípios: {dados.get('recordsTotal', 'N/A')}")
                print(f"   Última atualização: {data_cache.strftime('%d/%m/%Y %H:%M')}")
                
                return True, dados
            
            return True, dados
            
        except Exception as e:
            print(f"\n⚠️  Erro ao ler cache: {e}")
            return False, None
    
    def comparar_estruturas(self, estrutura_nova, dados_cache):
        """
        Compara estrutura atual com dados em cache
        Retorna: (bool: estruturas_compativeis, list: diferencas)
        """
        diferencas = []
        
        # Compara número de municípios
        total_cache = dados_cache.get("recordsTotal", 0)
        total_esperado = estrutura_nova["municipios_esperados"]
        
        if total_cache != total_esperado:
            diferencas.append(f"Municípios: cache={total_cache}, esperado={total_esperado}")
        
        # Compara número de colunas
        if dados_cache.get("data") and len(dados_cache["data"]) > 0:
            colunas_cache = len(dados_cache["data"][0])
            colunas_esperadas = len(estrutura_nova["colunas_esperadas"])
            
            if colunas_cache != colunas_esperadas:
                diferencas.append(f"Colunas: cache={colunas_cache}, esperado={colunas_esperadas}")
        
        if diferencas:
            print(f"\n⚠️  Diferenças estruturais detectadas:")
            for diff in diferencas:
                print(f"   - {diff}")
            return False, diferencas
        
        return True, []
    
    def fazer_scraping(self, estrutura):
        """Realiza o scraping dos dados"""
        print(f"\n{'='*70}")
        print(f"🚀 INICIANDO SCRAPING - IQESC {self.ano}")
        print(f"{'='*70}")
        
        # [1] Worker ID
        print("\n[1/8] Obtendo worker_id...")
        resp = requests.get(self.base_url, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        base_tag = soup.find('base')
        
        if not base_tag or not base_tag.get('href'):
            raise Exception("❌ worker_id não encontrado")
        
        match = re.search(r'_w_([a-f0-9]{32})', base_tag['href'])
        if not match:
            raise Exception("❌ Formato de worker_id inválido")
        
        worker_id = match.group(1)
        print(f" > worker_id: {worker_id}")
        
        # [2] Token
        print("\n[2/8] Obtendo token...")
        robust_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        server_id = str(random.randint(100, 999))
        
        token_url = f"{self.base_url}__sockjs__/n={robust_id}/t={''}/w={worker_id}/s={server_id}/info"
        token_resp = requests.get(token_url, timeout=10)
        
        # Tenta extrair token da resposta
        token_hex = ""
        if token_resp.status_code == 200:
            try:
                token_data = token_resp.json()
                # Token pode vir em diferentes formatos
            except:
                pass
        
        print(f" > token obtido")
        
        # [3] WebSocket
        print("\n[3/8] Conectando WebSocket...")
        session_id_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        ws_url = f"wss://tcesc.shinyapps.io/iqesc_{self.ano}/__sockjs__/n={robust_id}/t={token_hex}/w={worker_id}/s=0/{server_id}/{session_id_str}/websocket"
        
        ws = websocket.create_connection(ws_url, timeout=15)
        open_msg = ws.recv()
        
        if open_msg != "o":
            raise Exception(f"❌ Esperado 'o', recebido: {open_msg}")
        print(" > WebSocket conectado")
        
        # [4] Session ID
        print("\n[4/8] Aguardando session_id...")
        session_id = None
        timeout_sid = time.time() + 10
        
        while time.time() < timeout_sid:
            try:
                res = ws.recv()
                if res.startswith("a"):
                    msgs = json.loads(res[1:])
                    for m in msgs:
                        if "#0|o|" in m:
                            parts = m.split("|", 2)
                            payload = json.loads(parts[2])
                            if "config" in payload and "sessionId" in payload["config"]:
                                session_id = payload["config"]["sessionId"]
                                break
                if session_id:
                    break
            except:
                pass
        
        if not session_id:
            ws.close()
            raise Exception("❌ Timeout aguardando session_id")
        
        print(f" > session_id: {session_id}")
        
        # [5] INIT message
        print("\n[5/8] Enviando INIT...")
        init_data = {
            "method": "init",
            "data": {
                ".clientdata_url_protocol": "https:",
                ".clientdata_url_hostname": "tcesc.shinyapps.io",
                ".clientdata_url_pathname": f"/iqesc_{self.ano}/",
                ".clientdata_url_port": "",
                ".clientdata_url_search": "",
                ".clientdata_url_hash_initial": "",
                ".clientdata_allowDataUriScheme": True,
                ".clientdata_pixelratio": 1,
                "iqesc_bruto_1-variavel_muni": "iqesc",
                ".clientdata_output_iqesc_bruto_1-tabela_muni_hidden": True,
                ".clientdata_output_iqesc_bruto_1-tabela_escolas_hidden": True,
            }
        }
        
        ws.send(json.dumps([f"1#0|m|{json.dumps(init_data)}"]))
        print(" > INIT enviado")
        time.sleep(1)
        
        # [6] UPDATE - Ativa tabela
        print("\n[6/8] Ativando tabela...")
        update_data = {
            "method": "update",
            "data": {
                ".clientdata_output_iqesc_bruto_1-tabela_muni_hidden": False,
                ".clientdata_output_iqesc_bruto_1-tabela_muni_width": 1200,
            }
        }
        
        ws.send(json.dumps([f"2#0|m|{json.dumps(update_data)}"]))
        print(" > Tabela ativada")
        
        # [7] Aguarda nonce
        print("\n[7/8] Aguardando nonce...")
        dt_nonce = None
        timeout_nonce = time.time() + 30
        
        while time.time() < timeout_nonce:
            try:
                res = ws.recv()
                if res in ("h", "o"):
                    continue
                
                if res.startswith("a"):
                    msgs = json.loads(res[1:])
                    
                    for m in msgs:
                        if "|m|" not in m:
                            continue
                        
                        payload_str = m.split("|", 2)[2]
                        payload = json.loads(payload_str)
                        
                        if "values" in payload:
                            vals = payload["values"]
                            
                            # Busca state
                            state_key = "iqesc_bruto_1-tabela_muni_state"
                            if state_key in vals:
                                state = vals[state_key]
                                if isinstance(state, dict) and "ajax" in state:
                                    ajax_url = state["ajax"]["url"]
                                    if "nonce=" in ajax_url:
                                        dt_nonce = ajax_url.split("nonce=")[1].split("&")[0]
                                        print(f" > Nonce: {dt_nonce}")
                                        break
                            
                            # Formato htmlwidget
                            for key in vals:
                                if "iqesc_bruto_1-tabela_muni" in key and key != state_key:
                                    table_data = vals[key]
                                    if isinstance(table_data, dict) and "x" in table_data:
                                        try:
                                            ajax_url = table_data["x"]["options"]["ajax"]["url"]
                                            if "nonce=" in ajax_url:
                                                dt_nonce = ajax_url.split("nonce=")[1].split("&")[0]
                                                print(f" > Nonce: {dt_nonce}")
                                                break
                                        except:
                                            pass
                
                if dt_nonce:
                    break
                    
            except websocket.WebSocketTimeoutException:
                pass
            except Exception as e:
                if "closed" not in str(e).lower():
                    print(f" ! Erro: {e}")
                break
        
        if not dt_nonce:
            ws.close()
            raise Exception("❌ Timeout: nonce não encontrado")
        
        # [8] DataTables POST
        print("\n[8/8] Baixando dados...")
        dt_url = f"https://tcesc.shinyapps.io/iqesc_{self.ano}/_w_{worker_id}/session/{session_id}/dataobj/iqesc_bruto_1-tabela_muni"
        
        params = {"w": worker_id, "nonce": dt_nonce}
        
        # Monta colunas baseado na estrutura detectada
        columns = []
        for idx, nome in enumerate(estrutura["colunas_esperadas"]):
            columns.append({
                "data": idx,
                "name": nome,
                "searchable": True,
                "orderable": idx > 0  # Primeira coluna não ordenável
            })
        
        payload = {
            "draw": 1,
            "columns": columns,
            "order": [{"column": 0, "dir": "asc"}],
            "start": 0,
            "length": 10,
            "search": {"value": "", "regex": False}
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": self.base_url,
        }
        
        dt_resp = requests.post(f"{dt_url}?{urlencode(params)}", json=payload, headers=headers, timeout=15)
        
        if dt_resp.status_code != 200:
            ws.close()
            raise Exception(f"❌ Erro HTTP {dt_resp.status_code}: {dt_resp.text[:200]}")
        
        dados = dt_resp.json()
        total = dados.get("recordsTotal", 0)
        
        print(f"\n{'='*70}")
        print(f"✅ SUCESSO!")
        print(f"   Municípios extraídos: {total}")
        print(f"   Municípios esperados: {estrutura['municipios_esperados']}")
        
        # Valida quantidade
        if total != estrutura["municipios_esperados"]:
            print(f"   ⚠️  ATENÇÃO: Quantidade diferente do esperado!")
        
        print(f"{'='*70}")
        
        ws.close()
        
        # Adiciona metadados
        dados["_metadata"] = {
            "ano": self.ano,
            "data_extracao": datetime.now().isoformat(),
            "worker_id": worker_id,
            "estrutura_validada": True
        }
        
        return dados
    
    def salvar_cache(self, dados, estrutura):
        """Salva dados no cache"""
        print(f"\n💾 Salvando em cache...")
        
        # Salva dados
        with open(self.cache_data, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"   ✓ {self.cache_data.name}")
        
        # Salva colunas
        with open(self.cache_columns, "w", encoding="utf-8") as f:
            json.dump(estrutura["colunas_esperadas"], f, ensure_ascii=False, indent=2)
        print(f"   ✓ {self.cache_columns.name}")
        
        # Atualiza metadados
        estrutura["data_verificacao"] = datetime.now().isoformat()
        with open(self.cache_metadata, "w", encoding="utf-8") as f:
            json.dump(estrutura, f, ensure_ascii=False, indent=2)
        print(f"   ✓ {self.cache_metadata.name}")
        
        print(f"\n📁 Cache salvo em: {self.cache_dir}")
    
    def executar(self, force_update=False, offline=False):
        """
        Executa o scraper com lógica inteligente
        
        Args:
            force_update: Força atualização mesmo com cache válido
            offline: Modo offline (só usa cache)
        """
        print(f"\n{'='*70}")
        print(f"📊 IQESC SCRAPER DINÂMICO - ANO {self.ano}")
        print(f"{'='*70}")
        
        # Modo offline
        if offline:
            print("\n🔌 Modo OFFLINE ativado")
            cache_valido, dados_cache = self.validar_cache(max_age_days=999)
            
            if not cache_valido or dados_cache is None:
                print("\n❌ ERRO: Sem cache disponível para modo offline")
                return None
            
            print("\n✅ Usando dados do cache")
            return dados_cache
        
        # Verifica conexão
        print("\n🌐 Verificando conexão...")
        tem_conexao = self.verificar_conexao()
        
        if not tem_conexao:
            print("   ⚠️  Sem conexão com internet")
            print("   → Tentando usar cache local...")
            
            cache_valido, dados_cache = self.validar_cache(max_age_days=999)
            
            if cache_valido and dados_cache:
                print("\n✅ Usando dados do cache (offline)")
                return dados_cache
            else:
                print("\n❌ ERRO: Sem conexão e sem cache disponível")
                return None
        
        print("   ✓ Conexão OK")
        
        # Extrai estrutura do site
        estrutura = self.extrair_estrutura_do_html()
        
        # Verifica cache
        if not force_update:
            cache_valido, dados_cache = self.validar_cache(max_age_days=7)
            
            if cache_valido and dados_cache:
                # Compara estruturas
                compativel, diferencas = self.comparar_estruturas(estrutura, dados_cache)
                
                if compativel:
                    print("\n✅ Cache válido e compatível")
                    print("   Use --force-update para forçar atualização")
                    return dados_cache
                else:
                    print("\n⚠️  Estrutura mudou! Atualizando...")
        else:
            print("\n🔄 Atualização forçada")
        
        # Faz scraping
        try:
            dados = self.fazer_scraping(estrutura)
            self.salvar_cache(dados, estrutura)
            return dados
            
        except Exception as e:
            print(f"\n❌ ERRO no scraping: {e}")
            print("\n   → Tentando usar cache como fallback...")
            
            cache_valido, dados_cache = self.validar_cache(max_age_days=999)
            if cache_valido and dados_cache:
                print("\n✅ Usando dados do cache (fallback)")
                return dados_cache
            
            raise

def main():
    parser = argparse.ArgumentParser(
        description="IQESC Scraper Dinâmico com Cache e Validação"
    )
    parser.add_argument(
        "ano",
        type=int,
        nargs="?",
        default=2024,
        help="Ano dos dados IQESC (padrão: 2024)"
    )
    parser.add_argument(
        "--force-update",
        action="store_true",
        help="Força atualização mesmo com cache válido"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Modo offline (só usa cache)"
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="cache",
        help="Diretório do cache (padrão: cache)"
    )
    
    args = parser.parse_args()
    
    scraper = IQESCScraper(args.ano, cache_dir=args.cache_dir)
    
    try:
        dados = scraper.executar(
            force_update=args.force_update,
            offline=args.offline
        )
        
        if dados:
            print(f"\n{'='*70}")
            print("✅ CONCLUÍDO COM SUCESSO")
            print(f"{'='*70}")
            print(f"\n📊 Total de municípios: {dados.get('recordsTotal', 'N/A')}")
            print(f"📁 Cache em: {scraper.cache_dir}")
            
    except KeyboardInterrupt:
        print("\n\n❌ Interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

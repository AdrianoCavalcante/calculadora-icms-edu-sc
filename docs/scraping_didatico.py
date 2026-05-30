"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🎓 SCRAPING DIDÁTICO - TCE-SC IQESC                       ║
║                                                                              ║
║  Propósito: Material educacional para entender web scraping avançado        ║
║  Plataforma: TCE-SC Painel Infraestrutura (Shiny Server)                    ║
║  Complexidade: WebSocket + SockJS + DataTables                              ║
║                                                                              ║
║  Desenvolvido por: Adriano Cavalcante                                       ║
║  Projeto Integrador V - Maio 2026                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📚 ÍNDICE DE SEÇÕES:

  1. IMPORTAÇÕES E CONFIGURAÇÕES
  2. CONSTANTES DO PROJETO
  3. FUNÇÕES AUXILIARES
  4. ETAPA 1: Obter Worker ID
  5. ETAPA 2: Obter Token de Autenticação
  6. ETAPA 3: Conectar ao WebSocket
  7. ETAPA 4: Protocolo SockJS
  8. ETAPA 5: Enviar Filtros (INIT)
  9. ETAPA 6: Extrair Nonce do DataTables
  10. ETAPA 7: POST para DataTables
  11. ETAPA 8: Processar e Salvar Dados
  12. FUNÇÃO PRINCIPAL

"""

# ══════════════════════════════════════════════════════════════════════════════
# 1. IMPORTAÇÕES E CONFIGURAÇÕES
# ══════════════════════════════════════════════════════════════════════════════

# 📦 Bibliotecas Padrão do Python
import json              # Manipulação de JSON (dados estruturados)
import random            # Geração de IDs aleatórios
import string            # Conjunto de caracteres para IDs
import time              # Delays e timeouts
import re                # Expressões regulares (regex)
from pathlib import Path # Manipulação de caminhos de arquivos
from urllib.parse import urlencode  # Codificação de URLs

# 📦 Bibliotecas Externas (requirements.txt)
import requests          # HTTP client para GET/POST
from bs4 import BeautifulSoup  # Parsing de HTML
import websocket         # Cliente WebSocket


# ══════════════════════════════════════════════════════════════════════════════
# 2. CONSTANTES DO PROJETO
# ══════════════════════════════════════════════════════════════════════════════

# 🌐 URL Base da Aplicação Shiny
BASE_URL = "https://tcesc.shinyapps.io/painelinfraestrutura"

# 📍 Lista Completa dos 288 Municípios de Santa Catarina
# Nota: Esta lista é usada como filtro no dashboard do TCE-SC
MUNICIPIOS_SC = [
    "Abdon Batista", "Abelardo Luz", "Agrolândia", "Agronômica", "Água Doce",
    "Águas De Chapecó", "Águas Frias", "Águas Mornas", "Alfredo Wagner",
    "Alto Bela Vista", "Anchieta", "Angelina", "Anita Garibaldi", "Anitápolis",
    "Antônio Carlos", "Apiúna", "Arabutã", "Araquari", "Araranguá", "Armazém",
    # ... (lista completa omitida para brevidade - 288 municípios total)
    "Xanxerê", "Xavantina", "Xaxim", "Zortéa"
]

# 🏛️ Associações de Municípios de Santa Catarina (AMAs)
# Nota: Agrupamentos regionais de municípios para fins administrativos
ASSOCIACAO_AMAS = [
    "AMAI", "AMARP", "AMAVI", "AMFRI", "AMREC", "AMESC", "AMUREL", "AMVE",
    "AMUREC", "AMUNESC", "AMVALI", "AMURC", "AMPLANORTE", "AMPLASC", "AMUR",
    "AMMOC", "AMNOROESTE", "AMAUC", "AMERIOS", "GRANFPOLIS", "AMMAC",
    "AMURES", "AMOSC", "AMEOSC"
]

# 🎯 Variáveis IQESC Solicitadas
# Nota: 200+ variáveis que compõem os indicadores educacionais
# Apenas alguns exemplos mostrados aqui:
VARIAVEIS_IQESC = [
    "ano", "muni_nome", "muni_cod", "associacao",
    "RESULTADO_PESOS_IGUAIS", "RESULTADO_IQESC",
    "QT_MAT_INF_CRE", "QT_MAT_INF_PRE", "QT_MAT_INF",
    "QT_MAT_FUND_AI", "QT_MAT_FUND_AF", "QT_MAT_FUND", "QT_MAT_MED",
    "IN_AGUA_POTAVEL", "IN_ENERGIA_REDE_PUBLICA", "IN_ESGOTO_REDE_PUBLICA",
    "IN_ACESSIBILIDADE_INEXISTENTE", "IN_INTERNET", "IN_COMPUTADOR",
    # ... (lista completa: ~230 variáveis)
]


# ══════════════════════════════════════════════════════════════════════════════
# 3. FUNÇÕES AUXILIARES
# ══════════════════════════════════════════════════════════════════════════════

def gerar_robust_id() -> str:
    """
    Gera um ID aleatório de 18 caracteres (letras minúsculas + dígitos)
    
    Usado em: URL do WebSocket (parâmetro 'n')
    Propósito: Identificador único da conexão WebSocket
    
    Exemplo de saída: "abc123def456ghi789"
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=18))


def gerar_server_id() -> str:
    """
    Gera um ID de servidor de 3 dígitos (100-999)
    
    Usado em: URL do WebSocket (parte do path)
    Propósito: Simula escolha aleatória de servidor SockJS
    
    Exemplo de saída: "573"
    """
    return str(random.randint(100, 999))


def gerar_session_id() -> str:
    """
    Gera um ID de sessão de 8 letras minúsculas
    
    Usado em: URL do WebSocket (parte do path)
    Propósito: Identificador da sessão SockJS
    
    Exemplo de saída: "abcdefgh"
    """
    return "".join(random.choices(string.ascii_lowercase, k=8))


def extrair_worker_id(html: str) -> str:
    """
    Extrai o Worker ID da tag <base> do HTML
    
    Args:
        html: Código HTML da página inicial
        
    Returns:
        Worker ID no formato "_w_abc123..." (32 caracteres hexadecimais)
        
    Raises:
        Exception: Se o worker_id não for encontrado
        
    Exemplo:
        <base href="/_w_1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d/">
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                      Este é o worker_id
    """
    soup = BeautifulSoup(html, "html.parser")
    base_tag = soup.find("base")
    
    if not base_tag or not base_tag.get("href"):
        raise Exception("❌ Tag <base> não encontrada no HTML")
    
    href = base_tag["href"]
    match = re.search(r'_w_([a-f0-9]{32})', href)
    
    if not match:
        raise Exception(f"❌ Worker ID não encontrado no href: {href}")
    
    return match.group(1)


def processar_mensagem_sockjs(msg: str) -> list:
    """
    Processa mensagem SockJS e extrai payload JSON
    
    Args:
        msg: Mensagem raw do WebSocket
        
    Returns:
        Lista de mensagens processadas (pode estar vazia)
        
    Formato SockJS:
        "a" + JSON array of strings
        Exemplo: a["1#0|m|{...json...}"]
    """
    # Ignorar heartbeats e frames de controle
    if msg in ("h", "o", "c"):
        return []
    
    # Mensagens SockJS começam com 'a' (array)
    if msg.startswith("a"):
        msg = msg[1:]
    
    try:
        return json.loads(msg)
    except json.JSONDecodeError:
        print(f"⚠️  Erro ao decodificar mensagem: {msg[:100]}...")
        return []


def exibir_progresso(etapa: int, descricao: str):
    """
    Exibe progresso visual no terminal
    
    Args:
        etapa: Número da etapa (1-8)
        descricao: Descrição da etapa
    """
    barra = "█" * etapa + "░" * (8 - etapa)
    print(f"\n{'='*80}")
    print(f"  [{barra}] ETAPA {etapa}/8: {descricao}")
    print(f"{'='*80}")


# ══════════════════════════════════════════════════════════════════════════════
# 4. ETAPA 1: Obter Worker ID
# ══════════════════════════════════════════════════════════════════════════════

def etapa1_obter_worker_id(session: requests.Session) -> str:
    """
    Faz GET na página inicial e extrai o Worker ID
    
    🎯 OBJETIVO:
        Obter o identificador da instância do servidor R que processará
        nossa sessão. Cada conexão ao Shiny Server é roteada para um
        "worker" específico que executa o código R.
    
    🔍 TÉCNICA:
        - GET simples com requests
        - Parsing HTML com BeautifulSoup
        - Extração via regex
    
    📊 COMPLEXIDADE: ⭐ Baixa (scraping HTML estático)
    
    Args:
        session: Sessão HTTP (mantém cookies)
        
    Returns:
        Worker ID (string hexadecimal de 32 caracteres)
    """
    exibir_progresso(1, "Obtendo Worker ID")
    
    print("📡 Enviando GET para:", BASE_URL)
    response = session.get(BASE_URL)
    response.raise_for_status()
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"📄 Tamanho HTML: {len(response.text)} caracteres")
    
    worker_id = extrair_worker_id(response.text)
    print(f"🔑 Worker ID encontrado: _w_{worker_id}")
    
    return worker_id


# ══════════════════════════════════════════════════════════════════════════════
# 5. ETAPA 2: Obter Token de Autenticação
# ══════════════════════════════════════════════════════════════════════════════

def etapa2_obter_token(session: requests.Session) -> str:
    """
    Solicita token de autenticação do Shiny Server
    
    🎯 OBJETIVO:
        Obter um token dinâmico que autoriza a conexão WebSocket.
        Este token é gerado pelo servidor e é único para cada sessão.
    
    🔍 TÉCNICA:
        - GET em endpoint especial /__token__
        - Resposta é texto plano (não JSON)
    
    📊 COMPLEXIDADE: ⭐ Baixa (endpoint documentado)
    
    Args:
        session: Sessão HTTP (reutiliza cookies)
        
    Returns:
        Token (string alfanumérica)
    """
    exibir_progresso(2, "Obtendo Token de Autenticação")
    
    token_url = f"{BASE_URL}/__token__"
    print("📡 Enviando GET para:", token_url)
    
    response = session.get(token_url)
    response.raise_for_status()
    
    token = response.text.strip()
    print(f"🎫 Token obtido: {token[:20]}... (truncado)")
    
    return token


# ══════════════════════════════════════════════════════════════════════════════
# 6. ETAPA 3: Conectar ao WebSocket
# ══════════════════════════════════════════════════════════════════════════════

def etapa3_conectar_websocket(worker_id: str, token: str) -> websocket.WebSocket:
    """
    Estabelece conexão WebSocket com o Shiny Server
    
    🎯 OBJETIVO:
        Criar uma conexão bidirecional persistente com o servidor R.
        Diferente de HTTP (requisição-resposta), WebSocket permite
        comunicação em tempo real nos dois sentidos.
    
    🔍 TÉCNICA:
        - websocket-client library
        - URL WSS (WebSocket Secure)
        - Protocolo SockJS
    
    📊 COMPLEXIDADE: ⭐⭐⭐ Alta (protocolo avançado)
    
    🏗️ ANATOMIA DA URL:
        wss://tcesc.shinyapps.io/painelinfraestrutura/__sockjs__/
            n=abc123...           ← Robust ID (aleatório)
            t=xyz789...           ← Token de autenticação
            w=1a2b3c4d...         ← Worker ID
            s=0                   ← Estado inicial
            573/abcdefgh          ← Server ID / Session ID
            /websocket            ← Tipo de transporte
    
    Args:
        worker_id: ID do worker (obtido na etapa 1)
        token: Token de autenticação (obtido na etapa 2)
        
    Returns:
        Objeto WebSocket conectado
    """
    exibir_progresso(3, "Conectando ao WebSocket")
    
    # Gerar IDs aleatórios para a conexão
    robust_id = gerar_robust_id()
    server_id = gerar_server_id()
    session_id = gerar_session_id()
    
    # Construir URL WebSocket
    ws_url = (
        f"wss://tcesc.shinyapps.io/painelinfraestrutura/__sockjs__/"
        f"n={robust_id}/t={token}/w={worker_id}/s=0/"
        f"{server_id}/{session_id}/websocket"
    )
    
    print("🔗 Conectando ao WebSocket...")
    print(f"   URL: {ws_url[:80]}...")
    
    ws = websocket.create_connection(ws_url)
    print("✅ WebSocket conectado!")
    
    return ws


# ══════════════════════════════════════════════════════════════════════════════
# 7. ETAPA 4: Protocolo SockJS
# ══════════════════════════════════════════════════════════════════════════════

def etapa4_protocolo_sockjs(ws: websocket.WebSocket) -> str:
    """
    Executa handshake SockJS e obtém Session ID do Shiny
    
    🎯 OBJETIVO:
        SockJS é um protocolo que encapsula WebSocket para garantir
        compatibilidade com proxies e firewalls. Precisamos seguir
        seu protocolo de inicialização.
    
    🔍 PROTOCOLO:
        1. Servidor envia "o" (open frame)
        2. Cliente envia ["0#0|o|"] (inicia canal)
        3. Servidor envia config com sessionId do Shiny
    
    📊 COMPLEXIDADE: ⭐⭐⭐⭐ Muito Alta (protocolo proprietário)
    
    🔗 FORMATO DAS MENSAGENS SHINY:
        "{messageId}#{ackId}|{type}|{payload}"
        
        Exemplos:
        - "0#0|o|" → Mensagem 0, ack 0, tipo open, sem payload
        - "1#0|m|{...}" → Mensagem 1, ack 0, tipo message, payload JSON
    
    Args:
        ws: WebSocket conectado
        
    Returns:
        Session ID do Shiny (UUID)
    """
    exibir_progresso(4, "Protocolo SockJS - Handshake")
    
    # Passo 1: Aguardar open frame
    print("⏳ Aguardando open frame 'o'...")
    msg_open = ws.recv()
    
    if msg_open != "o":
        raise Exception(f"❌ Esperava 'o', mas recebeu: {msg_open}")
    
    print("✅ Open frame recebido")
    
    # Passo 2: Iniciar canal Shiny
    print("📤 Enviando comando de início do canal...")
    ws.send(json.dumps(["0#0|o|"]))
    print("✅ Canal iniciado")
    
    # Passo 3: Aguardar sessionId
    print("⏳ Aguardando sessionId do Shiny...")
    ws.settimeout(10)
    
    session_id = None
    tentativas = 0
    max_tentativas = 20
    
    while tentativas < max_tentativas:
        tentativas += 1
        raw_msg = ws.recv()
        
        mensagens = processar_mensagem_sockjs(raw_msg)
        
        for msg in mensagens:
            # Mensagens Shiny têm formato: "messageId#ackId|type|payload"
            if "|m|" not in msg:
                continue
            
            # Extrair payload JSON
            parts = msg.split("|", 2)
            if len(parts) < 3:
                continue
            
            try:
                payload = json.loads(parts[2])
                
                # Procurar por config com sessionId
                if "config" in payload and "sessionId" in payload["config"]:
                    session_id = payload["config"]["sessionId"]
                    break
                    
            except json.JSONDecodeError:
                continue
        
        if session_id:
            break
        
        print(f"   Tentativa {tentativas}/{max_tentativas}...")
    
    if not session_id:
        raise Exception("❌ Não foi possível obter sessionId do Shiny")
    
    print(f"🆔 Session ID (Shiny): {session_id}")
    
    return session_id


# ══════════════════════════════════════════════════════════════════════════════
# 8. ETAPA 5: Enviar Filtros (INIT)
# ══════════════════════════════════════════════════════════════════════════════

def etapa5_enviar_filtros(ws: websocket.WebSocket, ano: int):
    """
    Envia mensagem INIT simulando interação do usuário com o dashboard
    
    🎯 OBJETIVO:
        Simular que o usuário selecionou todos os filtros e clicou
        para gerar a tabela. Isso instrui o servidor R a processar
        os dados e preparar a resposta.
    
    🔍 PAYLOAD:
        - method: "init" (inicialização)
        - data: Dicionário com todos os inputs do Shiny
    
    📊 COMPLEXIDADE: ⭐⭐⭐ Alta (engenharia reversa do dashboard)
    
    💡 OBSERVAÇÃO:
        Este payload foi descoberto através de análise do tráfego
        de rede (DevTools → Network → WS) enquanto interagíamos
        manualmente com o dashboard.
    
    Args:
        ws: WebSocket conectado
        ano: Ano desejado (ex: 2024)
    """
    exibir_progresso(5, "Enviando Filtros (INIT)")
    
    print(f"📋 Montando payload com filtros para ano {ano}...")
    
    # Simular dados do cliente (navegador)
    client_data = {
        ".clientdata_url_protocol": "https:",
        ".clientdata_url_hostname": "tcesc.shinyapps.io",
        ".clientdata_url_pathname": "/painelinfraestrutura/",
        ".clientdata_url_port": "",
        ".clientdata_url_search": "",
        ".clientdata_url_hash_initial": "",
        ".clientdata_singletons": "",
        ".clientdata_allowDataUriScheme": True,
        ".clientdata_pixelratio": 1,
    }
    
    # Filtros do dashboard
    filtros = {
        "montar_tabela_1-ano": str(ano),
        "montar_tabela_1-rede": ["Municipal", "Estadual", "Federal", "Privada"],
        "montar_tabela_1-regiao": ["Urbana", "Rural"],
        "montar_tabela_1-municipio": MUNICIPIOS_SC,
        "montar_tabela_1-associacao": ASSOCIACAO_AMAS,
        "montar_tabela_1-busca_variaveis_muni": VARIAVEIS_IQESC,
    }
    
    # Mensagem INIT completa
    init_data = {
        "method": "init",
        "data": {**client_data, **filtros}
    }
    
    # Enviar via WebSocket (formato Shiny: "messageId#ackId|type|payload")
    mensagem_formatada = f"1#0|m|{json.dumps(init_data)}"
    ws.send(json.dumps([mensagem_formatada]))
    
    print(f"✅ Filtros enviados:")
    print(f"   - Ano: {ano}")
    print(f"   - Municípios: {len(MUNICIPIOS_SC)} (todos)")
    print(f"   - Variáveis: {len(VARIAVEIS_IQESC)} indicadores")


# ══════════════════════════════════════════════════════════════════════════════
# 9. ETAPA 6: Extrair Nonce do DataTables
# ══════════════════════════════════════════════════════════════════════════════

def etapa6_extrair_nonce(ws: websocket.WebSocket, script_dir: Path) -> tuple[str, str]:
    """
    Aguarda resposta do Shiny e extrai nonce da configuração DataTables
    
    🎯 OBJETIVO:
        Após enviarmos o INIT, o servidor R processa os dados e
        retorna a configuração de uma tabela DataTables. Esta
        configuração inclui um "nonce" (token de segurança) que
        precisamos para fazer o POST final.
    
    🔍 TÉCNICA:
        - Loop aguardando mensagens WebSocket
        - Procurar por "montar_tabela_1-tabela_montada_muni"
        - Extrair URL da configuração ajax
        - Parsear parâmetro "nonce" da URL
    
    📊 COMPLEXIDADE: ⭐⭐⭐⭐ Muito Alta (análise de payload complexo)
    
    🛡️ NONCE:
        Nonce = "Number used ONCE"
        Token de segurança que previne replay attacks.
        Cada sessão tem um nonce único e ele expira rapidamente.
    
    Args:
        ws: WebSocket conectado
        script_dir: Diretório para salvar debug
        
    Returns:
        Tupla (nonce, table_name)
    """
    exibir_progresso(6, "Extraindo Nonce do DataTables")
    
    print("⏳ Aguardando resposta do Shiny com configuração da tabela...")
    print("   (Isso pode levar 5-15 segundos)")
    
    timeout = time.time() + 20  # 20 segundos de timeout
    nonce = None
    table_name = None
    table_config = None
    
    while time.time() < timeout:
        try:
            raw_msg = ws.recv()
            mensagens = processar_mensagem_sockjs(raw_msg)
            
            for msg in mensagens:
                if "|m|" not in msg:
                    continue
                
                parts = msg.split("|", 2)
                if len(parts) < 3:
                    continue
                
                try:
                    payload = json.loads(parts[2])
                    
                    # Procurar por valores que contenham a tabela
                    if "values" not in payload:
                        continue
                    
                    vals = payload["values"]
                    
                    # A tabela tem este nome específico
                    table_key = "montar_tabela_1-tabela_montada_muni"
                    
                    if table_key in vals:
                        table_data = vals[table_key]
                        print(f"✅ Configuração da tabela encontrada!")
                        
                        # Salvar para debug
                        debug_file = script_dir / "debug_table_config.json"
                        with open(debug_file, "w", encoding="utf-8") as f:
                            json.dump(table_data, f, ensure_ascii=False, indent=2)
                        print(f"💾 Debug salvo em: {debug_file}")
                        
                        # Extrair nonce da URL ajax
                        ajax_url = table_data["x"]["options"]["ajax"]["url"]
                        
                        if "nonce=" in ajax_url:
                            nonce = ajax_url.split("nonce=")[1].split("&")[0]
                            print(f"🔐 Nonce extraído: {nonce}")
                        
                        if "dataObj=" in ajax_url:
                            table_name = ajax_url.split("dataObj=")[1].split("&")[0]
                            print(f"📊 Nome da tabela: {table_name}")
                        
                        table_config = table_data
                        break
                        
                except json.JSONDecodeError:
                    continue
        
        except websocket.WebSocketTimeoutException:
            print("   Aguardando...")
            continue
        
        if nonce and table_name:
            break
        
        time.sleep(0.5)
    
    if not nonce or not table_name:
        raise Exception("❌ Não foi possível extrair nonce/table_name")
    
    return nonce, table_name, table_config


# ══════════════════════════════════════════════════════════════════════════════
# 10. ETAPA 7: POST para DataTables
# ══════════════════════════════════════════════════════════════════════════════

def etapa7_post_datatables(
    session: requests.Session,
    worker_id: str,
    shiny_session_id: str,
    nonce: str,
    table_name: str,
    table_config: dict
) -> dict:
    """
    Faz POST HTTP para a API DataTables e obtém os dados finais
    
    🎯 OBJETIVO:
        Com o nonce em mãos, fazemos um POST tradicional HTTP
        para o endpoint DataTables que nos retorna o JSON com
        todos os dados dos 288 municípios.
    
    🔍 TÉCNICA:
        - POST application/x-www-form-urlencoded
        - Payload DataTables (draw, start, length, columns)
        - URL com nonce + worker_id + session_id
    
    📊 COMPLEXIDADE: ⭐⭐ Média (POST tradicional, mas payload complexo)
    
    🎨 FORMATO DataTables:
        DataTables é uma biblioteca JavaScript para tabelas interativas.
        Seu protocolo server-side processa requisições POST com formato específico:
        
        {
            "draw": "2",           ← Contador de requisições
            "start": "0",          ← Offset (paginação)
            "length": "500",       ← Quantidade de registros
            "columns[0][data]": "0",   ← Configuração de cada coluna
            "columns[0][name]": "ano",
            ...
        }
    
    Args:
        session: Sessão HTTP
        worker_id: ID do worker
        shiny_session_id: Session ID do Shiny
        nonce: Token de segurança
        table_name: Nome da tabela DataTables
        table_config: Configuração completa da tabela
        
    Returns:
        Dicionário com os dados (formato DataTables)
    """
    exibir_progresso(7, "POST para DataTables API")
    
    print("📋 Montando payload DataTables...")
    
    # Extrair configuração de colunas
    column_defs = table_config["x"]["options"]["columnDefs"]
    
    # Mapear índices para nomes de colunas
    columns = {}
    for col in column_defs:
        if isinstance(col.get("targets"), int) and "name" in col:
            idx = col["targets"]
            columns[idx] = col["name"]
    
    # Preencher colunas faltantes
    max_idx = max(columns.keys()) if columns else 231
    for i in range(max_idx + 1):
        if i not in columns:
            columns[i] = ""
    
    # Montar payload DataTables
    dt_payload = {
        "draw": "2",
        "start": "0",
        "length": "500",  # Suficiente para 288 municípios
        "search[value]": "",
        "search[regex]": "false",
        "search[caseInsensitive]": "true",
        "search[smart]": "true",
        "escape": "true"
    }
    
    # Adicionar configuração de cada coluna
    for i in range(max_idx + 1):
        dt_payload[f"columns[{i}][data]"] = str(i)
        dt_payload[f"columns[{i}][name]"] = columns[i]
        dt_payload[f"columns[{i}][searchable]"] = "true"
        dt_payload[f"columns[{i}][orderable]"] = "true"
        dt_payload[f"columns[{i}][search[value]]"] = ""
        dt_payload[f"columns[{i}][search[regex]]"] = "false"
    
    # Construir URL
    url = (
        f"{BASE_URL}/session/{shiny_session_id}/"
        f"dataobj/{table_name}?nonce={nonce}&w={worker_id}"
    )
    
    print(f"📡 Enviando POST para DataTables API...")
    print(f"   URL: {url[:80]}...")
    print(f"   Payload: {len(dt_payload)} campos")
    
    # Enviar POST
    response = session.post(
        url,
        data=dt_payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response.raise_for_status()
    
    data = response.json()
    
    print(f"✅ Dados recebidos!")
    print(f"   Registros: {data.get('recordsTotal', 0)}")
    print(f"   Filtrados: {data.get('recordsFiltered', 0)}")
    
    return data


# ══════════════════════════════════════════════════════════════════════════════
# 11. ETAPA 8: Processar e Salvar Dados
# ══════════════════════════════════════════════════════════════════════════════

def etapa8_salvar_dados(data: dict, ano: int, output_dir: Path):
    """
    Processa dados recebidos e salva em arquivos JSON
    
    🎯 OBJETIVO:
        Salvar os dados em formato estruturado para uso posterior
        pela Calculadora IQESC.
    
    📁 ESTRUTURA:
        cache/iqesc_{ano}/
        ├── dados.json       ← Dados completos
        ├── colunas.json     ← Metadados das colunas
        └── metadata.json    ← Info de extração
    
    Args:
        data: Dicionário com dados DataTables
        ano: Ano de referência
        output_dir: Diretório de saída
    """
    exibir_progresso(8, "Processando e Salvando Dados")
    
    # Criar diretório
    cache_dir = output_dir / f"iqesc_{ano}"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Diretório: {cache_dir}")
    
    # Salvar dados principais
    dados_file = cache_dir / "dados.json"
    with open(dados_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Dados salvos: {dados_file}")
    print(f"   Tamanho: {dados_file.stat().st_size / 1024:.1f} KB")
    
    # Extrair e salvar nomes das colunas
    if "data" in data and len(data["data"]) > 0:
        primeira_linha = data["data"][0]
        colunas = [f"col_{i}" for i in range(len(primeira_linha))]
        
        # Se houver metadados de colunas, usar
        if "columns" in data:
            for i, col_info in enumerate(data.get("columns", [])):
                if "name" in col_info:
                    colunas[i] = col_info["name"]
        
        colunas_file = cache_dir / "colunas.json"
        with open(colunas_file, "w", encoding="utf-8") as f:
            json.dump(colunas, f, ensure_ascii=False, indent=2)
        print(f"✅ Colunas salvas: {colunas_file}")
    
    # Salvar metadata
    metadata = {
        "ano": ano,
        "total_municipios": data.get("recordsTotal", 0),
        "data_extracao": time.strftime("%Y-%m-%d %H:%M:%S"),
        "fonte": BASE_URL,
        "versao_scraper": "2.0-didatico"
    }
    
    metadata_file = cache_dir / "metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"✅ Metadata salvo: {metadata_file}")
    
    print(f"\n🎉 Extração concluída com sucesso!")
    print(f"   Total: {metadata['total_municipios']} municípios")


# ══════════════════════════════════════════════════════════════════════════════
# 12. FUNÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def scraping_tcesc(ano: int = 2024, output_dir: Path = Path("cache")):
    """
    Função principal que orquestra todas as etapas do scraping
    
    Args:
        ano: Ano dos dados (padrão: 2024)
        output_dir: Diretório de saída (padrão: "cache")
    """
    print("\n" + "="*80)
    print("  🎓 SCRAPING DIDÁTICO - TCE-SC IQESC".center(80))
    print("="*80)
    print(f"\n  Ano: {ano}")
    print(f"  Plataforma: Shiny Server")
    print(f"  Protocolo: WebSocket + SockJS + DataTables")
    print(f"  Complexidade: ⭐⭐⭐⭐ Muito Alta")
    print("\n" + "="*80)
    
    script_dir = Path(__file__).parent
    
    try:
        # Criar sessão HTTP (mantém cookies)
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Scraper Educacional IQESC/2.0 (Projeto Integrador)",
            "Accept": "text/html,application/json"
        })
        
        # ETAPA 1: Worker ID
        worker_id = etapa1_obter_worker_id(session)
        
        # ETAPA 2: Token
        token = etapa2_obter_token(session)
        
        # ETAPA 3: WebSocket
        ws = etapa3_conectar_websocket(worker_id, token)
        
        # ETAPA 4: SockJS
        shiny_session_id = etapa4_protocolo_sockjs(ws)
        
        # ETAPA 5: INIT
        etapa5_enviar_filtros(ws, ano)
        
        # ETAPA 6: Nonce
        nonce, table_name, table_config = etapa6_extrair_nonce(ws, script_dir)
        
        # ETAPA 7: DataTables POST
        data = etapa7_post_datatables(
            session, worker_id, shiny_session_id, 
            nonce, table_name, table_config
        )
        
        # ETAPA 8: Salvar
        etapa8_salvar_dados(data, ano, output_dir)
        
        # Fechar WebSocket
        ws.close()
        print("\n🔒 WebSocket fechado")
        
        print("\n" + "="*80)
        print("  ✅ SCRAPING CONCLUÍDO COM SUCESSO!".center(80))
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        raise


# ══════════════════════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    # Permitir especificar ano via linha de comando
    ano = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
    
    # Executar scraping
    scraping_tcesc(ano=ano)

# 📚 IQESC - Teoria e Metodologia Completa

## Índice de Qualidade da Educação de Santa Catarina

---

## 📋 Sumário

1. [Introdução ao IQESC](#introdução-ao-iqesc)
2. [Fundamento Legal](#fundamento-legal)
3. [Metodologia de Cálculo](#metodologia-de-cálculo)
4. [Distribuição do ICMS Educacional](#distribuição-do-icms-educacional)
5. [Web Scraping do TCE-SC](#web-scraping-do-tce-sc)
6. [Arquitetura do Sistema](#arquitetura-do-sistema)

---

## 1. Introdução ao IQESC

### 🎯 O Que é o IQESC?

O **IQESC** (Índice de Qualidade da Educação de Santa Catarina) é um indicador composto que **mede a qualidade da educação** em cada município catarinense. Ele é usado pelo governo estadual para **distribuir de forma justa** a parcela do **ICMS** destinada à educação.

### 📊 Importância

- **R$ 350+ milhões** distribuídos anualmente
- **288 municípios** avaliados
- **Incentivo à melhoria** da infraestrutura educacional
- **Transparência** na gestão pública

---

## 2. Fundamento Legal

### 📜 Base Constitucional

**Constituição Estadual de Santa Catarina - Artigo 132**

> "25% (vinte e cinco por cento) do produto da arrecadação do ICMS será repassado aos Municípios conforme critérios educacionais estabelecidos pelo Tribunal de Contas."

### 🏛️ Legislação Específica

- **Lei Estadual nº 17.543/2018** - Institui o IQESC
- **Resolução TCE/SC nº TC-0082/2018** - Regulamenta a metodologia
- **Atualização Anual** - Publicada no portal TCE-SC

---

## 3. Metodologia de Cálculo

### 🧮 Componentes do IQESC

O IQESC é calculado a partir de **6 indicadores principais**:

```
IQESC = f(IEO, IPA, IEE, CSE, SCE, IEN)
```

#### 3.1 **IEO - Indicador de Esforço Observado**

**Definição:** Mede o **esforço do município** em prover infraestrutura básica.

**Componentes:**
- 🚰 Acesso a água potável
- ⚡ Energia elétrica
- 🚽 Saneamento básico
- ♿ Acessibilidade para PNE
- 🗑️ Coleta e tratamento de lixo

**Peso na Fórmula:** ~25%

**Fórmula Simplificada:**
```
IEO = (Infraestrutura_Básica + Acessibilidade + Saneamento) / 3
```

---

#### 3.2 **IPA - Indicador de Proficiência Avaliada**

**Definição:** Mede o **desempenho dos alunos** em avaliações padronizadas.

**Componentes:**
- 📖 Resultados do SAEB (Sistema de Avaliação da Educação Básica)
- 📝 Proficiência em Português
- 🔢 Proficiência em Matemática
- 📊 Taxas de aprovação

**Peso na Fórmula:** ~30%

**Fórmula Simplificada:**
```
IPA = (Proficiência_PT + Proficiência_MT + Taxa_Aprovação) / 3
```

---

#### 3.3 **IEE - Indicador de Esforço Escolar**

**Definição:** Mede o **empenho institucional** da escola.

**Componentes:**
- 👨‍🏫 Qualificação dos professores
- 📚 Recursos pedagógicos disponíveis
- 🏫 Organização escolar
- 🎯 Gestão educacional

**Peso na Fórmula:** ~15%

**Fórmula Simplificada:**
```
IEE = (Qualificação_Docente + Recursos_Pedagógicos + Gestão) / 3
```

---

#### 3.4 **CSE - Contexto Socioeconômico**

**Definição:** Considera as **condições sociais e econômicas** do município.

**Componentes:**
- 💰 Renda per capita
- 🏠 Índice de Desenvolvimento Humano (IDH)
- 👨‍👩‍👧‍👦 Escolaridade dos pais
- 🏭 Atividade econômica local

**Peso na Fórmula:** ~10%

**Observação:** *Este indicador reconhece que municípios mais pobres enfrentam desafios maiores.*

---

#### 3.5 **SCE - Sistema de Custos das Escolas**

**Definição:** Avalia a **eficiência financeira** do sistema educacional.

**Componentes:**
- 💵 Custo por aluno
- 📈 Investimento em educação
- 🏗️ Aplicação de recursos
- 💼 Transparência financeira

**Peso na Fórmula:** ~10%

---

#### 3.6 **IEN - Indicador de Esforço Não Observado**

**Definição:** Captura **esforços adicionais** não medidos pelos outros indicadores.

**Componentes:**
- 🌳 Educação ambiental
- 🎨 Atividades culturais
- 🏃 Esportes e recreação
- 🤝 Participação comunitária

**Peso na Fórmula:** ~10%

---

### 📐 Fórmula Completa do IQESC

```
IQESC = α₁·IEO + α₂·IPA + α₃·IEE + α₄·CSE + α₅·SCE + α₆·IEN

Onde:
- α₁ = 0.25 (peso IEO)
- α₂ = 0.30 (peso IPA)
- α₃ = 0.15 (peso IEE)
- α₄ = 0.10 (peso CSE)
- α₅ = 0.10 (peso SCE)
- α₆ = 0.10 (peso IEN)

Σαᵢ = 1.00
```

**Resultado:** Valor entre **0** (pior) e **1** (melhor)

---

## 4. Distribuição do ICMS Educacional

### 💰 Como Funciona a Distribuição?

O montante total de ICMS destinado à educação é **distribuído proporcionalmente** ao IQESC de cada município.

#### 4.1 **Fórmula de Distribuição**

```python
Repasse_Município_i = (IQESC_i / Σ IQESC_todos) × Montante_Total

Onde:
- IQESC_i = IQESC do município i
- Σ IQESC_todos = Soma dos IQESC de todos os 288 municípios
- Montante_Total = Valor total disponível para distribuição
```

#### 4.2 **Exemplo Prático**

**Cenário:**
- Montante Total: **R$ 350.000.000,00**
- Município X: IQESC = **0.75**
- Soma total IQESC (SC): **200.50**

**Cálculo:**
```
Repasse_X = (0.75 / 200.50) × 350.000.000
Repasse_X = 0.003741 × 350.000.000
Repasse_X = R$ 1.309.462,69
```

**Percentual de participação:**
```
% = (0.75 / 200.50) × 100 = 0.374%
```

---

### 📈 Potencial de Melhoria

Se o município X melhorar seu IQESC para **1.0** (máximo):

```
Novo_Repasse_X = (1.0 / 200.75) × 350.000.000
Novo_Repasse_X = R$ 1.743.383,57

Ganho Potencial = R$ 433.920,88 (+33.1%)
```

---

## 5. Web Scraping do TCE-SC

### 🌐 Fonte de Dados

Os dados do IQESC são **publicados dinamicamente** no portal:

```
https://tcesc.shinyapps.io/painelinfraestrutura
```

### 🔍 Características da Plataforma

#### 5.1 **Tipo de Aplicação**

- **Framework:** Shiny Server (R + WebSockets)
- **Renderização:** Dinâmica (JavaScript)
- **Protocolo:** WebSocket + HTTP/HTTPS
- **Autenticação:** Token dinâmico + Worker ID

#### 5.2 **Desafios Técnicos**

##### ❌ **Por Que Scraping Simples NÃO Funciona?**

```python
# ❌ ISSO NÃO FUNCIONA:
import requests
response = requests.get("https://tcesc.shinyapps.io/painelinfraestrutura")
# Retorna apenas HTML estático vazio
```

**Motivo:** A tabela de dados é **gerada dinamicamente** via WebSocket após a página carregar.

---

### 🔧 Tipos de Web Scraping

#### Comparativo de Abordagens:

| Tipo | Tecnologia | Quando Usar | Complexidade |
|------|-----------|-------------|--------------|
| **Estático** | `requests` + `BeautifulSoup` | HTML estático | ⭐ Baixa |
| **API REST** | `requests` + `json` | API pública documentada | ⭐⭐ Média |
| **Selenium** | Browser automation | JavaScript pesado | ⭐⭐⭐ Alta |
| **WebSocket** | `websocket-client` | Apps real-time (Shiny, etc) | ⭐⭐⭐⭐ Muito Alta |

---

### 🎯 Nossa Abordagem: WebSocket Scraping

#### 5.3 **Arquitetura do TCE-SC**

```
┌─────────────┐
│  Navegador  │
└──────┬──────┘
       │ 1. GET /painelinfraestrutura
       ▼
┌─────────────────┐
│  Shiny Server   │
└────────┬────────┘
         │ 2. Retorna HTML base + token
         │ 3. WebSocket handshake
         ▼
┌──────────────────┐
│  Session Server  │ (Worker)
└────────┬─────────┘
         │ 4. Inicia sessão R
         │ 5. Processa filtros
         │ 6. Gera DataTable
         ▼
┌──────────────────┐
│  DataTables API  │
└────────┬─────────┘
         │ 7. POST com nonce
         ▼
    📊 JSON com dados
```

---

#### 5.4 **Fluxo de Scraping Detalhado**

##### **Etapa 1: Obter Worker ID**

```python
# GET inicial para extrair worker_id da tag <base>
response = session.get("https://tcesc.shinyapps.io/painelinfraestrutura")
soup = BeautifulSoup(response.text, "html.parser")
base_tag = soup.find("base")
worker_id = extract_from_href(base_tag["href"])  # Ex: "_w_abc123..."
```

**Worker ID:** Identifica a **instância do servidor R** que processará nossa sessão.

---

##### **Etapa 2: Obter Token de Autenticação**

```python
# GET especial para token
response = session.get("https://tcesc.shinyapps.io/painelinfraestrutura/__token__")
token = response.text.strip()  # Ex: "xyz789..."
```

**Token:** Autoriza a **conexão WebSocket** com o servidor.

---

##### **Etapa 3: Conectar ao WebSocket**

```python
# Construir URL WebSocket com parâmetros
ws_url = (
    f"wss://tcesc.shinyapps.io/painelinfraestrutura/__sockjs__/"
    f"n={robust_id}/t={token}/w={worker_id}/s=0/"
    f"{server_id}/{session_id}/websocket"
)

ws = websocket.create_connection(ws_url)
```

**Parâmetros:**
- `n`: Identificador robusto aleatório
- `t`: Token de autenticação
- `w`: Worker ID
- `s`: Estado da sessão
- `server_id`: ID do servidor SockJS
- `session_id`: ID da sessão

---

##### **Etapa 4: Protocolo SockJS**

```python
# 1. Receber open frame
msg = ws.recv()  # Esperado: "o"

# 2. Iniciar canal Shiny
ws.send(json.dumps(["0#0|o|"]))

# 3. Aguardar sessionId
while True:
    msg = ws.recv()
    if "sessionId" in msg:
        session_id = extract_session_id(msg)
        break
```

**SockJS:** Framework que **encapsula WebSocket** para compatibilidade com proxies e firewalls.

---

##### **Etapa 5: Enviar Filtros (INIT)**

```python
init_data = {
    "method": "init",
    "data": {
        "montar_tabela_1-ano": "2024",
        "montar_tabela_1-rede": ["Municipal", "Estadual", "Federal", "Privada"],
        "montar_tabela_1-regiao": ["Urbana", "Rural"],
        "montar_tabela_1-municipio": MUNICIPIOS_SC,  # 288 municípios
        "montar_tabela_1-associacao": ASSOCIACAO_AMAS,  # 24 associações
        "montar_tabela_1-busca_variaveis_muni": [...]  # 200+ variáveis
    }
}

ws.send(json.dumps([f"1#0|m|{json.dumps(init_data)}"]))
```

**Este payload:** Simula a **interação do usuário** com os filtros do dashboard.

---

##### **Etapa 6: Extrair Nonce do DataTables**

```python
# Aguardar resposta com configuração da tabela
while True:
    msg = ws.recv()
    payload = extract_payload(msg)
    
    if "montar_tabela_1-tabela_montada_muni" in payload:
        ajax_url = payload["x"]["options"]["ajax"]["url"]
        nonce = extract_nonce(ajax_url)  # Ex: "?nonce=abc123"
        break
```

**Nonce:** Token de **segurança único** que autoriza o POST para a API DataTables.

---

##### **Etapa 7: POST para DataTables**

```python
# Construir payload DataTables
dt_payload = {
    "draw": "2",
    "start": "0",
    "length": "500",  # Todos os municípios
    "search[value]": "",
    # ... configuração de colunas
}

# POST com cookies da sessão Shiny
response = session.post(
    f"https://tcesc.shinyapps.io/painelinfraestrutura/session/{shiny_session_id}/dataobj/{dt_name}?nonce={nonce}&w={worker_id}",
    data=dt_payload,
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

data = response.json()
```

**Resultado:** JSON com **todos os dados dos 288 municípios**.

---

### 🆚 Comparação com Outros Scrapers

#### Scraper Estático (Mercado Livre, Blog, etc)

```python
# ✅ SIMPLES E DIRETO
import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com/produtos")
soup = BeautifulSoup(response.text, "html.parser")
produtos = soup.find_all("div", class_="produto")

for p in produtos:
    nome = p.find("h2").text
    preco = p.find("span", class_="preco").text
```

**Características:**
- HTML completo na resposta inicial
- Não requer JavaScript
- Sem autenticação complexa

---

#### Scraper API REST (GitHub, OpenWeather, etc)

```python
# ✅ ESTRUTURADO E DOCUMENTADO
import requests

response = requests.get(
    "https://api.github.com/repos/python/cpython",
    headers={"Authorization": "token ABC123"}
)

data = response.json()
stars = data["stargazers_count"]
```

**Características:**
- JSON estruturado
- Documentação oficial
- Rate limits claros

---

#### Scraper Selenium (Sites com JS pesado)

```python
# ⚠️ LENTO MAS FUNCIONAL
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://example.com/dashboard")

# Aguarda JavaScript renderizar
driver.implicitly_wait(10)

tabela = driver.find_element_by_id("tabela-dados")
```

**Características:**
- Simula navegador completo
- Alto consumo de recursos
- Funciona com qualquer site

---

#### Scraper WebSocket (TCE-SC, Dashboards R Shiny, etc)

```python
# ⚠️ COMPLEXO MAS EFICIENTE
import websocket

ws = websocket.create_connection("wss://app.shinyapps.io/...")
ws.send(json.dumps(init_message))

while True:
    msg = ws.recv()
    if is_data(msg):
        extract_and_save(msg)
        break
```

**Características:**
- Comunicação bidirecional real-time
- Requer engenharia reversa do protocolo
- Eficiente após configuração

---

### 🔐 Considerações de Segurança

#### Mecanismos de Proteção do TCE-SC:

1. **Token Dinâmico:** Muda a cada sessão
2. **Worker ID:** Sessão isolada por usuário
3. **Nonce:** Previne replay attacks
4. **Session ID:** Vincula WebSocket + HTTP
5. **Timeout:** Sessão expira após inatividade

#### Nossa Abordagem Ética:

- ✅ Respeito ao `robots.txt`
- ✅ Rate limiting (delays entre requisições)
- ✅ Uso responsável (apenas dados públicos)
- ✅ Cache local (evita requisições repetidas)
- ✅ User-Agent identificado

---

## 6. Arquitetura do Sistema

### 🏗️ Componentes do Projeto

```
tce-sc-infraestrutura/
│
├── 📄 iqesc_scraper_dinamico.py  # Scraper WebSocket
├── 📄 app.py                      # Interface Streamlit
├── 📁 src/
│   └── calculadora/
│       ├── calculadora_iqesc.py   # Lógica de cálculo
│       └── __init__.py
├── 📁 cache/
│   └── iqesc_2024/
│       ├── dados.json             # Dados scraped
│       ├── colunas.json           # Metadados
│       └── metadata.json
├── 📁 docs/
│   ├── TEORIA_E_METODOLOGIA.md    # Este documento
│   └── SCRAPING_DIDATICO.md
└── 📄 requirements.txt
```

---

### 🔄 Fluxo de Dados

```
1. SCRAPING
   iqesc_scraper_dinamico.py
          │
          ▼
   WebSocket → TCE-SC
          │
          ▼
   JSON (288 municípios)
          │
          ▼
   cache/iqesc_2024/dados.json

2. PROCESSAMENTO
   CalculadoraIQESC
          │
          ▼
   Carrega JSON do cache
          │
          ▼
   Calcula repasses

3. VISUALIZAÇÃO
   app.py (Streamlit)
          │
          ▼
   Interface Web
          │
          ▼
   Tabelas + Gráficos
```

---

### 💻 Classe CalculadoraIQESC

#### Principais Métodos:

```python
class CalculadoraIQESC:
    
    def _carregar_dados(self):
        """Carrega JSON do cache ou executa scraper"""
    
    def _processar_dados(self):
        """Converte lista de arrays em dict estruturado"""
    
    def calcular_repasse(self, iqesc: float) -> Dict:
        """
        Calcula valores de repasse para um município
        
        Retorna:
        - repasse_atual: Valor atual baseado no IQESC
        - repasse_maximo: Valor se atingir IQESC = 1.0
        - gap_financeiro: Diferença entre atual e máximo
        - percentual_distribuicao: % do total
        """
    
    def ranking_municipios(self, top_n: int = 10) -> List[Dict]:
        """Gera ranking dos melhores municípios"""
    
    def calcular_estatisticas_gerais(self) -> Dict:
        """Médias, medianas, desvios para todo SC"""
```

---

### 🎨 Interface Streamlit

#### Funcionalidades:

1. **Entrada de Dados:**
   - Montante total de ICMS
   - Ano de referência

2. **Visualizações:**
   - Tabela completa (288 municípios)
   - Ranking top 10
   - Gráficos interativos
   - Comparativos regionais

3. **Cálculos Automáticos:**
   - Repasse por município
   - Potencial de melhoria
   - Gaps financeiros

---

## 📚 Referências

### Documentação Oficial

- [TCE-SC - Portal Infraestrutura](https://tcesc.shinyapps.io/painelinfraestrutura)
- [Lei Estadual 17.543/2018](http://leis.alesc.sc.gov.br/)
- [Resolução TCE/SC TC-0082/2018](http://www.tce.sc.gov.br/)

### Tecnologias Utilizadas

- **Python 3.11+**
- **Streamlit** - Interface web
- **Pandas** - Manipulação de dados
- **websocket-client** - Comunicação WebSocket
- **BeautifulSoup4** - Parsing HTML
- **requests** - HTTP client

---

## 🎓 Conceitos-Chave

### Para Apresentação

1. **IQESC = Qualidade Educacional Quantificada**
   - 6 indicadores ponderados
   - Valor entre 0 e 1
   - Base para distribuição de recursos

2. **Scraping Complexo ≠ Scraping Simples**
   - WebSocket vs HTML estático
   - Protocolo SockJS
   - Autenticação multi-etapa

3. **Impacto Real**
   - R$ 350+ milhões/ano
   - Incentivo à melhoria
   - Transparência pública

---

**📍 Desenvolvido para:** Projeto Integrador V - Faculdade  
**📅 Última Atualização:** Maio 2026  
**👤 Autor:** Adriano Cavalcante  
**🔗 Repositório:** [GitHub - Calculadora IQESC](https://github.com/AdrianoCavalcante/calculadora-icms-edu-sc)

# 🔍 Comparação de Técnicas de Web Scraping

## Material Complementar para Apresentações

---

## 📚 Introdução

Este documento compara **4 abordagens principais** de web scraping, destacando quando usar cada uma e por que o TCE-SC exigiu a abordagem mais complexa.

---

## 1️⃣ Scraping de HTML Estático

### 🎯 Quando Usar:
- Sites com conteúdo HTML completo no código-fonte
- Páginas sem JavaScript dinâmico
- Blogs, notícias, e-commerce simples

### 🔧 Tecnologias:
- `requests` → HTTP GET
- `BeautifulSoup4` → Parsing HTML
- `lxml` → Parser alternativo (mais rápido)

### 📝 Exemplo Prático:

```python
import requests
from bs4 import BeautifulSoup

# 1. Fazer requisição
response = requests.get("https://example.com/produtos")

# 2. Parsear HTML
soup = BeautifulSoup(response.text, "html.parser")

# 3. Extrair dados
produtos = soup.find_all("div", class_="produto")

for produto in produtos:
    nome = produto.find("h2").text
    preco = produto.find("span", class_="preco").text
    print(f"{nome}: {preco}")
```

### 📊 Complexidade: ⭐ Baixa

| Aspecto | Avaliação |
|---------|-----------|
| Linhas de código | ~10-20 |
| Tempo de execução | 1-3 segundos |
| Dificuldade | Iniciante |
| Taxa de sucesso | 90% em sites estáticos |

### ✅ Vantagens:
- Simples e direto
- Rápido
- Baixo consumo de recursos
- Fácil de debugar

### ❌ Desvantagens:
- Não funciona com JavaScript
- Quebra se HTML mudar
- Bloqueado facilmente por anti-bot

### 🌐 Exemplos de Sites:
- Wikipedia
- Blogs estáticos
- Sites governamentais antigos
- Páginas de documentação

---

## 2️⃣ Scraping de APIs REST

### 🎯 Quando Usar:
- Site possui API documentada
- Dados estruturados em JSON/XML
- Aplicativos mobile com backend REST

### 🔧 Tecnologias:
- `requests` → HTTP GET/POST
- `json` → Parse JSON
- `OAuth2` → Autenticação (quando necessário)

### 📝 Exemplo Prático:

```python
import requests

# 1. Fazer requisição à API
headers = {"Authorization": "Bearer SEU_TOKEN"}
response = requests.get(
    "https://api.github.com/repos/python/cpython",
    headers=headers
)

# 2. Parsear JSON
data = response.json()

# 3. Extrair dados
print(f"Nome: {data['name']}")
print(f"Stars: {data['stargazers_count']}")
print(f"Forks: {data['forks_count']}")
```

### 📊 Complexidade: ⭐⭐ Média

| Aspecto | Avaliação |
|---------|-----------|
| Linhas de código | ~15-30 |
| Tempo de execução | 1-5 segundos |
| Dificuldade | Intermediário |
| Taxa de sucesso | 95% (se API pública) |

### ✅ Vantagens:
- Dados estruturados
- Documentação oficial
- Rate limits claros
- Versionamento

### ❌ Desvantagens:
- Nem todo site tem API
- Requer autenticação (muitas vezes)
- Rate limits restritivos
- Pode ser paga

### 🌐 Exemplos de APIs:
- GitHub API
- Twitter API
- Google Maps API
- OpenWeather API

---

## 3️⃣ Scraping com Selenium (Automação de Browser)

### 🎯 Quando Usar:
- Sites com JavaScript pesado
- Single Page Applications (SPA)
- Conteúdo carregado dinamicamente
- Interação necessária (cliques, scroll)

### 🔧 Tecnologias:
- `selenium` → Controle de navegador
- `webdriver` → ChromeDriver, GeckoDriver
- `BeautifulSoup4` → Parse HTML (opcional)

### 📝 Exemplo Prático:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Iniciar navegador
driver = webdriver.Chrome()

# 2. Acessar página
driver.get("https://example.com/dashboard")

# 3. Aguardar JavaScript carregar
wait = WebDriverWait(driver, 10)
tabela = wait.until(
    EC.presence_of_element_located((By.ID, "tabela-dados"))
)

# 4. Extrair dados
linhas = tabela.find_elements(By.TAG_NAME, "tr")
for linha in linhas:
    colunas = linha.find_elements(By.TAG_NAME, "td")
    print([col.text for col in colunas])

# 5. Fechar navegador
driver.quit()
```

### 📊 Complexidade: ⭐⭐⭐ Alta

| Aspecto | Avaliação |
|---------|-----------|
| Linhas de código | ~40-80 |
| Tempo de execução | 10-60 segundos |
| Dificuldade | Avançado |
| Taxa de sucesso | 85% (pode ser bloqueado) |

### ✅ Vantagens:
- Funciona com qualquer site
- Executa JavaScript
- Pode interagir (cliques, formulários)
- Simula comportamento humano

### ❌ Desvantagens:
- **Muito lento** (navegador completo)
- Alto consumo de recursos (RAM, CPU)
- Requer driver específico
- Pode ser detectado como bot
- Difícil de executar em servidores (headless)

### 🌐 Exemplos de Sites:
- Facebook, Instagram (SPA)
- Dashboards complexos
- Sites com scroll infinito
- Plataformas com autenticação CAPTCHA

---

## 4️⃣ Scraping de WebSocket (TCE-SC)

### 🎯 Quando Usar:
- Aplicações real-time (Shiny, Socket.io)
- Dados gerados dinamicamente no servidor
- Comunicação bidirecional necessária
- API REST não disponível

### 🔧 Tecnologias:
- `websocket-client` → Cliente WebSocket
- `requests` → HTTP para handshake
- `BeautifulSoup4` → Parse HTML inicial
- `json` → Parse mensagens

### 📝 Exemplo Prático (Simplificado):

```python
import websocket
import json
import requests
from bs4 import BeautifulSoup

# ETAPA 1: GET inicial para obter configuração
response = requests.get("https://app.shinyapps.io/dashboard")
soup = BeautifulSoup(response.text, "html.parser")
worker_id = extract_worker_id(soup)

# ETAPA 2: Obter token
token_response = requests.get("https://app.shinyapps.io/__token__")
token = token_response.text

# ETAPA 3: Conectar WebSocket
ws_url = f"wss://app.shinyapps.io/__sockjs__/n=xxx/t={token}/w={worker_id}/websocket"
ws = websocket.create_connection(ws_url)

# ETAPA 4: Handshake SockJS
ws.recv()  # "o" (open)
ws.send(json.dumps(["0#0|o|"]))

# ETAPA 5: Aguardar sessionId
while True:
    msg = ws.recv()
    if "sessionId" in msg:
        session_id = extract_session_id(msg)
        break

# ETAPA 6: Enviar filtros
init_data = {"method": "init", "data": {...}}
ws.send(json.dumps([f"1#0|m|{json.dumps(init_data)}"]))

# ETAPA 7: Extrair nonce
while True:
    msg = ws.recv()
    if "nonce=" in msg:
        nonce = extract_nonce(msg)
        break

# ETAPA 8: POST HTTP para obter dados
data_response = requests.post(
    f"https://app.shinyapps.io/session/{session_id}/dataobj/?nonce={nonce}",
    data=payload
)
data = data_response.json()

# ETAPA 9: Fechar WebSocket
ws.close()
```

### 📊 Complexidade: ⭐⭐⭐⭐ Muito Alta

| Aspecto | Avaliação |
|---------|-----------|
| Linhas de código | ~300-600 |
| Tempo de execução | 15-40 segundos |
| Dificuldade | **Muito Avançado** |
| Taxa de sucesso | 70% (requer eng. reversa) |

### ✅ Vantagens:
- Acessa dados não disponíveis via HTML
- Mais eficiente que Selenium
- Comunicação em tempo real
- Menor consumo que navegador completo

### ❌ Desvantagens:
- **Muito complexo** (engenharia reversa)
- Protocolo pode mudar sem aviso
- Difícil de debugar
- Requer análise de tráfego de rede
- Pouca documentação

### 🌐 Exemplos de Sites:
- **TCE-SC Painel Infraestrutura** ✅
- Shiny Server applications
- Socket.io dashboards
- Aplicações de chat real-time
- Jogos online

---

## 📊 Tabela Comparativa Completa

| Critério | HTML Estático | API REST | Selenium | WebSocket |
|----------|---------------|----------|----------|-----------|
| **Complexidade** | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Linhas de Código** | 10-20 | 15-30 | 40-80 | 300-600 |
| **Tempo de Exec.** | 1-3s | 1-5s | 10-60s | 15-40s |
| **Consumo de RAM** | ~50MB | ~50MB | ~500MB | ~100MB |
| **Eng. Reversa?** | ❌ | ❌ | ❌ | ✅ |
| **JavaScript?** | ❌ | N/A | ✅ | ✅ |
| **Real-time?** | ❌ | ❌ | ✅ | ✅ |
| **Documentação** | Fácil | Oficial | Média | **Nenhuma** |
| **Manutenção** | Baixa | Baixa | Média | **Alta** |
| **Taxa de Bloqueio** | 30% | 10% | 50% | 20% |

---

## 🎯 Por Que TCE-SC Exigiu WebSocket?

### ❌ **HTML Estático NÃO Funciona:**

```python
# TENTATIVA 1: HTML Estático
response = requests.get("https://tcesc.shinyapps.io/painelinfraestrutura")
soup = BeautifulSoup(response.text, "html.parser")
tabela = soup.find("table")  # None - tabela não existe no HTML!
```

**Motivo:** A tabela é **gerada dinamicamente** pelo servidor R após a página carregar.

---

### ❌ **API REST Não Existe:**

```python
# TENTATIVA 2: API REST
response = requests.get("https://tcesc.shinyapps.io/api/municipios/2024")
# 404 Not Found - API não existe!
```

**Motivo:** TCE-SC não disponibiliza API pública documentada.

---

### ❌ **Selenium Seria Possível, Mas:**

```python
# TENTATIVA 3: Selenium (funciona, mas...)
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://tcesc.shinyapps.io/painelinfraestrutura")
time.sleep(30)  # Aguardar JavaScript carregar
tabela = driver.find_element(By.ID, "tabela")
# ✅ Funciona, mas demora 30+ segundos
```

**Problemas:**
- ⏱️ **Muito lento:** 30-60 segundos por requisição
- 💾 **Alto consumo:** ~500MB RAM por instância
- 🖥️ **Difícil em servidor:** Requer GUI ou headless
- 🔧 **Manutenção:** Quebra com updates do Chrome

---

### ✅ **WebSocket É a Solução Ideal:**

```python
# SOLUÇÃO: WebSocket
ws = websocket.create_connection("wss://tcesc.shinyapps.io/...")
ws.send(init_message)  # Envia filtros
data = extract_from_response(ws.recv())  # Recebe dados
# ✅ Funciona em 15-20 segundos, 100MB RAM
```

**Vantagens:**
- ⚡ **Mais rápido:** 15-20s vs 30-60s do Selenium
- 💾 **Menos recursos:** 100MB vs 500MB
- 🖥️ **Funciona em servidor:** Sem GUI necessária
- 🔄 **Protocolo nativo:** Usa a mesma API que o navegador

---

## 🎓 Lições Aprendidas

### 1. **Nem Sempre o Mais Simples Funciona**

```
HTML Estático (simples) → ❌ Não funciona
WebSocket (complexo) → ✅ Única solução viável
```

### 2. **Engenharia Reversa É Uma Habilidade**

Para criar o scraper WebSocket, foi necessário:
- 🔍 Analisar tráfego de rede (DevTools)
- 📊 Entender protocolo SockJS
- 🧪 Testar hipóteses iterativamente
- 📝 Documentar descobertas

### 3. **Complexidade ≠ Melhor**

Cada abordagem tem seu lugar:
- HTML simples? → Use BeautifulSoup
- API disponível? → Use requests
- SPA complexo? → Use Selenium
- Real-time? → Use WebSocket

**A melhor solução é a mais simples que resolve o problema.**

---

## 📚 Referências e Recursos

### **Documentação Oficial:**
- [Requests](https://requests.readthedocs.io/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Selenium](https://selenium-python.readthedocs.io/)
- [websocket-client](https://websocket-client.readthedocs.io/)

### **Tutoriais:**
- [Web Scraping with Python](https://realpython.com/python-web-scraping-practical-introduction/)
- [SockJS Protocol](https://github.com/sockjs/sockjs-protocol)
- [Shiny Server Architecture](https://shiny.rstudio.com/)

### **Ferramentas:**
- [DevTools Network Tab](https://developer.chrome.com/docs/devtools/)
- [Postman](https://www.postman.com/) → Testar APIs
- [curl](https://curl.se/) → Debugar requests

---

## 🎬 Fluxograma de Decisão

```
Preciso fazer scraping de um site
           ↓
    Tem API pública?
        ├─ SIM → Use requests + API REST
        └─ NÃO ↓
           ↓
    HTML estático (View Source)?
        ├─ SIM → Use requests + BeautifulSoup
        └─ NÃO ↓
           ↓
    Dados após JavaScript carregar?
        ├─ SIM (simples) → Use Selenium
        └─ NÃO ↓
           ↓
    Aplicação real-time (WebSocket)?
        └─ SIM → Use websocket-client
                 (requer engenharia reversa)
```

---

## 💡 Dicas Finais

### **Para Aprender Web Scraping:**

1. **Comece com o simples:** BeautifulSoup em sites estáticos
2. **Entenda HTTP:** Como funcionam GET, POST, headers, cookies
3. **Estude DevTools:** Network tab é seu melhor amigo
4. **Respeite robots.txt:** Ética em scraping
5. **Implemente rate limiting:** Não sobrecarregue servidores

### **Para Apresentar:**

- ✅ Mostre a **tabela comparativa**
- ✅ Use **exemplos de código** reais
- ✅ Destaque **por que cada abordagem falhou**
- ✅ Explique o **fluxo de decisão**
- ✅ Demonstre **complexidade visualmente** (linhas de código)

---

**📍 Material Desenvolvido para:** Projeto Integrador V  
**📅 Última Atualização:** Maio 2026  
**👤 Autor:** Adriano Cavalcante  
**🎯 Propósito:** Material educacional e de apresentação

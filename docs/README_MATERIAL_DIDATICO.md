# 📚 Material Didático - IQESC TCE-SC

## 🎯 Propósito

Este diretório contém **material educacional** para compreender:

1. **Teoria do IQESC** - Metodologia de cálculo e distribuição
2. **Web Scraping Avançado** - Técnicas para plataformas complexas
3. **Arquitetura do Sistema** - Como tudo se conecta

---

## 📁 Arquivos Disponíveis

### 1. **TEORIA_E_METODOLOGIA.md**

**📖 Documento Completo sobre o Projeto**

**Conteúdo:**
- ✅ O que é o IQESC e sua importância
- ✅ Fundamento legal (Constituição SC, leis)
- ✅ Metodologia de cálculo dos 6 indicadores
- ✅ Fórmula de distribuição do ICMS Educacional
- ✅ Teoria de web scraping
- ✅ Comparação entre tipos de scraping
- ✅ Arquitetura do sistema

**Ideal para:**
- 📊 Apresentações
- 📝 Relatórios acadêmicos
- 🎓 Material de estudo
- 🗣️ Explicação para não-técnicos

**Como usar:**
```bash
# Visualizar no navegador
start docs/TEORIA_E_METODOLOGIA.md

# Ou usar um visualizador Markdown
code docs/TEORIA_E_METODOLOGIA.md
```

---

### 2. **scraping_didatico.py**

**🐍 Script de Scraping Comentado**

**Características:**
- ✅ **80+ comentários explicativos**
- ✅ **Dividido em 8 etapas claras**
- ✅ **Docstrings completas** em cada função
- ✅ **Progresso visual** no terminal
- ✅ **Emojis** para facilitar leitura
- ✅ **Debug logs** para aprendizado

**Estrutura:**
```python
# 1. IMPORTAÇÕES E CONFIGURAÇÕES
# 2. CONSTANTES DO PROJETO
# 3. FUNÇÕES AUXILIARES
# 4. ETAPA 1: Obter Worker ID
# 5. ETAPA 2: Obter Token
# 6. ETAPA 3: Conectar WebSocket
# 7. ETAPA 4: Protocolo SockJS
# 8. ETAPA 5: Enviar Filtros
# 9. ETAPA 6: Extrair Nonce
# 10. ETAPA 7: POST DataTables
# 11. ETAPA 8: Salvar Dados
# 12. FUNÇÃO PRINCIPAL
```

**Como usar:**
```bash
# Executar para ano 2024 (padrão)
python docs/scraping_didatico.py

# Executar para outro ano
python docs/scraping_didatico.py 2023
```

**Saída visual:**
```
================================================================================
  🎓 SCRAPING DIDÁTICO - TCE-SC IQESC
================================================================================

  Ano: 2024
  Plataforma: Shiny Server
  Protocolo: WebSocket + SockJS + DataTables
  Complexidade: ⭐⭐⭐⭐ Muito Alta

================================================================================

================================================================================
  [█░░░░░░░] ETAPA 1/8: Obtendo Worker ID
================================================================================
📡 Enviando GET para: https://tcesc.shinyapps.io/painelinfraestrutura
✅ Status Code: 200
📄 Tamanho HTML: 45321 caracteres
🔑 Worker ID encontrado: _w_abc123...

[continua...]
```

---

## 🎓 Como Usar para Apresentação

### **Opção 1: Apresentação Teórica**

1. **Abra o arquivo TEORIA_E_METODOLOGIA.md**
2. **Use as seções como slides:**
   - Introdução ao IQESC (5 min)
   - Metodologia de cálculo (10 min)
   - Web scraping explicado (10 min)
   - Comparação de técnicas (5 min)

3. **Pontos-chave para destacar:**
   - 💰 R$ 350+ milhões distribuídos
   - 📊 6 indicadores educacionais
   - 🌐 Complexidade: WebSocket vs HTML simples
   - ⭐⭐⭐⭐ Muito Alta complexidade técnica

---

### **Opção 2: Demonstração Prática**

1. **Abra o scraping_didatico.py no editor**
2. **Mostre a estrutura modular:**
   ```python
   # Destaque as 8 etapas
   def etapa1_obter_worker_id()
   def etapa2_obter_token()
   # ...
   ```

3. **Execute o script ao vivo:**
   ```bash
   python docs/scraping_didatico.py 2024
   ```

4. **Explique cada etapa conforme aparece:**
   - Worker ID → "Servidor que processará nossos dados"
   - Token → "Senha temporária"
   - WebSocket → "Conexão em tempo real"
   - Nonce → "Segurança anti-replay"

---

### **Opção 3: Comparação Didática**

**Mostre a diferença de complexidade:**

#### **Scraping Simples (Mercado Livre):**
```python
# 5 linhas, 30 segundos
import requests
from bs4 import BeautifulSoup

html = requests.get("https://site.com").text
produtos = BeautifulSoup(html).find_all("div", class_="produto")
```

#### **Scraping TCE-SC:**
```python
# 500+ linhas, 8 etapas complexas
# 1. GET HTML → Worker ID
# 2. GET Token → Autenticação
# 3. WebSocket → Conexão
# 4. SockJS → Handshake
# 5. INIT → Filtros
# 6. Aguardar → Nonce
# 7. POST → Dados
# 8. Salvar → JSON
```

**Impacto visual:** 5 linhas vs 500 linhas!

---

## 🔍 Navegação Rápida

### **Para Estudar a Teoria:**
```bash
# Leia na ordem:
1. TEORIA_E_METODOLOGIA.md (Seção 1-4) → Conceitos
2. TEORIA_E_METODOLOGIA.md (Seção 5) → Scraping
3. scraping_didatico.py → Implementação
```

### **Para Entender o Código:**
```bash
# Leia na ordem:
1. scraping_didatico.py (seções 1-3) → Setup
2. scraping_didatico.py (seções 4-11) → Etapas
3. Execute e veja os logs
```

### **Para Apresentar:**
```bash
# Prepare:
1. TEORIA_E_METODOLOGIA.md → Abra no navegador
2. scraping_didatico.py → Abra no VS Code
3. Terminal → Pronto para executar
```

---

## 📊 Comparativo de Abordagens

### **Tabela Resumo:**

| Critério | HTML Estático | API REST | Selenium | WebSocket (TCE-SC) |
|----------|---------------|----------|----------|-------------------|
| **Complexidade** | ⭐ Baixa | ⭐⭐ Média | ⭐⭐⭐ Alta | ⭐⭐⭐⭐ Muito Alta |
| **Linhas de Código** | ~20 | ~30 | ~50 | ~500 |
| **Tempo de Exec.** | 1-2s | 1-3s | 10-30s | 15-30s |
| **Libs Necessárias** | 2 | 1 | 3 | 4 |
| **Engenharia Reversa** | Não | Não | Não | **Sim** |
| **Autenticação** | Simples | Token | Cookies | Multi-etapa |
| **Quando Usar** | Sites estáticos | APIs públicas | JS pesado | Apps real-time |

---

## 🎬 Roteiro de Apresentação Sugerido

### **Slides 1-3: Contexto (5 min)**
- O que é IQESC?
- Por que é importante?
- Quanto dinheiro envolve?

### **Slides 4-6: Metodologia (10 min)**
- 6 indicadores explicados
- Fórmula de cálculo
- Exemplo prático de distribuição

### **Slides 7-9: Web Scraping (10 min)**
- Tipos de scraping (tabela comparativa)
- Por que TCE-SC é complexo?
- Arquitetura: GET → WebSocket → POST

### **Slides 10-11: Demonstração (10 min)**
- Mostrar código comentado
- Executar script
- Explicar cada etapa

### **Slide 12: Resultados (5 min)**
- Dados obtidos: 288 municípios
- Uso na calculadora
- Impacto do projeto

---

## 💡 Dicas de Apresentação

### **✅ O Que Fazer:**
- Use o **documento Markdown** para conceitos
- Use o **script Python** para código
- **Execute ao vivo** se possível
- Destaque a **diferença de complexidade**
- Mostre os **emojis e progresso** do script

### **❌ O Que Evitar:**
- Não entre em detalhes técnicos demais de WebSocket
- Não mostre TODO o código (500 linhas)
- Não execute se conexão instável
- Não pule a parte da teoria

---

## 🔗 Links Úteis

### **Documentação Oficial:**
- [TCE-SC Painel](https://tcesc.shinyapps.io/painelinfraestrutura)
- [Lei 17.543/2018](http://leis.alesc.sc.gov.br/)
- [Shiny Server Docs](https://shiny.rstudio.com/)

### **Tecnologias:**
- [Python websocket-client](https://pypi.org/project/websocket-client/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Streamlit](https://streamlit.io/)

---

## 📝 Checklist de Apresentação

**Antes da apresentação:**
- [ ] Testar execução do script
- [ ] Abrir TEORIA_E_METODOLOGIA.md no navegador
- [ ] Abrir scraping_didatico.py no VS Code
- [ ] Preparar terminal
- [ ] Testar conexão com TCE-SC

**Durante a apresentação:**
- [ ] Explicar contexto (IQESC)
- [ ] Mostrar cálculos (fórmulas)
- [ ] Comparar tipos de scraping
- [ ] Demonstrar código
- [ ] Executar (se possível)
- [ ] Mostrar resultados

**Backup (se der erro):**
- [ ] Ter screenshots prontos
- [ ] Ter JSON de exemplo
- [ ] Ter logs salvos

---

## 🎓 Para Professores/Avaliadores

Este material foi desenvolvido com foco em:

1. **Didática:** Cada linha de código tem explicação
2. **Progressão:** Do simples ao complexo
3. **Visualização:** Emojis, cores, progresso
4. **Comparação:** Mostra alternativas e por quê esta foi escolhida
5. **Reprodutibilidade:** Código funcional e testado

**Diferenciais do projeto:**
- ✅ Engenharia reversa de protocolo proprietário
- ✅ Manipulação de WebSocket em tempo real
- ✅ Extração de dados não-estruturados
- ✅ Arquitetura modular e escalável
- ✅ Interface web funcional (Streamlit)

---

**📍 Projeto:** Calculadora IQESC - TCE-SC  
**🎓 Curso:** Projeto Integrador V  
**👤 Autor:** Adriano Cavalcante  
**📅 Data:** Maio 2026  
**🔗 GitHub:** [calculadora-icms-edu-sc](https://github.com/AdrianoCavalcante/calculadora-icms-edu-sc)

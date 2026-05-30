# 📚 Documentação do Projeto - Calculadora IQESC

## 📍 Visão Geral

Este diretório contém toda a documentação técnica e didática do projeto de análise e distribuição do ICMS Educacional de Santa Catarina baseado no IQESC (Índice de Qualidade da Educação de Santa Catarina).

---

## 📁 Índice de Documentos

### 🎓 **Material Didático Principal**

#### 1. [TEORIA_E_METODOLOGIA.md](TEORIA_E_METODOLOGIA.md)
**📖 Documento Completo - 1.200+ linhas**

Conteúdo abrangente sobre:
- O que é o IQESC e sua importância
- Fundamento legal (Constituição SC, Lei 17.543/2018)
- Metodologia detalhada dos 6 indicadores (IEO, IPA, IEE, CSE, SCE, IEN)
- Fórmula de cálculo e distribuição do ICMS
- Teoria completa de web scraping
- Arquitetura do sistema

**Ideal para:**
- 📊 Apresentações acadêmicas
- 📝 Relatórios técnicos
- 🎓 Material de estudo
- 🗣️ Explicação para não-técnicos

---

#### 2. [scraping_didatico.py](scraping_didatico.py)
**🐍 Script Comentado - 500+ linhas**

Implementação educacional do scraper com:
- 80+ comentários explicativos
- 8 etapas claramente separadas
- Docstrings completas em todas as funções
- Progresso visual com emojis
- Logs detalhados para aprendizado

**Ideal para:**
- 💻 Demonstrações ao vivo
- 🔍 Análise de código
- 🎯 Entendimento de implementação
- 🧪 Experimentos e testes

---

#### 3. [COMPARACAO_TECNICAS_SCRAPING.md](COMPARACAO_TECNICAS_SCRAPING.md)
**🔍 Análise Comparativa - 800+ linhas**

Comparação detalhada de 4 abordagens:
1. HTML Estático (BeautifulSoup)
2. API REST (requests)
3. Selenium (Browser Automation)
4. WebSocket (TCE-SC - nossa solução)

Com exemplos de código, tabelas comparativas e justificativas.

**Ideal para:**
- 📊 Slides de apresentação
- 🎯 Justificar escolha técnica
- 🔬 Discussão de alternativas
- 🎓 Material complementar

---

#### 4. [README_MATERIAL_DIDATICO.md](README_MATERIAL_DIDATICO.md)
**📚 Guia de Uso - Este documento**

Instruções sobre:
- Como usar cada documento
- Roteiro de apresentação sugerido
- Checklist de preparação
- Dicas pedagógicas

---

## 🎯 Como Usar Este Material

### **Para Estudar:**

**Ordem recomendada:**
```
1. TEORIA_E_METODOLOGIA.md (Seções 1-4)
   └─ Entender o conceito de IQESC
   
2. COMPARACAO_TECNICAS_SCRAPING.md
   └─ Ver por que WebSocket foi escolhido
   
3. scraping_didatico.py (Seções 1-3)
   └─ Setup e configurações
   
4. scraping_didatico.py (Seções 4-11)
   └─ Implementação passo a passo
   
5. TEORIA_E_METODOLOGIA.md (Seção 6)
   └─ Arquitetura completa do sistema
```

---

### **Para Apresentar:**

**Setup (5 minutos antes):**
```bash
# 1. Abrir documentos
start TEORIA_E_METODOLOGIA.md          # No navegador
code scraping_didatico.py               # No VS Code

# 2. Preparar terminal
cd "c:\Users\User\Documents\VSC\Facu\Projeto Integrador V\ICMS Educacional SC\tce-sc-infraestrutura"

# 3. Testar scraper (opcional)
python docs/scraping_didatico.py 2024
```

**Roteiro (40 minutos):**
```
[5 min]  Contexto e Importância (TEORIA - Seção 1-2)
[10 min] Metodologia IQESC (TEORIA - Seção 3-4)
[10 min] Comparação de Scraping (COMPARACAO - Todas)
[10 min] Demonstração de Código (scraping_didatico.py)
[5 min]  Resultados e Impacto
```

---

### **Para Desenvolver:**

**Arquivos de referência:**
```python
# Para entender a lógica:
src/calculadora/calculadora_iqesc.py

# Para ver o scraper em produção:
iqesc_scraper_dinamico.py

# Para interface:
app.py
```

---

## 📊 Estatísticas do Projeto

### **Documentação:**
- 📄 4 documentos markdown (~3.000 linhas)
- 🐍 1 script Python didático (500+ linhas)
- 📝 200+ comentários explicativos
- 🎯 80+ seções organizadas

### **Complexidade Técnica:**
- ⭐⭐⭐⭐ Muito Alta (WebSocket + SockJS + DataTables)
- 🔍 Engenharia reversa de protocolo proprietário
- 🌐 8 etapas de scraping
- 🔐 Multi-camadas de autenticação

### **Dados Processados:**
- 📍 288 municípios de Santa Catarina
- 📊 230+ variáveis educacionais por município
- 💰 R$ 350+ milhões distribuídos anualmente
- 🎯 6 indicadores principais (IQESC)

---

## 🎓 Recursos Adicionais

### **Diagramas Visuais:**

#### Fluxo de Scraping:
```
GET HTML → Worker ID
    ↓
GET Token → Autenticação
    ↓
WebSocket → Conexão Real-time
    ↓
SockJS Handshake → Protocolo
    ↓
INIT Message → Filtros
    ↓
Aguardar Resposta → Nonce
    ↓
POST DataTables → Dados
    ↓
JSON (288 municípios)
```

#### Arquitetura do Sistema:
```
┌─────────────────┐
│  TCE-SC Shiny   │ ← Fonte de dados
└────────┬────────┘
         │ scraping_didatico.py
         ▼
┌─────────────────┐
│   cache/ JSON   │ ← Armazenamento
└────────┬────────┘
         │ CalculadoraIQESC
         ▼
┌─────────────────┐
│  Streamlit App  │ ← Interface web
└─────────────────┘
```

---

## 💡 Destaques para Apresentação

### **Pontos-Chave:**

1. **Impacto Financeiro:**
   - 💰 R$ 350+ milhões/ano distribuídos
   - 📊 288 municípios beneficiados
   - 🎯 Incentivo à melhoria educacional

2. **Complexidade Técnica:**
   - ⭐⭐⭐⭐ 4/4 estrelas
   - 🔍 Engenharia reversa necessária
   - 🌐 8 etapas de scraping

3. **Diferencial do Projeto:**
   - ✅ Único scraper funcional do TCE-SC
   - ✅ Interface web completa
   - ✅ Cálculos automáticos de distribuição
   - ✅ Material didático abrangente

---

## 🔗 Links Importantes

### **Projeto:**
- 🌐 [Aplicação Online](https://calculadora-icms-edu-sc-faoiv8xaf58gyrh6d9dhdh.streamlit.app)
- 💻 [Repositório GitHub](https://github.com/AdrianoCavalcante/calculadora-icms-edu-sc)
- 📊 [TCE-SC Painel Original](https://tcesc.shinyapps.io/painelinfraestrutura)

### **Documentação Oficial:**
- 📜 [Lei Estadual 17.543/2018](http://leis.alesc.sc.gov.br/)
- 🏛️ [TCE-SC](http://www.tce.sc.gov.br/)
- 📖 [Resolução TC-0082/2018](http://www.tce.sc.gov.br/)

### **Tecnologias:**
- 🐍 [Python](https://python.org)
- 🌐 [Streamlit](https://streamlit.io)
- 🔌 [websocket-client](https://pypi.org/project/websocket-client/)
- 🍲 [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

---

## 📋 Checklist de Qualidade

### **Documentação:**
- [x] Teoria completa e fundamentada
- [x] Código totalmente comentado
- [x] Comparação de alternativas
- [x] Exemplos práticos
- [x] Fluxogramas e diagramas

### **Código:**
- [x] Modular e organizado
- [x] Docstrings completas
- [x] Tratamento de erros
- [x] Logs informativos
- [x] Debug facilitado

### **Apresentação:**
- [x] Material visual preparado
- [x] Roteiro sugerido
- [x] Exemplos executáveis
- [x] Tabelas comparativas
- [x] Backup de screenshots

---

## 🎬 Estrutura de Apresentação Sugerida

### **Slide 1: Título**
- Calculadora IQESC - TCE-SC
- Análise e Distribuição do ICMS Educacional

### **Slides 2-4: Contexto (5 min)**
- O que é IQESC?
- Por que R$ 350+ milhões?
- Importância da transparência

### **Slides 5-8: Metodologia (10 min)**
- 6 indicadores detalhados
- Fórmula de cálculo
- Exemplo de distribuição
- Potencial de melhoria

### **Slides 9-12: Web Scraping (10 min)**
- Tabela comparativa de técnicas
- Por que WebSocket?
- Arquitetura de 8 etapas
- Fluxograma visual

### **Slides 13-14: Demonstração (10 min)**
- Código comentado
- Execução ao vivo (se possível)
- Progresso visual

### **Slide 15-16: Resultados (5 min)**
- 288 municípios extraídos
- Interface web funcional
- Cálculos automáticos
- Deploy online

### **Slide 17: Conclusão**
- Diferenciais técnicos
- Impacto social
- Material didático

---

## 📞 Suporte

**Desenvolvedor:** Adriano Cavalcante  
**Projeto:** Integrador V  
**Instituição:** [Sua Faculdade]  
**Data:** Maio 2026

**Contato:**
- 💻 GitHub: [@AdrianoCavalcante](https://github.com/AdrianoCavalcante)
- 📧 Email: adrianocavalcante84@gmail.com

---

## 📄 Licença

Este material foi desenvolvido para fins educacionais como parte do Projeto Integrador V.

**Uso permitido:**
- ✅ Estudo e aprendizado
- ✅ Apresentações acadêmicas
- ✅ Referência técnica
- ✅ Adaptação com atribuição

**Uso não permitido:**
- ❌ Comercialização
- ❌ Plágio sem atribuição
- ❌ Distribuição sem créditos

---

**📍 Última Atualização:** Maio 2026  
**📌 Versão da Documentação:** 1.0  
**🎯 Status:** Completo e revisado

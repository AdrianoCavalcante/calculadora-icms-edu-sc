# 📊 Calculadora IQESC - Análise de Indicadores Educacionais SC

> **Sistema completo de análise dos indicadores IQESC com interface web e cálculos de repasse financeiro do ICMS Educacional**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.58.0-FF4B4B.svg)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![TCE-SC](https://img.shields.io/badge/Dados-TCE--SC-green.svg)](https://tcesc.shinyapps.io/iqesc_2024/)

---

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em: **http://localhost:8501**

✅ **Pronto!** Os dados de 2024 já estão em cache e serão carregados automaticamente.

---

## 🎯 Funcionalidades

### 📈 **Análise Completa por Município**
- **IQESC** e todos os 6 indicadores detalhados
- **Ranking estadual** com posicionamento
- **Comparação com média** de Santa Catarina
- **Pontos fortes** e **pontos de atenção**
- **Recomendações estratégicas** personalizadas

### 💰 **Cálculos Financeiros de Repasse ICMS**
- Informe o **montante total anual** do ICMS Educacional
- Calcule automaticamente:
  - **Repasse atual** baseado no IQESC do município
  - **Repasse potencial** se atingir IQESC máximo (1.0)
  - **Gap financeiro** (diferença entre atual e potencial)
  - **Percentual de distribuição** do município no total estadual

### 🏆 **Rankings Personalizados**
- Ordene por qualquer indicador (IQESC, IEO, IPA, IEE, etc)
- Escolha quantos municípios exibir (Top 10, 20, 50, ou todos)
- Visualização em tabela interativa

### 📊 **Estatísticas Gerais**
- Visão panorâmica de Santa Catarina
- Média, mediana, desvio padrão de cada indicador
- Valores máximos e mínimos por indicador

### 💾 **Exportação de Dados**
- **CSV** para análise em Excel/planilhas
- **JSON** com estrutura completa e metadados
- **Relatórios em TXT** para download

---

## 📦 Estrutura do Projeto

```
tce-sc-infraestrutura/
├── app.py                          # 🌟 Interface Streamlit principal
```
tce-sc-infraestrutura/
├── app.py                          # 🌟 Interface Streamlit principal
├── iniciar_app.bat                 # Atalho Windows
│
├── src/                            # 📦 Código-fonte e scripts
│   ├── __init__.py
│   ├── iqesc_scraper_dinamico.py   # Scraper automático TCE-SC
│   ├── testar_sistema.py           # Script de testes
│   └── calculadora/
│       ├── __init__.py
│       └── calculadora_iqesc.py    # Motor de cálculos e análises
│
├── cache/
│   └── iqesc_2024/                 # Dados em cache (288 municípios)
│       ├── dados.json              # Indicadores de todos os municípios
│       ├── colunas.json            # Nomes das colunas
│       └── metadata.json           # Metadados e timestamp
│
├── docs/                           # 📚 Documentação completa
│   ├── EXEMPLO_RELATORIO.md        # Exemplo de relatório gerado
│   ├── TROUBLESHOOTING_DEPENDENCIAS.md  # Guia de problemas
│   ├── CORRECAO_NUMPY_PANDAS.md    # Histórico de correções
│   └── RELATORIO_LIMPEZA.md        # Relatório de organização
│
├── requirements.txt                # Dependências do projeto
├── README.md                       # Este arquivo
├── README_APP.md                   # Documentação detalhada da aplicação
├── GUIA_RAPIDO.md                  # Tutorial de uso
└── CHANGELOG.md                    # Histórico de versões
```

---

## 📊 Dados e Indicadores

O sistema trabalha com os seguintes indicadores oficiais do TCE-SC:

| Indicador | Nome Completo | Faixa | Descrição |
|-----------|---------------|-------|-----------|
| **IQESC** | Índice de Qualidade da Educação SC | 0-1 | Índice geral (composição dos demais) |
| **IEO** | Índice de Esforço Observado | 0-1 | Esforço observável na gestão educacional |
| **IPA** | Índice de Proficiência Avaliada | 0-1 | Desempenho dos alunos nas avaliações |
| **IEE** | Índice de Esforço Escolar | 0-1 | Esforço da rede municipal de ensino |
| **IEN** | Índice de Esforço Não Observado | 0-1 | Fatores não diretamente observáveis |
| **CSE** | Contexto Socioeconômico | 0-1 | Contexto social e econômico dos estudantes |
| **SCE** | Sistema de Custos das Escolas | 0-1 | Eficiência na gestão de custos |

**Fonte oficial**: [TCE-SC - IQESC 2024](https://tcesc.shinyapps.io/iqesc_2024/)

**Dados disponíveis**: 288 municípios de Santa Catarina

---

## 💻 Interface da Aplicação

### 📋 **Aba 1: Análise por Município**
- Seleção de município via dropdown (busca instantânea)
- 4 métricas principais no topo:
  - IQESC atual + distância para o máximo
  - Aproveitamento percentual + classificação
  - Ranking estadual + total de municípios
  - Comparação com média estadual
- **Seção de Repasse Financeiro** (se montante ICMS informado):
  - Repasse Atual (R$)
  - Repasse Potencial (R$)
  - Gap Financeiro (R$ e %)
  - % da Distribuição estadual
- Indicadores detalhados com barras de progresso
- Pontos fortes e fracos destacados
- Recomendações estratégicas personalizadas
- Geração e download de relatório completo em TXT

### 🏆 **Aba 2: Rankings**
- Escolha o indicador para ordenação
- Defina quantidade de municípios (Top 10, 20, 50, todos)
- Tabela interativa com todos os indicadores

### 📊 **Aba 3: Estatísticas Gerais**
- Visão panorâmica de Santa Catarina
- Total de municípios analisados
- Estatísticas por indicador:
  - Média estadual
  - Mediana
  - Desvio padrão
  - Valores mínimos e máximos

### 💾 **Aba 4: Exportar Dados**
- Exportação em CSV (compatível com Excel)
- Exportação em JSON (estrutura completa)
- Download direto pela interface

---

## ⚙️ Configurações da Aplicação

### **Barra Lateral (Sidebar)**

**Ano de Referência:**
- Atualmente: **2024** (dados em cache)
- Input numérico para fácil alteração

**Montante Total ICMS Educacional:**
- Informe o valor anual em Reais (R$)
- Usado para cálculos de repasse financeiro
- Deixe em 0 para desabilitar cálculos financeiros

**Forçar Atualização:**
- Botão para baixar dados atualizados do TCE-SC
- Ignora cache local existente
- Útil para garantir dados mais recentes

**Visão Geral:**
- Total de municípios carregados
- IQESC médio de SC
- IQESC máximo e mínimo

---

## 🔧 Uso Avançado

### Atualizar Dados Manualmente

Para baixar novos dados diretamente do TCE-SC:

```bash
python iqesc_scraper_dinamico.py 2024 --force-update
```

Ou use o botão **"🔄 Forçar Atualização de Dados"** na interface.

### Usar a Calculadora Programaticamente

```python
from src.calculadora.calculadora_iqesc import CalculadoraIQESC

# Criar calculadora com montante ICMS
calc = CalculadoraIQESC(
    ano=2024,
    montante_total_icms=500000000.00  # R$ 500 milhões
)

# Analisar município
analise = calc.analisar_municipio("Florianópolis")

print(f"IQESC: {analise['municipio']['iqesc']:.4f}")
print(f"Ranking: {analise['ranking']['posicao']}º")

# Se montante foi informado, ver repasse financeiro
if 'repasse_financeiro' in analise:
    rep = analise['repasse_financeiro']
    print(f"Repasse Atual: R$ {rep['repasse_atual']:,.2f}")
    print(f"Gap Financeiro: R$ {rep['gap_financeiro']:,.2f}")

# Gerar relatório completo
relatorio = calc.gerar_relatorio_completo("Florianópolis")
print(relatorio)
```

---

## �️ Comandos Úteis

### Executar a Aplicação
```bash
streamlit run app.py
```
Ou use o atalho Windows: **`iniciar_app.bat`**

### Atualizar Dados do TCE-SC
```bash
python src/iqesc_scraper_dinamico.py 2024 --force-update
```

### Testar o Sistema
```bash
python src/testar_sistema.py
```

### Instalar Dependências
```bash
pip install -r requirements.txt
```

### Verificar Estrutura do Projeto
```bash
tree /F /A
```

### Limpar Cache Python
```bash
python -c "import shutil; shutil.rmtree('__pycache__', ignore_errors=True); shutil.rmtree('src/__pycache__', ignore_errors=True)"
```

---

## ☁️ Deploy Online (Streamlit Cloud)

### 🌐 Acesso Online + Offline

Este projeto funciona tanto **online** quanto **offline**:

- **🌐 Online**: Deploy gratuito no Streamlit Community Cloud
- **💻 Offline**: Execução local com `streamlit run app.py`

### 🚀 Deploy no Streamlit Cloud

**Guia completo**: [docs/DEPLOY_STREAMLIT_CLOUD.md](docs/DEPLOY_STREAMLIT_CLOUD.md)

**Resumo rápido:**

1. **Criar conta** no [Streamlit Cloud](https://share.streamlit.io)
2. **Conectar** ao seu repositório GitHub
3. **Configurar** deploy: `app.py` como arquivo principal
4. **Deploy automático** - pronto em minutos!

**Vantagens:**
- ✅ Acessível de qualquer lugar
- ✅ Compartilhável via link
- ✅ HTTPS gratuito
- ✅ Deploy automático a cada commit
- ✅ Funciona offline também

### 📦 Arquivos de Deploy

```
.streamlit/
└── config.toml          # Configurações do Streamlit Cloud

cache/
└── .gitkeep             # Estrutura do cache (dados baixados automaticamente)

.gitignore               # Cache não vai para GitHub
requirements.txt         # Dependências com versões fixadas
```

**Cache inteligente:**
- Não vai para o GitHub (`.gitignore`)
- Criado automaticamente na primeira execução online
- Funciona offline se cache já existir

---

## 📖 Documentação Adicional

- **[docs/DEPLOY_STREAMLIT_CLOUD.md](docs/DEPLOY_STREAMLIT_CLOUD.md)** - 🚀 Guia completo de deploy online
- **[README_APP.md](README_APP.md)** - Documentação completa da aplicação Streamlit
- **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** - Tutorial passo a passo para iniciantes
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões e mudanças

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **Streamlit 1.58.0** - Interface web interativa
- **Requests** - Cliente HTTP para scraping
- **BeautifulSoup4** - Parsing de HTML
- **WebSocket-Client** - Comunicação com Shiny apps
- **JSON** - Armazenamento de dados estruturados

---

## 🤝 Contribuindo

Este é um projeto educacional. Sugestões e melhorias são bem-vindas!

---

## 📞 Informações

**Desenvolvido para**: Análise de indicadores educacionais de Santa Catarina  
**Fonte de dados**: Tribunal de Contas do Estado de Santa Catarina (TCE-SC)  
**Ano de referência**: 2024  
**Última atualização**: 30 de maio de 2026

---

**🎓 Projeto Integrador V - Análise IQESC**

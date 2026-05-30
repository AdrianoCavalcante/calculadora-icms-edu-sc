# 📊 Calculadora e Visualizador IQESC

## 🎯 Visão Geral

Sistema completo para **extração, análise e visualização** dos indicadores educacionais IQESC (Índice de Qualidade da Educação de SC) do Tribunal de Contas do Estado de Santa Catarina.

### ✨ Funcionalidades

- 🔄 **Scraper Dinâmico** - Extração automática de dados do TCE-SC
- 📊 **Calculadora Analítica** - Processamento e análise dos indicadores
- 🖥️ **Interface Web Interativa** - Visualização com Streamlit
- 💾 **Sistema de Cache** - Armazenamento local para uso offline
- 📁 **Exportação** - CSV e JSON para análises externas

---

## 🚀 Início Rápido

### 1️⃣ Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ Extrair Dados (Primeira Vez)

```bash
# Baixar dados do ano desejado
python iqesc_scraper_dinamico.py 2024
```

### 3️⃣ Iniciar Interface

**Opção A - Duplo Clique (Mais Fácil):**
```
Duplo clique em: iniciar_app.bat
```

**Opção B - Linha de Comando:**
```bash
streamlit run app.py
```

A interface abrirá automaticamente em: **http://localhost:8501**

---

## 📖 Guia de Uso

### 🔄 Scraper Dinâmico

O scraper extrai dados diretamente do painel oficial do TCE-SC com cache inteligente:

```bash
# Uso básico (verifica cache, atualiza se necessário)
python iqesc_scraper_dinamico.py 2024

# Forçar atualização (ignora cache)
python iqesc_scraper_dinamico.py 2024 --force-update

# Modo offline (apenas cache)
python iqesc_scraper_dinamico.py 2024 --offline

# Diretório de cache customizado
python iqesc_scraper_dinamico.py 2024 --cache-dir meu_cache
```

**Estrutura do Cache:**
```
cache/
└── iqesc_2024/
    ├── dados.json      # Dados completos dos municípios
    ├── colunas.json    # Nomes das colunas
    └── metadata.json   # Informações estruturais
```

### 📊 Calculadora (Uso Programático)

```python
from src.calculadora.calculadora_iqesc import CalculadoraIQESC

# Inicializar
calc = CalculadoraIQESC(ano=2024)

# Listar municípios
municipios = calc.listar_municipios()

# Análise detalhada
analise = calc.analisar_municipio("Florianópolis")

# Relatório completo
relatorio = calc.gerar_relatorio_completo("Florianópolis")
print(relatorio)

# Estatísticas gerais
stats = calc.calcular_estatisticas_gerais()

# Rankings
top10 = calc.ranking_municipios(top_n=10, por='iqesc')

# Exportações
calc.exportar_todos_csv("resultado.csv")
calc.exportar_todos_json("resultado.json")
```

### 🖥️ Interface Web

A interface Streamlit oferece 4 abas principais:

#### 🏛️ Aba 1: Análise por Município

- **Seleção de município** com busca inteligente
- **Métricas principais:**
  - IQESC Atual
  - Aproveitamento (%)
  - Ranking Estadual
  - Comparação com Média
- **Indicadores detalhados:**
  - IEO - Esforço Observado
  - IPA - Proficiência Avaliada
  - IEE - Esforço Escolar
  - IEN - Esforço Não Observado
  - CSE - Contexto Socioeconômico
  - SCE - Sistema de Custos
- **Pontos fortes** (Top 3 indicadores)
- **Pontos de atenção** (3 indicadores mais fracos)
- **Recomendações estratégicas** personalizadas
- **Relatório completo** para download (.txt)

#### 🏆 Aba 2: Rankings

- **Ordenação flexível** por qualquer indicador
- **Quantidade customizável** (5 a 100 municípios)
- **Visualização em tabela** com todos os indicadores
- **Pódio destacado** (Top 3)

#### 📊 Aba 3: Estatísticas Gerais

- **Estatísticas do IQESC:**
  - Média, Mediana, Máximo, Mínimo
  - Desvio Padrão
- **Estatísticas por indicador:**
  - Média, Máximo, Mínimo de cada componente

#### 💾 Aba 4: Exportar Dados

- **CSV** - Formato compacto para planilhas
- **JSON** - Formato completo com metadados
- **Download direto** pelo navegador

---

## 📊 Indicadores IQESC

### Índice Final

**IQESC** - Índice de Qualidade da Educação de SC (0-1)
- Indicador agregado que combina todos os componentes
- Representa a qualidade geral da educação municipal

### Componentes

1. **IEO - Indicador de Esforço Observado**
   - Combina proficiência e esforço escolar
   - Subcomponentes:
     - **IPA** - Indicador de Proficiência Avaliada
     - **IEE** - Indicador de Esforço Escolar

2. **IEN - Indicador de Esforço Não Observado**
   - Fatores não diretamente observáveis

3. **CSE - Contexto Socioeconômico**
   - Condições sociais e econômicas do município

4. **SCE - Sistema de Custos das Escolas**
   - Gestão e eficiência de custos educacionais

### Classificação de Desempenho

| Aproveitamento | Classificação |
|----------------|---------------|
| ≥ 90% | 🟢 EXCELENTE |
| 80-89% | 🟢 MUITO BOM |
| 70-79% | 🟡 BOM |
| 60-69% | 🟡 REGULAR |
| 50-59% | 🟠 ABAIXO DA MÉDIA |
| < 50% | 🔴 CRÍTICO |

---

## 📂 Estrutura do Projeto

```
tce-sc-infraestrutura/
│
├── app.py                          # Interface Streamlit principal
├── iniciar_app.bat                 # Script de inicialização rápida
├── iqesc_scraper_dinamico.py       # Scraper com cache e validação
├── requirements.txt                # Dependências Python
│
├── src/
│   ├── calculadora/
│   │   ├── calculadora_iqesc.py    # Motor de análise
│   │   └── analisador_iqesc.py     # Analisador básico (legacy)
│   │
│   ├── scrapers/
│   │   └── scraper_iqesc.py        # Scraper básico (legacy)
│   │
│   └── utils/
│       └── ...
│
├── cache/                          # Cache de dados (criado automaticamente)
│   └── iqesc_XXXX/
│       ├── dados.json
│       ├── colunas.json
│       └── metadata.json
│
├── data/                           # Dados e exportações
│
└── docs/                           # Documentação adicional
```

---

## 🔧 Resolução de Problemas

### ❌ Erro: "Dados não encontrados"

**Causa:** Cache não existe ou está vazio

**Solução:**
```bash
python iqesc_scraper_dinamico.py 2024
```

### ❌ Erro: "Sem conexão"

**Causa:** Site TCE-SC indisponível ou sem internet

**Solução:**
```bash
# Use modo offline (requer cache existente)
python iqesc_scraper_dinamico.py 2024 --offline
```

### ❌ Erro: "ModuleNotFoundError: streamlit"

**Causa:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

### ⚠️ Cache Desatualizado

**Sintoma:** Mensagem "Cache antigo (X dias)"

**Solução:**
```bash
# Forçar atualização
python iqesc_scraper_dinamico.py 2024 --force-update
```

---

## 📈 Exemplos de Análise

### Exemplo 1: Relatório Individual

```python
from src.calculadora.calculadora_iqesc import CalculadoraIQESC

calc = CalculadoraIQESC(2024)
relatorio = calc.gerar_relatorio_completo("Florianópolis")

print(relatorio)
```

**Saída:**
```
================================================================================
📊 RELATÓRIO COMPLETO IQESC - FLORIANÓPOLIS
================================================================================
ANO: 2024 | Fonte: TCE-SC

────────────────────────────────────────────────────────────────────────────────
📈 ÍNDICE IQESC
────────────────────────────────────────────────────────────────────────────────
   IQESC Atual................: 0.8542
   IQESC Máximo Possível......: 1.0000
   Aproveitamento.............: 85.4%
   Classificação..............: 🟢 MUITO BOM
   Gap de Melhoria............: 0.1458 pontos
...
```

### Exemplo 2: Top 10 Estadual

```python
calc = CalculadoraIQESC(2024)
top10 = calc.ranking_municipios(top_n=10)

for i, m in enumerate(top10, 1):
    print(f"{i}º - {m['nome']}: {m['iqesc']:.4f}")
```

### Exemplo 3: Exportação Completa

```python
calc = CalculadoraIQESC(2024)

# CSV para Excel/Planilhas
calc.exportar_todos_csv("analise_sc_2024.csv")

# JSON para análises programáticas
calc.exportar_todos_json("analise_sc_2024.json")
```

---

## 🔄 Workflow Completo

```
┌─────────────────────┐
│  1. Extração        │
│  (Scraper)          │
│  iqesc_scraper_     │
│  dinamico.py        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  2. Cache           │
│  cache/iqesc_XXXX/  │
│  - dados.json       │
│  - metadata.json    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  3. Processamento   │
│  (Calculadora)      │
│  calculadora_       │
│  iqesc.py           │
└──────┬──────────────┘
       │
       ├──────────────────┐
       │                  │
       ▼                  ▼
┌─────────────┐    ┌──────────────┐
│  4a. CLI    │    │  4b. Web UI  │
│  Terminal   │    │  (Streamlit) │
│  Python     │    │  app.py      │
└─────────────┘    └──────────────┘
       │                  │
       └────────┬─────────┘
                ▼
        ┌───────────────┐
        │  5. Saídas    │
        │  - Relatórios │
        │  - CSV/JSON   │
        │  - Análises   │
        └───────────────┘
```

---

## 🎓 Casos de Uso

### 1. Gestor Municipal

**Objetivo:** Entender performance educacional do município

**Workflow:**
1. Abrir `app.py`
2. Selecionar ano e município
3. Analisar métricas e recomendações
4. Baixar relatório completo

### 2. Pesquisador

**Objetivo:** Análise comparativa de múltiplos municípios

**Workflow:**
1. Extrair dados: `python iqesc_scraper_dinamico.py 2024`
2. Exportar: Aba "Exportar Dados" → JSON/CSV
3. Importar em ferramentas estatísticas (R, Python, SPSS)

### 3. Jornalista

**Objetivo:** Matéria sobre educação em SC

**Workflow:**
1. Abrir `app.py`
2. Aba "Rankings" → Top 10 e Bottom 10
3. Aba "Estatísticas Gerais" → Contexto estadual
4. Exportar dados para infográficos

### 4. Desenvolvedor

**Objetivo:** Integrar com outro sistema

**Workflow:**
```python
from src.calculadora.calculadora_iqesc import CalculadoraIQESC

calc = CalculadoraIQESC(2024)
dados = calc.dados_processados

# Integrar com API, dashboard, etc.
```

---

## 🆕 Novidades vs Versão Anterior

### ✅ Melhorias

- ✨ **Interface Streamlit completa** (antes: apenas CLI)
- 🔄 **Cache inteligente** com validação automática
- 📊 **Análises estatísticas** avançadas
- 🏆 **Rankings flexíveis** por qualquer indicador
- 💾 **Exportação aprimorada** (CSV + JSON completo)
- 📱 **Design responsivo** e intuitivo
- 🎯 **Recomendações automáticas** personalizadas

### 🔧 Correções

- ✅ Compatibilidade com estrutura dinâmica do site
- ✅ Validação de dados antes do scraping
- ✅ Fallback automático para cache
- ✅ Tratamento robusto de erros

---

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique a seção **Resolução de Problemas**
2. Consulte a documentação em `/docs`
3. Revise os logs de erro no terminal

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e de pesquisa.

**Dados:** Tribunal de Contas do Estado de Santa Catarina (TCE-SC)  
**Fonte Oficial:** https://tcesc.shinyapps.io/iqesc_2024/

---

## 🙏 Créditos

- **TCE-SC** - Fonte de dados oficial
- **Streamlit** - Framework de interface web
- **Python** - Linguagem de desenvolvimento

---

**Última Atualização:** 30/05/2026  
**Versão:** 2.0

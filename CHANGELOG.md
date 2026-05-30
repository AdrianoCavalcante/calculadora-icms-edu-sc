# 📝 CHANGELOG - Calculadora IQESC

Todas as mudanças notáveis do projeto estão documentadas neste arquivo.

---

## [3.2.0] - 2026-05-30

### 🚀 Preparação para Deploy Online (Streamlit Cloud)

**Objetivo:** Habilitar deploy no Streamlit Community Cloud mantendo compatibilidade offline

#### **Problema a Resolver:**
- Usuário quer acesso online (Streamlit Cloud)
- Mas precisa manter funcionalidade offline
- Cache não pode ir para GitHub (arquivos grandes)

#### **Solução Implementada:**

**1. Configuração Streamlit Cloud:**
- Criado `.streamlit/config.toml` com tema e configurações
- Cache inteligente: não vai para GitHub, criado automaticamente

**2. Preparação Git:**
- Atualizado `.gitignore` para excluir `cache/`
- Criado `cache/.gitkeep` para manter estrutura
- Mantém cache local para uso offline

**3. Documentação Completa:**
- `GITHUB_SETUP.md` - Guia passo a passo para subir no GitHub
- `docs/DEPLOY_STREAMLIT_CLOUD.md` - Guia completo de deploy online
- `README.md` - Seção sobre deploy e uso híbrido

**4. Funcionamento Híbrido:**
```
🌐 Online (Streamlit Cloud):
  → Download automático na 1ª execução
  → Cache criado dinamicamente
  → Compartilhável via link

💻 Offline (Localhost):
  → Usa cache existente se disponível
  → Funciona sem internet (com cache)
  → Download só se necessário
```

#### **Estrutura de Deploy:**
```
.streamlit/
└── config.toml          # Configurações Streamlit Cloud

cache/
└── .gitkeep             # Mantém estrutura (dados não vão pro GitHub)

.gitignore               # Exclui cache/, __pycache__, etc

requirements.txt         # Dependências com versões fixadas
GITHUB_SETUP.md          # Guia de setup GitHub
docs/DEPLOY_STREAMLIT_CLOUD.md  # Guia de deploy online
```

#### **Arquivos Criados:**
- `.streamlit/config.toml` - Configuração tema e servidor
- `cache/.gitkeep` - Estrutura do cache (vazio)
- `GITHUB_SETUP.md` - Guia completo Git + GitHub
- `docs/DEPLOY_STREAMLIT_CLOUD.md` - Guia deploy Streamlit Cloud

#### **Arquivos Atualizados:**
- `.gitignore` - Adicionado `cache/` e mantido `.gitkeep`
- `README.md` - Seção de deploy online/offline

#### **Benefícios:**
✅ **Deploy gratuito** no Streamlit Cloud  
✅ **Acessível de qualquer lugar** via link  
✅ **Mantém versão offline** funcionando  
✅ **Cache inteligente** - criado automaticamente online  
✅ **Compartilhável** - envie o link para qualquer pessoa  
✅ **Deploy automático** - push → deploy automático  
✅ **HTTPS incluído** - seguro por padrão  

#### **Como Usar:**

**1. Subir para GitHub:**
```bash
# Seguir guia completo
cat GITHUB_SETUP.md

# Resumo rápido
git init
git add .
git commit -m "🎉 Initial commit"
git remote add origin https://github.com/SEU_USUARIO/calculadora-iqesc-sc.git
git push -u origin main
```

**2. Deploy no Streamlit Cloud:**
```
1. Acessar share.streamlit.io
2. Conectar repositório GitHub
3. Configurar: app.py como main file
4. Deploy! (automático em ~3 min)
```

**3. Usar Offline:**
```bash
streamlit run app.py
# Funciona normalmente com cache local
```

#### **Documentação:**
📚 [GITHUB_SETUP.md](GITHUB_SETUP.md) - Guia Git + GitHub  
🚀 [docs/DEPLOY_STREAMLIT_CLOUD.md](docs/DEPLOY_STREAMLIT_CLOUD.md) - Deploy online  
📖 [README.md](README.md) - Documentação geral  

---

## [3.1.3] - 2026-05-30

### 📁 Consolidação Final da Estrutura

**Objetivo:** Eliminar redundância de diretórios - consolidar tudo em `src/`

#### **Problema Identificado:**
- Duas pastas separadas: `src/` e `scripts/`
- Causava confusão sobre onde colocar novos arquivos
- Estrutura redundante e menos intuitiva

#### **Solução:**
Consolidação completa em `src/`:
- Movido `scripts/iqesc_scraper_dinamico.py` → `src/iqesc_scraper_dinamico.py`
- Movido `scripts/testar_sistema.py` → `src/testar_sistema.py`
- Removido diretório `scripts/`

#### **Estrutura Final:**
```
src/
├── __init__.py
├── iqesc_scraper_dinamico.py       # Scraper TCE-SC
├── testar_sistema.py               # Testes
└── calculadora/                     # Módulo de cálculos
    ├── __init__.py
    └── calculadora_iqesc.py
```

#### **Arquivos Atualizados:**
- `app.py` - Caminho do scraper: `src/iqesc_scraper_dinamico.py`
- `README.md` - Estrutura e comandos atualizados

#### **Novos Comandos:**
```bash
# Scraper
python src/iqesc_scraper_dinamico.py 2024

# Testes
python src/testar_sistema.py
```

#### **Benefícios:**
✅ **Um único diretório** para todo código Python  
✅ **Estrutura mais limpa** e pythônica  
✅ **Menos confusão** sobre organização  
✅ **Mais fácil de navegar** e manter  
✅ **Padrão Python** - todo código em `src/`  

---

## [3.1.2] - 2026-05-30

### 📁 Reorganização da Estrutura

**Objetivo:** Consolidar scripts e documentação em diretórios únicos

#### **Mudanças:**

1. **Scripts organizados em `scripts/`:**
   - Movido `iqesc_scraper_dinamico.py` → `scripts/iqesc_scraper_dinamico.py`
   - Movido `testar_sistema.py` → `scripts/testar_sistema.py`
   - Mantido `app.py` na raiz (necessário para Streamlit)

2. **Documentação consolidada em `docs/`:**
   - Movido `RELATORIO_LIMPEZA.md` → `docs/RELATORIO_LIMPEZA.md`
   - Todos os documentos técnicos agora em um único diretório

3. **Limpeza de arquivos temporários:**
   - Removidos arquivos `1.24.0` e `2.0.0` (resíduos de versão)

#### **Arquivos Atualizados:**
- `app.py` - Referências ao scraper atualizadas para `scripts/`
- `README.md` - Estrutura do projeto e comandos atualizados

#### **Estrutura Final:**
```
tce-sc-infraestrutura/
├── app.py                          # Interface Streamlit
├── scripts/                        # 📜 Scripts auxiliares
│   ├── iqesc_scraper_dinamico.py
│   └── testar_sistema.py
├── src/calculadora/                # Código-fonte
├── cache/iqesc_2024/               # Dados locais
└── docs/                           # 📚 Documentação completa
    ├── EXEMPLO_RELATORIO.md
    ├── TROUBLESHOOTING_DEPENDENCIAS.md
    ├── CORRECAO_NUMPY_PANDAS.md
    └── RELATORIO_LIMPEZA.md
```

#### **Benefícios:**
✅ Estrutura mais organizada e profissional  
✅ Scripts agrupados logicamente  
✅ Documentação centralizada  
✅ Facilita navegação e manutenção  
✅ Separação clara entre código principal e utilitários  

---

## [3.1.1] - 2026-05-30

### 🐛 Correção Crítica

**Problema Resolvido:** Incompatibilidade binária NumPy/Pandas

#### **Erro:**
```
ValueError: numpy.dtype size changed, may indicate binary incompatibility. 
Expected 96 from C header, got 88 from PyObject
```

#### **Causa:**
- NumPy 2.0.0 instalado (incompatível com Pandas compilado para NumPy < 2.0)
- Pandas 1.5.3 compilado com versão antiga do NumPy

#### **Solução Aplicada:**
1. Desinstalação completa de NumPy e Pandas
2. Limpeza do cache do pip (4.1 GB removidos)
3. Instalação de versões compatíveis:
   - **NumPy 1.26.4** (< 2.0.0)
   - **Pandas 2.3.3** (>= 2.0.0, compatível com NumPy 1.26.x)

#### **Arquivos Atualizados:**
- `requirements.txt` - Adicionadas restrições de versão específicas:
  ```
  numpy>=1.24.0,<2.0.0
  pandas>=2.0.0,<3.0.0
  ```

#### **Resultado:**
✅ Aplicação Streamlit funciona perfeitamente  
✅ DataFrames renderizam sem erros  
✅ Todas as funcionalidades operacionais  

### 🐛 Correção de Import

**Problema:** `ModuleNotFoundError: No module named 'calculadora.analisador_iqesc'`

#### **Causa:**
- Arquivo `src/calculadora/__init__.py` ainda referenciava `analisador_iqesc.py`
- Arquivo foi removido na limpeza profunda (v3.1.0)
- Import obsoleto causava falha ao iniciar aplicação

#### **Solução:**
- Atualizado `src/calculadora/__init__.py`
- Removida linha: `from .analisador_iqesc import AnalisadorIQESC`
- Mantida apenas: `from .calculadora_iqesc import CalculadoraIQESC`

#### **Resultado:**
✅ Imports funcionando corretamente  
✅ Aplicação inicia sem erros  
✅ Calculadora carrega 288 municípios  
✅ Todas as funcionalidades testadas e operacionais  

---

## [3.1.0] - 2026-05-30

### 🧹 Limpeza Profunda e Otimização Final

**Objetivo:** Remover redundâncias, arquivos obsoletos e otimizar estrutura do projeto.

#### **Arquivos Removidos - 24 itens:**

**Dados Redundantes (4):**
- `iqesc_dados_2024.json` - duplicado de cache/iqesc_2024/dados.json
- `iqesc_column_names_2024.json` - duplicado de cache/iqesc_2024/colunas.json
- `iqesc_analise_completa_2024.json` - análise temporária
- `iqesc_completo_2024.csv` - exportação temporária

**Módulos Obsoletos (5 diretórios):**
- `src/scrapers/` - scrapers antigos (usamos iqesc_scraper_dinamico.py)
  - scraper_iqesc.py, scraper_iqesc_xhr.py, scraper_iqesc_debug.py
  - scraper_infraestrutura.py, __init__.py
- `src/utils/` - módulo vazio sem funcionalidade
- `src/legislacao/` - não usado no projeto atual
  - validador_calculos.py, scraper_legislacao.py, parser_metodologia.py
- `scripts/` - scripts antigos substituídos
  - scraper_simples.py, baixar_multiplos_anos.py, baixar_com_url.py
- `data/` - estrutura vazia (usamos cache/)

**Arquivos Redundantes (3):**
- `src/calculadora/analisador_iqesc.py` - funcionalidade em calculadora_iqesc.py
- `README_IQESC.md` - informações já em README.md
- `PROJETO_ORGANIZADO.md` - documentação consolidada
- `requirements-dev.txt` - dependências de desenvolvimento não essenciais

**Cache de Debug (4):**
- `cache/exploracao_iqesc.json`
- `cache/exploracao_iqesc_mensagens.txt`
- `cache/opcoes_tce_sc.json`
- `cache/teste_endpoint_especifico_resultado.json`

**Documentação Desatualizada (7):**
- `docs/SISTEMA_CACHE_HIBRIDO.md` - referências a scrapers antigos
- `docs/SCRAPER_ROBUSTO_EXPLICACAO.md` - scraper obsoleto
- `docs/README_SCRAPERS.md` - scrapers removidos
- `docs/IMPLEMENTACAO_INTERFACE_INTERATIVA.md` - interface antiga
- `docs/GUIA_LEGISLACAO.md` - módulo não usado
- `docs/CORRECAO_REQUISICAO_TCE.md` - debug antigo
- `docs/ANALISE_CONFORMIDADE.md` - não relevante

#### **Estrutura Final Otimizada:**

```
tce-sc-infraestrutura/
├── app.py                          # Interface Streamlit
├── iqesc_scraper_dinamico.py       # Scraper TCE-SC (único necessário)
├── testar_sistema.py               # Script de testes
│
├── src/
│   ├── __init__.py
│   └── calculadora/
│       ├── __init__.py
│       └── calculadora_iqesc.py    # Motor de cálculos (único arquivo)
│
├── cache/
│   └── iqesc_2024/                 # Dados locais
│
├── docs/
│   └── EXEMPLO_RELATORIO.md        # Único documento técnico mantido
│
├── requirements.txt                # Dependências essenciais
├── iniciar_app.bat                 # Atalho Windows
│
├── README.md                       # Documentação principal
├── README_APP.md                   # Guia completo da aplicação
├── GUIA_RAPIDO.md                  # Tutorial rápido
└── CHANGELOG.md                    # Este arquivo
```

#### **Estatísticas:**
- **Antes:** 50+ arquivos em múltiplos diretórios
- **Depois:** ~15 arquivos essenciais
- **Redução:** ~70% de arquivos
- **Módulos Python:** 7 → 3 (calculadora_iqesc.py + 2 __init__.py)
- **Scrapers:** 4 → 1 (iqesc_scraper_dinamico.py)
- **Docs:** 8 → 4 (3 guias + 1 exemplo)

#### **Benefícios:**
- ✅ Projeto mais enxuto e fácil de entender
- ✅ Sem redundâncias de código ou dados
- ✅ Documentação focada e atualizada
- ✅ Manutenção simplificada
- ✅ Onboarding mais rápido para novos desenvolvedores
- ✅ Cache limpo apenas com dados necessários

---

## [3.0.0] - 2026-05-30

### ✨ Novidades Principais

#### **💰 Sistema Completo de Cálculos Financeiros ICMS**
- Adicionado campo para informar montante total anual do ICMS Educacional
- Cálculo automático de repasse financeiro por município:
  - **Repasse Atual**: baseado no IQESC atual do município
  - **Repasse Potencial**: se o município atingir IQESC máximo (1.0)
  - **Gap Financeiro**: diferença entre potencial e atual (em R$ e %)
  - **% da Distribuição**: participação do município no total estadual
- Nova seção visual "💰 Repasse Financeiro" na análise de municípios
- Integração de dados financeiros nos relatórios TXT exportados
- Formatação monetária completa (R$ X.XXX.XXX,XX)

#### **🔄 Sistema de Atualização Aprimorado**
- Novo botão "🔄 Forçar Atualização de Dados" na sidebar
- Verificação inteligente de cache antes de fazer download
- Mensagens claras sobre origem dos dados:
  - "✅ Dados carregados do cache local"
  - "✅ Dados baixados com sucesso do TCE-SC"
  - "✅ Dados atualizados com sucesso"
- Sistema `st.session_state` para evitar recarregamentos desnecessários
- Download condicional apenas quando necessário

#### **🎨 Interface Redesenhada**
- Layout otimizado com métricas principais destacadas
- Seção de repasse financeiro com 4 cards visuais
- Avisos contextuais:
  - Mostra montante ICMS quando informado
  - Alerta quando montante = 0 (sem cálculos financeiros)
- Melhor organização hierárquica de informações
- Remoção de seção duplicada de indicadores

### 🔧 Melhorias Técnicas

**Backend (`calculadora_iqesc.py`):**
- Novo parâmetro `montante_total_icms` no construtor
- Método `calcular_repasse()` com lógica completa:
  ```python
  percentual_distribuicao = (iqesc_municipio / soma_iqesc_total) * 100
  repasse_atual = (iqesc_municipio / soma_iqesc_total) * montante_total
  repasse_maximo = (1.0 / soma_se_maximo) * montante_total
  gap_financeiro = repasse_maximo - repasse_atual
  ```
- Atualização de `analisar_municipio()` incluindo `repasse_financeiro`
- Modificação de `gerar_relatorio_completo()` com seção financeira

**Frontend (`app.py`):**
- Input numérico para montante ICMS (R$ 0 a 10 bilhões)
- Botão de forçar atualização substitui checkbox
- Função `verificar_e_carregar_dados()` aprimorada com parâmetro `forcar_atualizacao`
- Uso de `session_state` para manter estado entre execuções:
  - `calc`: instância da calculadora
  - `mensagem`: status do carregamento
  - `ultimo_ano`, `ultimo_montante`: controle de mudanças
  - `forcar_atualizacao`: flag temporária
- Carregamento condicional: só recarrega se ano/montante mudar

### 🧹 Limpeza e Organização

**Arquivos Removidos (14 itens):**
- `teste_iqesc_2023.py` - teste específico obsoleto
- `debug_handshake.txt`, `debug_iqesc_html.txt`, `debug_mensagens.json`
- `extrair_init_completo.py`, `init_payload_completo.json`
- `mapear_projeto.py` - script temporário
- `README_OLD.md` - documentação antiga
- `todos XHR.json`, `update_ativa_muni.json`, `ws_table_data_iqesc_2024.json`
- `GUIA_ANOS_ANTERIORES.md` - fora de escopo (foco em 2024)
- `iqesc_scraper.py` - versão antiga do scraper
- `cache/iqesc_2023/` - dados não funcionais

**Script de Limpeza:**
- Novo `limpar_projeto.py` para manutenção automatizada
- Relatório detalhado de arquivos removidos
- Estrutura do projeto documentada

### 📚 Documentação Atualizada

**README.md:**
- Reescrito completamente com foco em 2024
- Seção "Funcionalidades" detalhada:
  - Análise completa por município
  - Cálculos financeiros de repasse
  - Rankings personalizados
  - Estatísticas gerais
  - Exportação de dados
- Seção "Interface da Aplicação" com descrição de todas as 4 abas
- Seção "Configurações da Aplicação" explicando sidebar
- Exemplos de uso programático atualizados
- Lista de tecnologias utilizadas
- Links para documentação adicional

**Estrutura do Projeto:**
```
tce-sc-infraestrutura/
├── app.py                          # Interface Streamlit
├── iqesc_scraper_dinamico.py       # Scraper TCE-SC
├── src/calculadora/                # Motor de cálculos
├── cache/iqesc_2024/               # Dados (288 municípios)
├── requirements.txt                # Dependências
├── README.md                       # Documentação principal
├── README_APP.md                   # Guia da aplicação
├── GUIA_RAPIDO.md                  # Tutorial
└── CHANGELOG.md                    # Este arquivo
```

### 🐛 Correções

**Sintaxe e Indentação:**
- Corrigidos todos os erros de indentação no `app.py` (linhas 281, 443, 634)
- Removido bloco `except Exception` órfão sem `try` correspondente
- Corrigida estrutura `if/else` em bloco de análise de município
- Validação de compilação: todos os arquivos `.py` compilam sem erros

**Funcionalidade:**
- Correção de carregamento duplicado de dados
- Eliminação de chamadas desnecessárias ao scraper
- Cache funcionando corretamente (sem tentativa de download)

### ⚙️ Tecnologias

- **Python 3.11** - Linguagem principal
- **Streamlit 1.58.0** - Framework web
- **Requests, BeautifulSoup4, WebSocket-Client** - Scraping
- **JSON** - Armazenamento estruturado

### ⚠️ Limitações Conhecidas

- Suporte apenas para ano 2024 (dados disponíveis no TCE-SC)
- Download de anos anteriores (2023 e anteriores) não funcional
- Avisos de tipo do Pylance (não impedem funcionamento)

### 📊 Estatísticas do Projeto

- **Dados:** 288 municípios de SC
- **Indicadores:** 7 (IQESC, IEO, IPA, IEE, IEN, CSE, SCE)
- **Cache:** ~53KB (dados.json)
- **Arquivos removidos:** 14
- **Linhas de código:** ~1.500+ (app.py + calculadora)

---

## [2.0.0] - 2026-05-29

### ✨ Adições

#### **🚀 Download Automático de Dados**
- Sistema detecta automaticamente se dados existem no cache
- Download automático do TCE-SC quando necessário
- Barra de progresso durante download
- Mensagens informativas em todas as etapas
- Sem necessidade de comandos manuais

#### **📅 Seleção Flexível de Ano**
- Campo de input numérico substituindo dropdown
- Suporte a qualquer ano (range 2020-2030)
- Validação e feedback inteligente
- Sistema busca dados automaticamente

#### **🔄 Sistema de Cache Inteligente**
- Verifica cache antes de baixar (instantâneo)
- Download automático se cache não existir
- Mensagens claras sobre origem dos dados
- Suporte a uso offline após primeiro download

### 🔧 Melhorias Técnicas

**Integração Scraper:**
- Função `_executar_scraper()` na `CalculadoraIQESC`
- Uso de `subprocess` com timeout de 180s
- Captura e tratamento de erros de scraping
- Parâmetro `auto_download` no construtor

**Interface Streamlit:**
- Função `verificar_e_carregar_dados()` em `app.py`
- Spinner com mensagens de status
- Progress bar para feedback visual
- Tratamento robusto de erros

### 🐛 Correções
- Corrigido erro de import em `__init__.py`
- Ajustado parâmetro deprecado do Streamlit (`use_container_width` → `width`)
- Tratamento de timeout em scraping

---

## [1.0.0] - 2026-05-28

### ✨ Lançamento Inicial

#### **Interface Web Streamlit**
- 4 abas principais:
  1. Análise por Município
  2. Rankings
  3. Estatísticas Gerais
  4. Exportar Dados
- Visualizações interativas
- Métricas destacadas
- Gráficos de barras de progresso

#### **Motor de Cálculos**
- Classe `CalculadoraIQESC`
- Análise completa por município
- Rankings customizáveis
- Estatísticas estaduais
- Exportação CSV/JSON

#### **Scraper IQESC**
- Script `iqesc_scraper_dinamico.py`
- Comunicação WebSocket/SockJS
- Validação de cache
- Detecção de mudanças estruturais

### 📦 Dependências
- streamlit==1.58.0
- requests
- beautifulsoup4
- websocket-client

### 📚 Documentação
- README.md
- README_APP.md
- GUIA_RAPIDO.md
- requirements.txt

---

**Formato:** [MAJOR.MINOR.PATCH]  
**Versionamento Semântico:** https://semver.org/lang/pt-BR/

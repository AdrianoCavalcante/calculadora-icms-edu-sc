# 🚀 Deploy no Streamlit Community Cloud

Este guia explica como fazer o deploy da Calculadora IQESC no Streamlit Community Cloud.

---

## 📋 Pré-requisitos

1. **Conta GitHub** - Criar em [github.com](https://github.com)
2. **Conta Streamlit Cloud** - Criar em [streamlit.io/cloud](https://streamlit.io/cloud)
3. **Repositório Git** - Este projeto

---

## 🔧 Preparação do Projeto

### 1. Inicializar Repositório Git

```bash
cd "c:\Users\User\Documents\VSC\Facu\Projeto Integrador V\ICMS Educacional SC\tce-sc-infraestrutura"

# Inicializar Git
git init

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "Initial commit - Calculadora IQESC v3.1.3"
```

### 2. Criar Repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Nome: `calculadora-iqesc-sc`
3. Descrição: `Calculadora de IQESC para municípios de Santa Catarina`
4. Visibilidade: **Público** (ou Privado, se preferir)
5. **NÃO** marque "Add README" (já temos um)
6. Clique em **Create repository**

### 3. Conectar ao GitHub

```bash
# Adicionar remote
git remote add origin https://github.com/SEU_USUARIO/calculadora-iqesc-sc.git

# Renomear branch para main
git branch -M main

# Push inicial
git push -u origin main
```

---

## ☁️ Deploy no Streamlit Cloud

### 1. Acessar Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em **"New app"**

### 2. Configurar Deploy

**Deploy settings:**
- **Repository**: `SEU_USUARIO/calculadora-iqesc-sc`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL** (opcional): Escolha um nome customizado

### 3. Deploy Automático

- Clique em **"Deploy!"**
- Aguarde 2-5 minutos
- O app estará disponível em: `https://SEU_APP.streamlit.app`

---

## 🔄 Funcionamento Híbrido (Online + Offline)

### ✅ Online (Streamlit Cloud)

**Primeira execução:**
- O scraper baixa dados do TCE-SC automaticamente
- Cache é criado em `cache/iqesc_2024/`
- Dados ficam disponíveis para 288 municípios

**Execuções seguintes:**
- Usa cache existente
- Download só ocorre se forçar atualização

### ✅ Offline (Localhost)

**Com cache existente:**
```bash
streamlit run app.py
```
- Funciona totalmente offline
- Usa dados em `cache/iqesc_2024/`

**Sem cache (precisa internet):**
- Primeira execução baixa dados
- Depois funciona offline

---

## 📦 Arquivos Importantes

### `.gitignore`
```gitignore
cache/               # Cache NÃO vai pro GitHub
__pycache__/         # Arquivos compilados ignorados
.venv/               # Virtual env ignorado
```

### `requirements.txt`
```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
websocket-client>=1.6.0
streamlit>=1.28.0,<2.0.0
numpy>=1.24.0,<2.0.0
pandas>=2.0.0,<3.0.0
openpyxl>=3.1.0
```

### `.streamlit/config.toml`
Configurações de tema e servidor para o Streamlit Cloud.

---

## 🔐 Segurança

### Dados Públicos
- IQESC é público (fonte: TCE-SC)
- Não há secrets ou API keys
- Sem informações sensíveis

### Cache
- Cache **não** vai para o GitHub
- É recriado automaticamente online
- Baixado na primeira execução

---

## 🔄 Atualizar Deploy

### Atualização Automática

Qualquer `git push` dispara deploy automático:

```bash
# Fazer alterações no código
git add .
git commit -m "Descrição das mudanças"
git push origin main
```

O Streamlit Cloud detecta e redeploy automaticamente.

### Atualização Manual

No [dashboard do Streamlit Cloud](https://share.streamlit.io):
1. Clique no app
2. Menu ⚙️ → **Reboot app**

---

## 🐛 Troubleshooting

### Erro: "Module not found"

**Solução:** Verificar `requirements.txt`
```bash
# Listar dependências instaladas
pip list

# Gerar requirements atualizado
pip freeze > requirements.txt
```

### Erro: "No data available"

**Causa:** Scraper falhou ao baixar dados do TCE-SC

**Soluções:**
1. Verificar se TCE-SC está online
2. Forçar atualização pelo botão na interface
3. Executar manualmente: `python src/iqesc_scraper_dinamico.py 2024 --force-update`

### App Lento ou Timeout

**Causa:** Streamlit Cloud tem limites de recursos

**Soluções:**
1. Otimizar cache com `@st.cache_data`
2. Reduzir processamento pesado
3. Considerar plano pago para mais recursos

### Erro ao Conectar GitHub

**Solução:** Configurar credenciais Git
```bash
# Configurar nome e email
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Usar token de acesso pessoal
# GitHub Settings → Developer Settings → Personal Access Tokens
```

---

## 📊 Monitoramento

### Logs em Tempo Real

No Streamlit Cloud:
- Menu ⚙️ → **Logs**
- Visualizar prints e erros em tempo real

### Métricas de Uso

No dashboard:
- Número de visualizações
- Tempo de execução
- Uso de recursos

---

## 🎯 URLs Úteis

- **Streamlit Cloud**: [share.streamlit.io](https://share.streamlit.io)
- **Documentação**: [docs.streamlit.io](https://docs.streamlit.io)
- **Repositório GitHub**: `https://github.com/SEU_USUARIO/calculadora-iqesc-sc`
- **App Online**: `https://SEU_APP.streamlit.app`
- **TCE-SC Dados**: [portaldocidadao.tce.sc.gov.br](https://portaldocidadao.tce.sc.gov.br)

---

## ✨ Vantagens do Deploy Online

✅ **Acessível de qualquer lugar** - Não precisa instalar nada  
✅ **Sempre atualizado** - Deploy automático a cada push  
✅ **Gratuito** - Streamlit Cloud é free para projetos públicos  
✅ **Compartilhável** - Envie o link para qualquer pessoa  
✅ **HTTPS incluído** - Seguro por padrão  
✅ **Mantém versão offline** - Ainda funciona localmente  

---

## 📝 Checklist de Deploy

- [ ] Repositório Git inicializado
- [ ] `.gitignore` configurado (cache/ ignorado)
- [ ] `requirements.txt` atualizado
- [ ] `.streamlit/config.toml` criado
- [ ] Repositório GitHub criado
- [ ] Código enviado para GitHub
- [ ] Conta Streamlit Cloud criada
- [ ] App deployado no Streamlit Cloud
- [ ] App testado online
- [ ] URL compartilhada

---

**🎉 Pronto! Seu app está online e funcionando!**

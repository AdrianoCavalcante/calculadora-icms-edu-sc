# 🚀 Guia Rápido - Sistema IQESC Automático

## ✨ O que mudou?

### **Agora é 100% AUTOMÁTICO!**

Você não precisa mais executar comandos manualmente ou se preocupar com cache. O sistema faz tudo automaticamente!

---

## 📝 Como Usar

### 1️⃣ **Inicie a Aplicação**

Duplo clique em: `iniciar_app.bat`

**OU** execute no terminal:
```bash
streamlit run app.py
```

### 2️⃣ **Digite o Ano Desejado**

Na barra lateral, você verá:
```
📅 Selecione o Ano
Digite o ano desejado: [2024]
```

- **Digite qualquer ano** (ex: 2023, 2022, 2025)
- Pressione **Enter** ou clique em **"🔄 Carregar/Atualizar Dados"**

### 3️⃣ **O Sistema Faz Automaticamente:**

#### ✅ **Se os dados já existem no cache:**
```
✅ Dados carregados do cache local
```
→ **Instantâneo!** Sem necessidade de internet.

#### 🌐 **Se os dados NÃO existem:**
```
📥 Dados não encontrados no cache para o ano 2023
🌐 Conectando ao TCE-SC para baixar dados...
[■■■■■■■■■■■■■■■■■■■■] Processando...
✅ Dados baixados com sucesso do TCE-SC
```
→ **Download automático!** Aguarde 1-2 minutos.

#### ❌ **Se o ano não tem dados disponíveis:**
```
❌ Não foram encontrados dados para o ano 2020 no TCE-SC.

💡 Dicas:
- Verifique sua conexão com internet
- Confirme se o ano digitado tem dados disponíveis no TCE-SC
```

---

## 🎯 Exemplos de Uso

### **Exemplo 1: Consultar dados de 2024**
1. Digite: `2024`
2. Clique: **"🔄 Carregar/Atualizar Dados"**
3. **Resultado:** Dados carregados instantaneamente (do cache)

### **Exemplo 2: Consultar dados de 2023 (primeira vez)**
1. Digite: `2023`
2. Clique: **"🔄 Carregar/Atualizar Dados"**
3. **Sistema mostra:**
   - 📥 "Dados não encontrados no cache"
   - 🌐 "Conectando ao TCE-SC..."
   - ⏳ Barra de progresso
   - ✅ "Dados baixados com sucesso"
4. **Resultado:** Dados de 2023 disponíveis!

### **Exemplo 3: Atualizar dados de 2024**
1. Digite: `2024`
2. Clique: **"🔄 Carregar/Atualizar Dados"**
3. **Resultado:** Cache limpo, dados recarregados

---

## 🔄 Fluxo Automático

```
┌──────────────────┐
│ Usuário digita   │
│ ano (ex: 2023)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Sistema verifica │
│ cache local      │
└────┬────────┬────┘
     │        │
     │ SIM    │ NÃO
     ▼        ▼
┌─────────┐  ┌──────────────────┐
│ Carrega │  │ Mostra mensagem: │
│ do      │  │ "Baixando dados" │
│ cache   │  └────────┬─────────┘
└─────────┘           │
                      ▼
              ┌────────────────┐
              │ Executa scraper│
              │ automaticamente│
              └────────┬───────┘
                       │
                  ┌────┴────┐
                  │ Sucesso?│
                  └─┬─────┬─┘
             SIM   │     │  NÃO
                   ▼     ▼
            ┌─────────┐  ┌──────────────┐
            │ Carrega │  │ Mostra erro: │
            │ dados   │  │ "Dados não   │
            │ baixados│  │ encontrados" │
            └─────────┘  └──────────────┘
```

---

## 💡 Perguntas Frequentes

### **P: Preciso ter internet sempre?**
**R:** Não! Após o primeiro download, os dados ficam em cache. Você pode usar offline.

### **P: Como forçar atualização dos dados?**
**R:** Clique no botão **"🔄 Carregar/Atualizar Dados"** na sidebar.

### **P: Onde ficam os dados salvos?**
**R:** No diretório `cache/iqesc_XXXX/` (ex: `cache/iqesc_2023/`)

### **P: Quanto tempo leva o download?**
**R:** Entre 1-2 minutos, dependendo da conexão.

### **P: Posso usar vários anos ao mesmo tempo?**
**R:** Sim! Cada ano fica em seu próprio cache. Digite o ano e o sistema carrega automaticamente.

### **P: O que fazer se der erro?**
**R:** 
1. Verifique sua conexão com internet
2. Confirme se o ano tem dados no TCE-SC (disponível geralmente de 2021-2025)
3. Tente executar manualmente: `python iqesc_scraper_dinamico.py 2023`

---

## 🎨 Interface Visual

### **Sidebar (Esquerda)**
```
⚙️ Configurações
━━━━━━━━━━━━━━━━━━
📅 Selecione o Ano
Digite o ano: [2024]

🔄 Carregar/Atualizar Dados
━━━━━━━━━━━━━━━━━━
✅ Dados carregados do cache local
━━━━━━━━━━━━━━━━━━
📈 Visão Geral
Total de Municípios: 288
IQESC Médio: 0.5918
IQESC Máximo: 0.9214
IQESC Mínimo: 0.2897
```

### **Área Principal**
- 🏛️ **Análise por Município** - Relatórios detalhados
- 🏆 **Rankings** - Top municípios por indicador
- 📊 **Estatísticas Gerais** - Visão estadual
- 💾 **Exportar Dados** - CSV/JSON para download

---

## 🚀 Vantagens do Sistema Automático

✅ **Sem comandos** - Tudo pela interface  
✅ **Download inteligente** - Só baixa se necessário  
✅ **Cache eficiente** - Uso offline após primeira vez  
✅ **Feedback visual** - Barras de progresso e mensagens  
✅ **Validação automática** - Verifica ano disponível  
✅ **Múltiplos anos** - Alterna entre anos facilmente  

---

## 📞 Suporte

Se tiver problemas:
1. Verifique o [README_APP.md](README_APP.md) completo
2. Execute testes manuais: `python src/calculadora/calculadora_iqesc.py`
3. Verifique cache: `dir cache\iqesc_*`

---

**Desenvolvido para:** Projeto Integrador V - ICMS Educacional SC  
**Última Atualização:** 30/05/2026  
**Versão:** 2.0 (Automática)

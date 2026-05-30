# 🔧 GUIA DE TROUBLESHOOTING - Dependências

## 📋 Problema: ValueError numpy.dtype size changed

### Sintomas
```
ValueError: numpy.dtype size changed, may indicate binary incompatibility. 
Expected 96 from C header, got 88 from PyObject
```

Erro aparece ao:
- Executar `streamlit run app.py`
- Usar `st.dataframe()`
- Importar pandas

---

## 🔍 Causa

**Incompatibilidade binária** entre NumPy e Pandas:
- Pandas foi compilado com uma versão do NumPy
- Mas está sendo executado com versão diferente do NumPy
- NumPy 2.0.0+ mudou a estrutura binária (ABI incompatível)

**No nosso caso:**
- ❌ NumPy 2.0.0 instalado
- ❌ Pandas 1.5.3 compilado para NumPy < 2.0
- ❌ Incompatibilidade binária

---

## ✅ Solução Implementada

### Opção 1: Script Automático (Recomendado)

```bash
cd "c:\Users\User\Documents\VSC\Facu\Projeto Integrador V\ICMS Educacional SC\tce-sc-infraestrutura"
pip uninstall numpy pandas -y
pip cache purge
pip install -r requirements.txt
```

### Opção 2: Passo a Passo Manual

```bash
# 1. Desinstalar pacotes problemáticos
pip uninstall numpy pandas -y

# 2. Limpar cache do pip
pip cache purge

# 3. Instalar versões compatíveis
pip install "numpy>=1.24.0,<2.0.0"
pip install "pandas>=2.0.0,<3.0.0"

# 4. Reinstalar todas as dependências
pip install -r requirements.txt
```

### Opção 3: Versões Específicas (Garantido)

```bash
pip uninstall numpy pandas -y
pip install numpy==1.26.4
pip install pandas==2.3.3
pip install -r requirements.txt
```

---

## 📦 Versões Compatíveis

### ✅ Configuração Atual (Funcionando)

```
numpy==1.26.4      # < 2.0.0 (compatível)
pandas==2.3.3      # >= 2.0.0 (moderno)
streamlit==1.58.0  # Funciona com ambos
```

### ⚠️ Versões Problemáticas

```
numpy==2.0.0+      # ABI incompatível com pandas antigos
pandas==1.5.3      # Compilado para numpy < 2.0
```

---

## 🧪 Verificação

Após a correção, verifique:

```python
python -c "import numpy as np; import pandas as pd; print(f'NumPy: {np.__version__}'); print(f'Pandas: {pd.__version__}'); df = pd.DataFrame({'A': [1, 2, 3]}); print('✅ Teste OK!')"
```

**Saída esperada:**
```
NumPy: 1.26.4
Pandas: 2.3.3
✅ Teste OK!
```

---

## 📝 Requirements.txt Atualizado

```txt
# Web Scraping
requests>=2.31.0
beautifulsoup4>=4.12.0
websocket-client>=1.6.0

# Interface Web
streamlit>=1.28.0,<2.0.0

# Dados e Análise (versões compatíveis)
numpy>=1.24.0,<2.0.0      # Evita numpy 2.0+
pandas>=2.0.0,<3.0.0       # Versão moderna

# Exportação
openpyxl>=3.1.0
```

---

## 🚨 Prevenção Futura

### Boas Práticas

1. **Sempre especificar versões** no requirements.txt:
   ```
   numpy>=1.24.0,<2.0.0  # Range seguro
   ```

2. **Evitar upgrades automáticos** de pacotes críticos:
   ```bash
   pip install --upgrade numpy  # ⚠️ CUIDADO!
   ```

3. **Testar após atualizações:**
   ```bash
   python -c "import pandas; import numpy"
   ```

4. **Usar ambientes virtuais** para isolar dependências

---

## 🔗 Referências

- [NumPy 2.0 Migration Guide](https://numpy.org/devdocs/numpy_2_0_migration_guide.html)
- [Pandas Release Notes](https://pandas.pydata.org/docs/whatsnew/index.html)
- [Streamlit Compatibility](https://docs.streamlit.io/)

---

## 📅 Histórico

- **30/05/2026** - Problema identificado e corrigido
  - NumPy 2.0.0 → 1.26.4
  - Pandas 1.5.3 → 2.3.3
  - Requirements.txt atualizado com restrições de versão

---

## 💡 Dica Rápida

Se o erro voltar a aparecer no futuro:

```bash
pip install --force-reinstall "numpy<2.0.0" "pandas>=2.0.0"
```

Isso força a reinstalação com as versões corretas.

---

**✅ Problema resolvido na versão 3.1.1**

# 🚀 Guia Rápido: Enviar Projeto para GitHub

Este arquivo contém os comandos exatos para subir o projeto no GitHub.

---

## 📋 Pré-requisitos

1. ✅ Git instalado - [Download](https://git-scm.com/downloads)
2. ✅ Conta GitHub - [Criar conta](https://github.com/signup)

---

## 🔧 Passo 1: Configurar Git (primeira vez apenas)

```bash
# Configurar nome e email
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

---

## 📦 Passo 2: Inicializar Repositório

Abra o PowerShell nesta pasta e execute:

```powershell
# Navegar para o diretório do projeto
cd "c:\Users\User\Documents\VSC\Facu\Projeto Integrador V\ICMS Educacional SC\tce-sc-infraestrutura"

# Inicializar Git
git init

# Adicionar todos os arquivos
git add .

# Verificar status (ver arquivos que serão commitados)
git status

# Primeiro commit
git commit -m "🎉 Initial commit - Calculadora IQESC v3.1.3"
```

**Resultado esperado:**
```
[master (root-commit) abc1234] 🎉 Initial commit - Calculadora IQESC v3.1.3
 XX files changed, XXXX insertions(+)
```

---

## 🌐 Passo 3: Criar Repositório no GitHub

### Via Interface Web (Recomendado)

1. Acesse: [https://github.com/new](https://github.com/new)

2. Preencha:
   - **Repository name**: `calculadora-iqesc-sc`
   - **Description**: `Calculadora de IQESC para municípios de Santa Catarina - Análise de indicadores educacionais com interface Streamlit`
   - **Visibilidade**: 
     - ✅ **Public** (recomendado para Streamlit Cloud gratuito)
     - 🔒 **Private** (se preferir restrito)
   - **NÃO** marque nada em "Initialize this repository with:"

3. Clique em **"Create repository"**

### Via GitHub CLI (Alternativo)

```bash
# Instalar GitHub CLI: https://cli.github.com/
gh repo create calculadora-iqesc-sc --public --description "Calculadora IQESC - Santa Catarina"
```

---

## 🔗 Passo 4: Conectar e Enviar para GitHub

Após criar o repositório, copie a URL (exemplo: `https://github.com/SEU_USUARIO/calculadora-iqesc-sc.git`)

```powershell
# Adicionar remote (SUBSTITUA SEU_USUARIO pelo seu nome no GitHub)
git remote add origin https://github.com/SEU_USUARIO/calculadora-iqesc-sc.git

# Renomear branch para main
git branch -M main

# Enviar código para GitHub
git push -u origin main
```

**Resultado esperado:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XX.XX KiB | XX.XX MiB/s, done.
Total XX (delta X), reused X (delta X)
To https://github.com/SEU_USUARIO/calculadora-iqesc-sc.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**✅ Projeto agora está no GitHub!**

Acesse: `https://github.com/SEU_USUARIO/calculadora-iqesc-sc`

---

## 🔐 Autenticação GitHub

### Opção 1: Token de Acesso Pessoal (Recomendado)

1. Acesse: [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Clique em **"Generate new token (classic)"**
3. Configurações:
   - **Note**: `Calculadora IQESC - VSCode`
   - **Expiration**: `90 days` (ou mais)
   - **Scopes**: Marque `repo` (full control)
4. Clique em **"Generate token"**
5. **COPIE O TOKEN** (só aparece uma vez!)

Quando o Git pedir senha, use o **token** (não sua senha do GitHub).

### Opção 2: GitHub CLI (Mais fácil)

```bash
# Instalar: https://cli.github.com/
gh auth login

# Seguir instruções interativas
```

---

## 🔄 Comandos para Atualizações Futuras

Após fazer alterações no código:

```powershell
# Ver o que mudou
git status

# Adicionar alterações
git add .

# Commit com mensagem descritiva
git commit -m "✨ Descrição das mudanças"

# Enviar para GitHub
git push origin main
```

**Dica:** Use emojis nos commits!
- 🎉 `:tada:` - Initial commit
- ✨ `:sparkles:` - Nova funcionalidade
- 🐛 `:bug:` - Correção de bug
- 📝 `:memo:` - Documentação
- 🔧 `:wrench:` - Configuração
- ♻️ `:recycle:` - Refatoração
- 🎨 `:art:` - Melhorias de UI/estilo

---

## 📊 Verificar Sucesso

Após o `git push`, verifique:

1. ✅ Repositório visível no GitHub
2. ✅ Todos os arquivos presentes
3. ✅ Cache **NÃO** presente (ignorado pelo .gitignore)
4. ✅ README.md renderizado na página principal

---

## 🚨 Troubleshooting

### Erro: "remote origin already exists"

```bash
# Remover remote existente
git remote remove origin

# Adicionar novamente
git remote add origin https://github.com/SEU_USUARIO/calculadora-iqesc-sc.git
```

### Erro: "Support for password authentication was removed"

**Solução:** Use token de acesso pessoal em vez de senha.

### Erro: "Permission denied"

**Solução:** Configure credenciais:
```bash
gh auth login
```

Ou use token de acesso pessoal.

### Ver remotes configurados

```bash
git remote -v
```

---

## 📚 Próximos Passos

Após o código estar no GitHub:

1. 🚀 **Deploy no Streamlit Cloud** - Ver [docs/DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)
2. 📝 **Adicionar descrição** no GitHub (About → ⚙️ → Description)
3. 🏷️ **Adicionar topics** no GitHub: `streamlit`, `python`, `education`, `santa-catarina`, `iqesc`
4. ⭐ **Estrelar o repositório** (favoritar)

---

## ✅ Checklist

- [ ] Git configurado (nome e email)
- [ ] Repositório inicializado (`git init`)
- [ ] Arquivos adicionados (`git add .`)
- [ ] Primeiro commit feito
- [ ] Repositório criado no GitHub
- [ ] Remote configurado (`git remote add`)
- [ ] Código enviado (`git push`)
- [ ] Repositório visível no GitHub
- [ ] README renderizado corretamente
- [ ] Pronto para deploy no Streamlit Cloud!

---

**🎉 Parabéns! Seu projeto está no GitHub!**

Agora pode seguir para o deploy no Streamlit Cloud: [docs/DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md)

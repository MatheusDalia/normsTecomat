# 🚀 Deploy no Streamlit Cloud - Guia Completo

## 🎯 Objetivo

Fazer o editor ficar disponível 24h/dia, sem depender do seu computador, e com persistência automática das edições.

## ✅ Vantagens do Streamlit Cloud

- **Disponível 24h/dia** - Não precisa deixar PC ligado
- **Link público** - Gerente acessa de qualquer lugar
- **Persistência** - Edições ficam salvas mesmo se suspender
- **Grátis** - Para uso pessoal/pequeno
- **Fácil** - Deploy automático

## 📋 Pré-requisitos

1. Conta no GitHub (gratuita)
2. Conta no Streamlit Cloud (gratuita)
3. Arquivos do projeto organizados

## 🛠️ Passo a Passo

### 1️⃣ **Preparar o Repositório GitHub**

#### A) Criar repositório no GitHub

1. Acesse: https://github.com
2. Clique em "New repository"
3. Nome: `actionplan-editor-tecomat`
4. Público ou privado (recomendo privado)
5. Clique "Create repository"

#### B) Subir arquivos para o GitHub

```bash
# No terminal, na pasta do projeto
git init
git add .
git commit -m "Primeiro commit - Editor ActionPlan"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/actionplan-editor-tecomat.git
git push -u origin main
```

### 2️⃣ **Arquivos Necessários**

Certifique-se de que estes arquivos estão no repositório:

```
actionplan-editor-tecomat/
├── streamlit_app.py          # Arquivo principal
├── SGQP-Tecomat.norms.json   # Dados originais
├── requirements.txt          # Dependências
├── .gitignore               # Arquivos a ignorar
└── README.md                # Documentação
```

### 3️⃣ **Configurar Streamlit Cloud**

#### A) Acessar Streamlit Cloud

1. Vá para: https://streamlit.io/cloud
2. Clique em "Sign in"
3. Faça login com GitHub

#### B) Criar nova aplicação

1. Clique em "New app"
2. Preencha:
   - **Repository**: `SEU_USUARIO/actionplan-editor-tecomat`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. Clique "Deploy!"

### 4️⃣ **Configurações Avançadas (Opcional)**

#### A) Configurar variáveis de ambiente

No Streamlit Cloud, vá em "Settings" → "Secrets" e adicione:

```toml
[general]
# Configurações específicas se necessário
```

#### B) Configurar domínio personalizado (se tiver)

1. Vá em "Settings" → "General"
2. Adicione seu domínio

## 🔧 Arquivos de Configuração

### `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Streamlit
.streamlit/

# Arquivos de edição (serão criados automaticamente)
edicoes_salvas.json
backup_edicoes.json

# Sistema
.DS_Store
Thumbs.db
```

### `requirements.txt`

```txt
streamlit>=1.28.0
```

### `README.md`

```markdown
# Editor ActionPlan - Tecomat

Editor simples para edição de ActionPlans com persistência automática.

## Como usar

1. Acesse o link do Streamlit Cloud
2. Edite os campos de título e texto
3. As edições são salvas automaticamente
4. Baixe o arquivo final quando terminar

## Arquivos

- `streamlit_app.py` - Aplicação principal
- `SGQP-Tecomat.norms.json` - Dados originais
```

## 🌐 Após o Deploy

### **Link Público**

Após o deploy, você receberá um link como:

```
https://actionplan-editor-tecomat-xxxxx.streamlit.app
```

### **Compartilhar com o Gerente**

1. Envie o link para o gerente
2. Envie também o `GUIA_GERENTE.md`
3. O gerente pode acessar de qualquer lugar

## 🔄 Atualizações

### **Para atualizar o site:**

```bash
# Faça as mudanças nos arquivos
git add .
git commit -m "Atualização do editor"
git push origin main
# O Streamlit Cloud atualiza automaticamente
```

## 📊 Monitoramento

### **No Streamlit Cloud você pode ver:**

- Status da aplicação (online/offline)
- Logs de erro
- Estatísticas de uso
- Configurações

## 🆘 Solução de Problemas

### **Site não abre:**

1. Verifique se o deploy foi concluído
2. Verifique os logs no Streamlit Cloud
3. Verifique se o arquivo `streamlit_app.py` existe

### **Erro de dependências:**

1. Verifique se `requirements.txt` está correto
2. Verifique se todas as dependências estão listadas

### **Arquivo JSON não encontrado:**

1. Verifique se `SGQP-Tecomat.norms.json` está no repositório
2. Verifique se o nome está correto

### **Edições não salvam:**

1. Verifique se o arquivo `edicoes_salvas.json` pode ser criado
2. Verifique os logs de erro

## 💡 Dicas Importantes

### **Para o Deploy:**

- ✅ Mantenha o repositório organizado
- ✅ Use nomes de arquivo simples
- ✅ Teste localmente antes do deploy
- ✅ Verifique os logs se der erro

### **Para o Gerente:**

- ✅ O link fica sempre disponível
- ✅ Edições são salvas automaticamente
- ✅ Pode acessar de qualquer dispositivo
- ✅ Não precisa instalar nada

## 🎉 Resultado Final

**Após o deploy, você terá:**

- ✅ Site disponível 24h/dia
- ✅ Link público para compartilhar
- ✅ Persistência automática das edições
- ✅ Zero dependência do seu computador
- ✅ Atualizações automáticas

**O gerente poderá:**

- ✅ Acessar de qualquer lugar
- ✅ Editar sem perder dados
- ✅ Baixar arquivo final
- ✅ Trabalhar sem interrupções

---

## 🚀 **PRONTO!**

Agora seu editor está na nuvem e disponível sempre! 🎯

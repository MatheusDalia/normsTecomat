# Editor de ActionPlan - Tecomat

## 📋 Descrição

Sistema melhorado para edição de ActionPlans no arquivo JSON da Tecomat, com persistência automática e interface organizada.

## 🚀 Principais Melhorias

### ✅ Persistência Automática

- **Salvamento automático**: As alterações são salvas automaticamente
- **Arquivo de progresso**: Mantém registro das edições realizadas
- **Backup automático**: Cria backups para segurança

### 🎨 Interface Melhorada

- **Layout responsivo**: Interface organizada com sidebar
- **Filtros inteligentes**: Busca e filtros para navegação fácil
- **Indicadores visuais**: Status de edição e progresso
- **Cards organizados**: Cada ActionPlan em um card separado

### 🔧 Funcionalidades

#### Sidebar de Controles

- **Estatísticas**: Total de ActionPlans, editados e pendentes
- **Progresso**: Barra de progresso visual
- **Filtros**: Mostrar apenas editados ou pendentes
- **Busca**: Buscar por itemNumber ou descrição
- **Ações**: Salvar, baixar e restaurar backup

#### Editor Principal

- **Cards organizados**: Cada ActionPlan em um card
- **Status visual**: Indicadores de editado/pendente
- **Comparação**: Ver diferenças entre original e editado
- **Auto-save**: Salva automaticamente as alterações

## 📁 Arquivos

- `edit_json_streamlit_improved.py` - Editor principal melhorado
- `backup_manager.py` - Gerenciador de backups
- `SGQP-Tecomat.norms.json` - Arquivo de dados
- `editing_progress.json` - Arquivo de progresso (criado automaticamente)

## 🛠️ Como Usar

### 1. Preparação Inicial

```bash
# Criar backup inicial
python backup_manager.py
# Escolha opção 1 para criar backup
```

### 2. Executar o Editor

```bash
streamlit run edit_json_streamlit_improved.py
```

### 3. Navegação

- **Filtros**: Use a sidebar para filtrar ActionPlans
- **Busca**: Digite termos para encontrar específicos
- **Edição**: Clique nos campos para editar
- **Salvamento**: Automático ou manual via botão

### 4. Backup e Restauração

```bash
# Listar backups
python backup_manager.py
# Escolha opção 2

# Restaurar backup
python backup_manager.py
# Escolha opção 3
```

## 🔄 Fluxo de Trabalho Recomendado

1. **Backup inicial**: Sempre crie backup antes de começar
2. **Edição em lotes**: Use filtros para trabalhar em grupos
3. **Verificação**: Use "Ver diferenças" para confirmar alterações
4. **Download**: Baixe o arquivo final quando concluir
5. **Limpeza**: Remova backups antigos periodicamente

## ⚠️ Importante

- **Não feche o navegador**: Mantenha a aba aberta durante a edição
- **Backup regular**: Crie backups antes de grandes edições
- **Verificação**: Sempre verifique as alterações antes de finalizar
- **Download**: Baixe o arquivo final para backup

## 🎯 Vantagens sobre a Versão Anterior

| Aspecto      | Versão Anterior | Versão Melhorada         |
| ------------ | --------------- | ------------------------ |
| Persistência | ❌ Perdia dados | ✅ Salva automaticamente |
| Interface    | ❌ Básica       | ✅ Organizada e moderna  |
| Navegação    | ❌ Difícil      | ✅ Filtros e busca       |
| Backup       | ❌ Manual       | ✅ Automático            |
| Progresso    | ❌ Não mostrava | ✅ Visual e detalhado    |
| Segurança    | ❌ Sem backup   | ✅ Múltiplos backups     |

## 🆘 Solução de Problemas

### Problema: Dados perdidos após inatividade

**Solução**: O novo sistema salva automaticamente e mantém progresso

### Problema: Difícil encontrar ActionPlans específicos

**Solução**: Use os filtros e busca na sidebar

### Problema: Não sabe quantos editou

**Solução**: Veja as estatísticas na sidebar

### Problema: Precisa restaurar versão anterior

**Solução**: Use o gerenciador de backup

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique se o arquivo JSON existe
2. Execute o backup manager para verificar backups
3. Use a função de restauração se necessário
4. Baixe sempre o arquivo final como backup

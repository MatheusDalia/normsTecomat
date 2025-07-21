import streamlit as st
import json
import os
from datetime import datetime

# Configuração simples
st.set_page_config(
    page_title="Editor Simples - ActionPlan",
    page_icon="✏️",
    layout="wide"
)

# Caminho do arquivo
JSON_PATH = 'SGQP-Tecomat.norms.json'

# CSS simples e limpo
st.markdown("""
<style>
    .header {
        background-color: #4CAF50;
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .action-card {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 15px;
    }
    .status-ok {
        background-color: #d4edda;
        color: #155724;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
    }
    .status-pendente {
        background-color: #fff3cd;
        color: #856404;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
    }
    .download-btn {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="header">
    <h1>✏️ Editor de ActionPlan - Versão Simples</h1>
    <p>Edite os títulos e textos dos planos de ação de forma fácil</p>
</div>
""", unsafe_allow_html=True)

# Carregar dados


@st.cache_data
def carregar_dados():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error(f'Arquivo {JSON_PATH} não encontrado!')
        st.stop()

# Extrair action plans


def extrair_action_plans(data):
    action_plans = []
    for obj_idx, obj in enumerate(data):
        requirements = obj.get('requirements', [])
        for req_idx, req in enumerate(requirements):
            action_plans_list = req.get('actionPlan', [])
            for ap_idx, ap in enumerate(action_plans_list):
                action_plans.append({
                    'obj_idx': obj_idx,
                    'req_idx': req_idx,
                    'ap_idx': ap_idx,
                    'title': ap.get('title', ''),
                    'text': ap.get('text', ''),
                    'itemNumber': req.get('itemNumber', ''),
                    'descricao': req.get('specificRequirementDescription', ''),
                    'original_title': ap.get('title', ''),
                    'original_text': ap.get('text', '')
                })
    return action_plans


# Carregar dados
data = carregar_dados()
action_plans = extrair_action_plans(data)

# Sidebar simples
with st.sidebar:
    st.header("📊 Resumo")

    total = len(action_plans)
    editados = sum(1 for ap in action_plans if ap['title'] !=
                   ap['original_title'] or ap['text'] != ap['original_text'])

    st.metric("Total de Action Plans", total)
    st.metric("Editados", editados)
    st.metric("Pendentes", total - editados)

    if total > 0:
        progresso = (editados / total) * 100
        st.progress(progresso / 100)
        st.write(f"📈 {progresso:.1f}% concluído")

    st.markdown("---")

    st.header("🔍 Buscar")
    busca = st.text_input("Digite para buscar:",
                          placeholder="Ex: 4.1.1 ou descrição...")

    st.markdown("---")

    st.header("📋 Filtros")
    mostrar_editados = st.checkbox("Só mostrar editados")
    mostrar_pendentes = st.checkbox("Só mostrar pendentes")

    st.markdown("---")

    st.header("💾 Ações")

    # Botão para salvar
    if st.button("💾 SALVAR TUDO", type="primary", use_container_width=True):
        # Aplicar mudanças
        for ap in action_plans:
            data[ap['obj_idx']]['requirements'][ap['req_idx']
                                                ]['actionPlan'][ap['ap_idx']]['title'] = ap['title']
            data[ap['obj_idx']]['requirements'][ap['req_idx']
                                                ]['actionPlan'][ap['ap_idx']]['text'] = ap['text']

        # Salvar arquivo
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        st.success("✅ Arquivo salvo com sucesso!")
        st.balloons()

# Filtrar action plans
filtrados = action_plans

if busca:
    filtrados = [ap for ap in filtrados if
                 busca.lower() in ap['itemNumber'].lower() or
                 busca.lower() in ap['descricao'].lower()]

if mostrar_editados:
    filtrados = [ap for ap in filtrados if
                 ap['title'] != ap['original_title'] or
                 ap['text'] != ap['original_text']]

if mostrar_pendentes:
    filtrados = [ap for ap in filtrados if
                 ap['title'] == ap['original_title'] and
                 ap['text'] == ap['original_text']]

# Mostrar action plans
st.subheader(f"📝 Action Plans ({len(filtrados)} de {total})")

if not filtrados:
    st.info("🔍 Nenhum action plan encontrado com os filtros aplicados.")

# Contador para mostrar progresso
if len(filtrados) > 20:
    st.info(
        f"⚠️ Mostrando {len(filtrados)} action plans. Use a busca para encontrar específicos.")

for i, ap in enumerate(filtrados):
    # Verificar se foi editado
    foi_editado = ap['title'] != ap['original_title'] or ap['text'] != ap['original_text']
    status = "✅ Editado" if foi_editado else "⏳ Pendente"
    status_class = "status-ok" if foi_editado else "status-pendente"

    with st.container():
        st.markdown(f"""
        <div class="action-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3>ActionPlan #{i+1}</h3>
                <span class="{status_class}">{status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Informações básicas
        col1, col2 = st.columns([1, 2])

        with col1:
            st.write(f"**Item:** `{ap['itemNumber']}`")
            st.write(
                f"**Descrição:** {ap['descricao'][:80]}{'...' if len(ap['descricao']) > 80 else ''}")

            # Mostrar diferenças se editado
            if foi_editado:
                with st.expander("👀 Ver o que mudou"):
                    if ap['title'] != ap['original_title']:
                        st.write("**Título mudou:**")
                        st.write(f"Antes: {ap['original_title']}")
                        st.write(f"Depois: {ap['title']}")
                    if ap['text'] != ap['original_text']:
                        st.write("**Texto mudou:**")
                        st.write(f"Antes: {ap['original_text']}")
                        st.write(f"Depois: {ap['text']}")

        with col2:
            # Campos de edição
            novo_titulo = st.text_input(
                "Título:",
                value=ap['title'],
                key=f"titulo_{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}",
                help="Digite o novo título aqui"
            )

            novo_texto = st.text_area(
                "Texto:",
                value=ap['text'],
                key=f"texto_{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}",
                height=80,
                help="Digite o novo texto aqui"
            )

            # Atualizar dados
            ap['title'] = novo_titulo
            ap['text'] = novo_texto

        st.markdown("---")

# Seção de download
st.markdown("---")
st.header("📤 Enviar Arquivo Editado")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📥 Baixar Arquivo Completo")
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    st.download_button(
        label="📥 BAIXAR JSON COMPLETO",
        data=json_str,
        file_name=f'ActionPlan_Editado_{datetime.now().strftime("%d-%m-%Y_%H%M")}.json',
        mime='application/json',
        use_container_width=True
    )

with col2:
    st.markdown("### 📊 Baixar Apenas Editados")
    # Filtrar apenas os editados
    editados_data = []
    for ap in action_plans:
        if ap['title'] != ap['original_title'] or ap['text'] != ap['original_text']:
            editados_data.append({
                'itemNumber': ap['itemNumber'],
                'descricao': ap['descricao'],
                'titulo_original': ap['original_title'],
                'titulo_novo': ap['title'],
                'texto_original': ap['original_text'],
                'texto_novo': ap['text']
            })

    if editados_data:
        editados_json = json.dumps(editados_data, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 BAIXAR APENAS EDITADOS",
            data=editados_json,
            file_name=f'ActionPlan_Editados_{datetime.now().strftime("%d-%m-%Y_%H%M")}.json',
            mime='application/json',
            use_container_width=True
        )
    else:
        st.info("Nenhuma edição feita ainda")

with col3:
    st.markdown("### 📋 Baixar Relatório")
    # Criar relatório simples
    relatorio = f"""
RELATÓRIO DE EDIÇÃO - ACTIONPLAN
Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}

RESUMO:
- Total de Action Plans: {total}
- Editados: {editados}
- Pendentes: {total - editados}
- Progresso: {(editados/total*100):.1f}%

DETALHES DOS EDITADOS:
"""

    for ap in action_plans:
        if ap['title'] != ap['original_title'] or ap['text'] != ap['original_text']:
            relatorio += f"""
Item: {ap['itemNumber']}
Descrição: {ap['descricao']}
Título mudou: {'Sim' if ap['title'] != ap['original_title'] else 'Não'}
Texto mudou: {'Sim' if ap['text'] != ap['original_text'] else 'Não'}
---
"""

    st.download_button(
        label="📥 BAIXAR RELATÓRIO",
        data=relatorio,
        file_name=f'Relatorio_Edicao_{datetime.now().strftime("%d-%m-%Y_%H%M")}.txt',
        mime='text/plain',
        use_container_width=True
    )

# Instruções simples
st.markdown("---")
st.markdown("""
### 📋 Instruções Simples:

1. **Editar**: Clique nos campos e digite as mudanças
2. **Salvar**: Clique em "SALVAR TUDO" na barra lateral
3. **Baixar**: Escolha uma das opções de download acima
4. **Enviar**: Mande o arquivo baixado por email ou WhatsApp

### 💡 Dicas:
- Use a busca para encontrar action plans específicos
- Os campos mudam de cor quando você edita
- Sempre salve antes de baixar o arquivo
- O relatório mostra um resumo das mudanças
""")

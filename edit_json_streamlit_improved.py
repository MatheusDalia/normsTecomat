import streamlit as st
import json
import os
import time
from datetime import datetime
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Editor de ActionPlan - Tecomat",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminhos dos arquivos
JSON_PATH = 'SGQP-Tecomat.norms.json'
BACKUP_PATH = 'SGQP-Tecomat.norms.backup.json'
PROGRESS_PATH = 'editing_progress.json'

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .action-plan-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        padding: 3px;
        margin: 10px 0;
    }
    .progress-fill {
        background-color: #4CAF50;
        height: 20px;
        border-radius: 8px;
        transition: width 0.3s ease;
    }
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .status-pending { background-color: #fff3cd; color: #856404; }
    .status-edited { background-color: #d4edda; color: #155724; }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados


@st.cache_data
def load_json_data():
    """Carrega os dados do JSON com cache"""
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error(f'Arquivo {JSON_PATH} não encontrado.')
        st.stop()

# Função para salvar progresso


def save_progress(progress_data):
    """Salva o progresso de edição"""
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)

# Função para carregar progresso


def load_progress():
    """Carrega o progresso de edição"""
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Função para criar backup


def create_backup(data):
    """Cria backup dos dados originais"""
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Função para extrair action plans


def extract_action_plans(data):
    """Extrai todos os action plans do JSON"""
    all_action_plans = []
    for obj_idx, obj in enumerate(data):
        requirements = obj.get('requirements', [])
        for req_idx, req in enumerate(requirements):
            action_plans = req.get('actionPlan', [])
            for ap_idx, ap in enumerate(action_plans):
                all_action_plans.append({
                    'obj_idx': obj_idx,
                    'req_idx': req_idx,
                    'ap_idx': ap_idx,
                    'title': ap.get('title', ''),
                    'text': ap.get('text', ''),
                    'itemNumber': req.get('itemNumber', ''),
                    'specificRequirementDescription': req.get('specificRequirementDescription', ''),
                    'original_title': ap.get('title', ''),
                    'original_text': ap.get('text', '')
                })
    return all_action_plans

# Função para salvar alterações


def save_changes(data, action_plans):
    """Salva as alterações no arquivo JSON"""
    # Aplica as alterações
    for ap in action_plans:
        data[ap['obj_idx']]['requirements'][ap['req_idx']
                                            ]['actionPlan'][ap['ap_idx']]['title'] = ap['title']
        data[ap['obj_idx']]['requirements'][ap['req_idx']
                                            ]['actionPlan'][ap['ap_idx']]['text'] = ap['text']

    # Salva o arquivo
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Carregar dados
data = load_json_data()
action_plans = extract_action_plans(data)
progress = load_progress()

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📋 Editor de ActionPlan - Tecomat</h1>
    <p>Edite os campos <strong>title</strong> e <strong>text</strong> dos planos de ação de forma organizada</p>
</div>
""", unsafe_allow_html=True)

# Sidebar com controles
with st.sidebar:
    st.header("🎛️ Controles")

    # Estatísticas
    total_plans = len(action_plans)
    edited_plans = sum(
        1 for ap in action_plans if ap['title'] != ap['original_title'] or ap['text'] != ap['original_text'])

    st.metric("Total de Action Plans", total_plans)
    st.metric("Editados", edited_plans)
    st.metric("Pendentes", total_plans - edited_plans)

    # Progresso
    if total_plans > 0:
        progress_percent = (edited_plans / total_plans) * 100
        st.progress(progress_percent / 100)
        st.write(f"{progress_percent:.1f}% concluído")

    st.markdown("---")

    # Filtros
    st.subheader("🔍 Filtros")
    show_edited = st.checkbox("Mostrar apenas editados", value=False)
    show_pending = st.checkbox("Mostrar apenas pendentes", value=False)

    # Busca
    search_term = st.text_input("🔎 Buscar por itemNumber ou descrição", "")

    st.markdown("---")

    # Ações
    st.subheader("⚡ Ações")

    if st.button("💾 Salvar Alterações", type="primary"):
        save_changes(data, action_plans)
        st.success("Alterações salvas com sucesso!")

    if st.button("📥 Baixar JSON"):
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f'SGQP-Tecomat.norms.editado_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            mime='application/json'
        )

    if st.button("🔄 Restaurar Backup"):
        if os.path.exists(BACKUP_PATH):
            with open(BACKUP_PATH, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            with open(JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            st.success("Backup restaurado!")
            st.rerun()
        else:
            st.error("Backup não encontrado!")

# Filtragem dos action plans
filtered_plans = action_plans

if show_edited:
    filtered_plans = [ap for ap in filtered_plans if ap['title']
                      != ap['original_title'] or ap['text'] != ap['original_text']]

if show_pending:
    filtered_plans = [ap for ap in filtered_plans if ap['title'] ==
                      ap['original_title'] and ap['text'] == ap['original_text']]

if search_term:
    filtered_plans = [ap for ap in filtered_plans if
                      search_term.lower() in ap['itemNumber'].lower() or
                      search_term.lower() in ap['specificRequirementDescription'].lower()]

# Exibição dos action plans
st.subheader(f"📝 Action Plans ({len(filtered_plans)} de {total_plans})")

if not filtered_plans:
    st.info("Nenhum action plan encontrado com os filtros aplicados.")

for i, ap in enumerate(filtered_plans):
    # Determina status
    is_edited = ap['title'] != ap['original_title'] or ap['text'] != ap['original_text']
    status_class = "status-edited" if is_edited else "status-pending"
    status_text = "✓ Editado" if is_edited else "⏳ Pendente"

    with st.container():
        st.markdown(f"""
        <div class="action-plan-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3>ActionPlan #{i+1}</h3>
                <span class="status-badge {status_class}">{status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"**Item Number:** `{ap['itemNumber']}`")
            st.markdown(
                f"**Descrição:** {ap['specificRequirementDescription'][:100]}{'...' if len(ap['specificRequirementDescription']) > 100 else ''}")

            # Mostra diferenças se editado
            if is_edited:
                with st.expander("🔍 Ver diferenças"):
                    if ap['title'] != ap['original_title']:
                        st.markdown("**Título alterado:**")
                        st.markdown(f"**Antes:** {ap['original_title']}")
                        st.markdown(f"**Depois:** {ap['title']}")
                    if ap['text'] != ap['original_text']:
                        st.markdown("**Texto alterado:**")
                        st.markdown(f"**Antes:** {ap['original_text']}")
                        st.markdown(f"**Depois:** {ap['text']}")

        with col2:
            # Campos de edição
            new_title = st.text_input(
                f"Título {i+1}",
                value=ap['title'],
                key=f"title_{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}",
                help="Edite o título do action plan"
            )

            new_text = st.text_area(
                f"Texto {i+1}",
                value=ap['text'],
                key=f"text_{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}",
                height=100,
                help="Edite o texto do action plan"
            )

            # Atualiza os dados
            ap['title'] = new_title
            ap['text'] = new_text

            # Salva automaticamente se houve mudança
            if new_title != ap['original_title'] or new_text != ap['original_text']:
                # Salva progresso
                progress[f"{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}"] = {
                    'title': new_title,
                    'text': new_text,
                    'timestamp': datetime.now().isoformat()
                }
                save_progress(progress)

        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>💡 Dica: As alterações são salvas automaticamente. Use os filtros para navegar mais facilmente.</p>
    <p>🔄 Para restaurar o arquivo original, use o botão "Restaurar Backup" na barra lateral.</p>
</div>
""", unsafe_allow_html=True)

# Auto-save a cada 30 segundos
if st.button("🔄 Atualizar", key="refresh"):
    st.rerun()

# Timer para auto-save
if 'last_save' not in st.session_state:
    st.session_state.last_save = time.time()

if time.time() - st.session_state.last_save > 30:  # 30 segundos
    save_changes(data, action_plans)
    st.session_state.last_save = time.time()

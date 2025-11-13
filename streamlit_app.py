import streamlit as st
import json
import os
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Editor ActionPlan - Tecomat 010",
    page_icon="💾",
    layout="wide"
)

# Caminhos dos arquivos
JSON_PATH = 'SGQP-Tecomat.norms13.11.2025.json'
EDITADOS_PATH = 'edicoes_salvas.json'

# CSS
st.markdown("""
<style>
    .header {
        background: linear-gradient(90deg, #4CAF50, #45a049);
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
    .status-editado {
        background-color: #d4edda;
        color: #155724;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    .status-pendente {
        background-color: #fff3cd;
        color: #856404;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
    }
    .auto-save-indicator {
        background-color: #e7f3ff;
        color: #0066cc;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar edições salvas


def carregar_edicoes_salvas():
    """Carrega as edições que foram salvas anteriormente"""
    if os.path.exists(EDITADOS_PATH):
        try:
            with open(EDITADOS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# Função para salvar edições


def salvar_edicoes(edicoes):
    """Salva as edições em arquivo local"""
    try:
        with open(EDITADOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(edicoes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

# Função para carregar dados originais


@st.cache_data
def carregar_dados_originais():
    """Carrega os dados originais do JSON"""
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error(f'Arquivo {JSON_PATH} não encontrado!')
        st.stop()

# Função para extrair action plans


def extrair_action_plans(data):
    """Extrai todos os action plans"""
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
data_original = carregar_dados_originais()
action_plans = extrair_action_plans(data_original)
edicoes_salvas = carregar_edicoes_salvas()

# Aplicar edições salvas aos action plans
for ap in action_plans:
    chave = f"{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}"
    if chave in edicoes_salvas:
        ap['title'] = edicoes_salvas[chave].get('title', ap['title'])
        ap['text'] = edicoes_salvas[chave].get('text', ap['text'])

# Header principal
st.markdown("""
<div class="header">
    <h1>💾 Editor ActionPlan - Tecomat</h1>
    <p>Suas edições são salvas automaticamente e não se perdem!</p>
</div>
""", unsafe_allow_html=True)

# Indicador de auto-save
if 'ultimo_save' not in st.session_state:
    st.session_state.ultimo_save = time.time()

tempo_desde_save = time.time() - st.session_state.ultimo_save
if tempo_desde_save < 30:  # Mostra por 30 segundos
    st.markdown("""
    <div class="auto-save-indicator">
        💾 Salvamento automático ativo - Suas edições estão seguras!
    </div>
    """, unsafe_allow_html=True)

# Sidebar
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

    # Botão para salvar manualmente
    if st.button("💾 SALVAR AGORA", type="primary", use_container_width=True):
        # Aplicar todas as mudanças
        for ap in action_plans:
            chave = f"{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}"
            edicoes_salvas[chave] = {
                'title': ap['title'],
                'text': ap['text'],
                'timestamp': datetime.now().isoformat()
            }

        if salvar_edicoes(edicoes_salvas):
            st.success("✅ Todas as edições salvas com sucesso!")
            st.session_state.ultimo_save = time.time()
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

# Função para salvar edição individual


def salvar_edicao_individual(ap, novo_titulo, novo_texto):
    """Salva uma edição individual"""
    chave = f"{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}"

    # Só salva se houve mudança
    if novo_titulo != ap['original_title'] or novo_texto != ap['original_text']:
        edicoes_salvas[chave] = {
            'title': novo_titulo,
            'text': novo_texto,
            'timestamp': datetime.now().isoformat()
        }
    else:
        # Remove se voltou ao original
        edicoes_salvas.pop(chave, None)

    # Salva automaticamente
    salvar_edicoes(edicoes_salvas)
    st.session_state.ultimo_save = time.time()


for i, ap in enumerate(filtrados):
    # Verificar se foi editado
    foi_editado = ap['title'] != ap['original_title'] or ap['text'] != ap['original_text']
    status = "✅ Editado" if foi_editado else "⏳ Pendente"
    status_class = "status-editado" if foi_editado else "status-pendente"

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
            # Verifica se há outros ActionPlans com a mesma descrição
            descricao_atual = ap['descricao']
            duplicados = [
                ap2 for ap2 in action_plans if ap2['descricao'] == descricao_atual]
            edicao_em_grupo = False
            mostrar_checkbox = len(duplicados) > 1
            if mostrar_checkbox:
                edicao_em_grupo = st.checkbox(
                    f"Aplicar para todos os {len(duplicados)} ActionPlans com esta descrição?",
                    key=f"grupo_{ap['obj_idx']}_{ap['req_idx']}_{ap['ap_idx']}"
                )

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

            # Salvar automaticamente se houve mudança
            if novo_titulo != ap['title'] or novo_texto != ap['text']:
                if mostrar_checkbox and edicao_em_grupo:
                    # Edição em grupo: propaga para todos com a mesma descrição
                    for ap2 in duplicados:
                        ap2['title'] = novo_titulo
                        ap2['text'] = novo_texto
                        salvar_edicao_individual(ap2, novo_titulo, novo_texto)
                else:
                    # Edição individual
                    ap['title'] = novo_titulo
                    ap['text'] = novo_texto
                    salvar_edicao_individual(ap, novo_titulo, novo_texto)

        st.markdown("---")

# Seção de download
st.markdown("---")
st.header("📤 Baixar Arquivo Final")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📥 Arquivo Completo")
    # Criar arquivo final com as edições aplicadas
    data_final = data_original.copy()
    for ap in action_plans:
        if ap['title'] != ap['original_title'] or ap['text'] != ap['original_text']:
            data_final[ap['obj_idx']]['requirements'][ap['req_idx']
                                                      ]['actionPlan'][ap['ap_idx']]['title'] = ap['title']
            data_final[ap['obj_idx']]['requirements'][ap['req_idx']
                                                      ]['actionPlan'][ap['ap_idx']]['text'] = ap['text']

    json_str = json.dumps(data_final, ensure_ascii=False, indent=2)
    st.download_button(
        label="📥 BAIXAR JSON COMPLETO",
        data=json_str,
        file_name=f'ActionPlan_Final_{datetime.now().strftime("%d-%m-%Y_%H%M")}.json',
        mime='application/json',
        use_container_width=True
    )

with col2:
    st.markdown("### 📊 Apenas Edições")
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
    st.markdown("### 📋 Relatório")
    # Criar relatório
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

# Instruções
st.markdown("---")
st.markdown("""
### 💾 Sistema de Persistência

**✅ Suas edições são salvas automaticamente:**
- Cada mudança é salva instantaneamente
- Mesmo se o site for suspenso, suas edições ficam seguras
- Ao abrir o site novamente, as edições são carregadas automaticamente

**📤 Para enviar:**
- Baixe o "JSON COMPLETO" quando terminar
- Envie por email ou WhatsApp
""")

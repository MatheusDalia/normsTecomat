import streamlit as st
import json
import os
from io import StringIO

# Caminho do arquivo JSON
JSON_PATH = 'SGQP-Tecomat.norms.json'

st.title('Editor de ActionPlan (title e text)')

# Carregar o JSON
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
else:
    st.error(f'Arquivo {JSON_PATH} não encontrado.')
    st.stop()

# Função para extrair todos os actionPlans
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
                'specificRequirementDescription': req.get('specificRequirementDescription', '')
            })

st.subheader('Edite os campos title e text de cada ActionPlan:')

for i, ap in enumerate(all_action_plans):
    st.markdown(f'**ActionPlan {i+1}**')
    st.markdown(f"**itemNumber:** `{ap['itemNumber']}`")
    st.markdown(f"**Descrição:** {ap['specificRequirementDescription']}")
    new_title = st.text_input(f'Título {i+1}', ap['title'], key=f'title_{i}')
    new_text = st.text_area(f'Texto {i+1}', ap['text'], key=f'text_{i}')
    # Atualiza na estrutura original
    data[ap['obj_idx']]['requirements'][ap['req_idx']
                                        ]['actionPlan'][ap['ap_idx']]['title'] = new_title
    data[ap['obj_idx']]['requirements'][ap['req_idx']
                                        ]['actionPlan'][ap['ap_idx']]['text'] = new_text
    st.markdown('---')

# Botão para salvar alterações
if st.button('Salvar alterações no arquivo'):
    try:
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        st.success('Arquivo salvo com sucesso!')
    except Exception as e:
        st.error(f'Erro ao salvar: {e}')

# Botão para baixar o JSON editado
json_str = json.dumps(data, ensure_ascii=False, indent=2)
st.download_button('Baixar JSON editado', data=json_str,
                   file_name='SGQP-Tecomat.norms.editado.json', mime='application/json')

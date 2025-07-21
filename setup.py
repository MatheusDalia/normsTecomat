#!/usr/bin/env python3
"""
Script de configuração inicial para o Editor de ActionPlan
"""

import os
import json
import shutil
from datetime import datetime
import sys


def check_requirements():
    """Verifica se os arquivos necessários existem"""
    required_files = ['SGQP-Tecomat.norms.json']
    missing_files = []

    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("❌ Arquivos necessários não encontrados:")
        for file in missing_files:
            print(f"   - {file}")
        return False

    print("✅ Todos os arquivos necessários encontrados")
    return True


def create_backup():
    """Cria backup inicial"""
    source_file = 'SGQP-Tecomat.norms.json'
    backup_file = f'SGQP-Tecomat.norms.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

    try:
        shutil.copy2(source_file, backup_file)
        print(f"✅ Backup criado: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return None


def validate_json():
    """Valida se o JSON está correto"""
    try:
        with open('SGQP-Tecomat.norms.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Verifica se tem actionPlans
        action_plan_count = 0
        for obj in data:
            requirements = obj.get('requirements', [])
            for req in requirements:
                action_plans = req.get('actionPlan', [])
                action_plan_count += len(action_plans)

        print(f"✅ JSON válido - {action_plan_count} ActionPlans encontrados")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro ao validar JSON: {e}")
        return False


def create_config():
    """Cria arquivo de configuração"""
    config = {
        'last_setup': datetime.now().isoformat(),
        'version': '2.0',
        'auto_save': True,
        'backup_interval': 30,
        'max_backups': 5
    }

    try:
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print("✅ Arquivo de configuração criado")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar configuração: {e}")
        return False


def show_instructions():
    """Mostra instruções de uso"""
    print("\n" + "="*50)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA!")
    print("="*50)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Execute: streamlit run edit_json_streamlit_improved.py")
    print("2. Abra o navegador no endereço mostrado")
    print("3. Use a sidebar para navegar e filtrar")
    print("4. As alterações são salvas automaticamente")
    print("\n💡 DICAS:")
    print("- Sempre crie backup antes de grandes edições")
    print("- Use os filtros para trabalhar em grupos")
    print("- Baixe o arquivo final quando concluir")
    print("\n🆘 EM CASO DE PROBLEMAS:")
    print("- Execute: python backup_manager.py")
    print("- Verifique se o arquivo JSON existe")
    print("- Use a função de restauração se necessário")


def main():
    """Função principal"""
    print("🔧 CONFIGURAÇÃO INICIAL - EDITOR ACTIONPLAN")
    print("="*50)

    # Verifica arquivos
    if not check_requirements():
        print("\n❌ Configuração falhou. Verifique se o arquivo JSON existe.")
        sys.exit(1)

    # Valida JSON
    if not validate_json():
        print("\n❌ JSON inválido. Verifique o arquivo.")
        sys.exit(1)

    # Cria backup
    backup_file = create_backup()
    if not backup_file:
        print("\n❌ Erro ao criar backup.")
        sys.exit(1)

    # Cria configuração
    if not create_config():
        print("\n⚠️ Erro ao criar configuração, mas pode continuar.")

    # Mostra instruções
    show_instructions()


if __name__ == "__main__":
    main()

import json
import os
import shutil
from datetime import datetime
import streamlit as st


def create_initial_backup():
    """Cria backup inicial do arquivo JSON"""
    source_file = 'SGQP-Tecomat.norms.json'
    backup_file = f'SGQP-Tecomat.norms.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

    if os.path.exists(source_file):
        shutil.copy2(source_file, backup_file)
        print(f"Backup criado: {backup_file}")
        return backup_file
    else:
        print(f"Arquivo {source_file} não encontrado")
        return None


def list_backups():
    """Lista todos os backups disponíveis"""
    backups = []
    for file in os.listdir('.'):
        if file.startswith('SGQP-Tecomat.norms.backup_') and file.endswith('.json'):
            file_path = os.path.join('.', file)
            stat = os.stat(file_path)
            backups.append({
                'filename': file,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime)
            })

    return sorted(backups, key=lambda x: x['created'], reverse=True)


def restore_backup(backup_filename):
    """Restaura um backup específico"""
    if os.path.exists(backup_filename):
        shutil.copy2(backup_filename, 'SGQP-Tecomat.norms.json')
        print(f"Backup {backup_filename} restaurado com sucesso")
        return True
    else:
        print(f"Backup {backup_filename} não encontrado")
        return False


def cleanup_old_backups(keep_count=5):
    """Remove backups antigos, mantendo apenas os mais recentes"""
    backups = list_backups()
    if len(backups) > keep_count:
        for backup in backups[keep_count:]:
            try:
                os.remove(backup['filename'])
                print(f"Backup removido: {backup['filename']}")
            except Exception as e:
                print(f"Erro ao remover {backup['filename']}: {e}")


if __name__ == "__main__":
    print("=== Gerenciador de Backup ===")
    print("1. Criar backup inicial")
    print("2. Listar backups")
    print("3. Restaurar backup")
    print("4. Limpar backups antigos")

    choice = input("Escolha uma opção (1-4): ")

    if choice == "1":
        backup_file = create_initial_backup()
        if backup_file:
            print(f"✅ Backup criado: {backup_file}")

    elif choice == "2":
        backups = list_backups()
        if backups:
            print("\nBackups disponíveis:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['filename']}")
                print(f"   Tamanho: {backup['size']} bytes")
                print(f"   Criado: {backup['created']}")
                print()
        else:
            print("Nenhum backup encontrado")

    elif choice == "3":
        backups = list_backups()
        if backups:
            print("\nBackups disponíveis:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['filename']}")

            try:
                idx = int(
                    input("Escolha o número do backup para restaurar: ")) - 1
                if 0 <= idx < len(backups):
                    if restore_backup(backups[idx]['filename']):
                        print("✅ Backup restaurado com sucesso!")
                    else:
                        print("❌ Erro ao restaurar backup")
                else:
                    print("❌ Opção inválida")
            except ValueError:
                print("❌ Entrada inválida")
        else:
            print("Nenhum backup encontrado")

    elif choice == "4":
        keep = input("Quantos backups manter? (padrão: 5): ")
        try:
            keep_count = int(keep) if keep else 5
            cleanup_old_backups(keep_count)
            print(
                f"✅ Limpeza concluída. Mantidos os {keep_count} backups mais recentes")
        except ValueError:
            print("❌ Entrada inválida")

    else:
        print("❌ Opção inválida")

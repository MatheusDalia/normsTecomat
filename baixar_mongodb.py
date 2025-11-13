#!/usr/bin/env python3
"""
Script para baixar dados do MongoDB
"""

from pymongo import MongoClient
import json
from datetime import datetime
import os


def baixar_norms_mongodb():
    """Baixa os dados norms do MongoDB"""

    print("🔄 Conectando ao MongoDB...")

    # CONFIGURAR AQUI SUA CONNECTION STRING
    # Exemplo: "mongodb://localhost:27017/"
    # Ou: "mongodb+srv://usuario:senha@cluster.mongodb.net/"
    CONNECTION_STRING = input("📝 Digite sua connection string do MongoDB: ")
    DATABASE_NAME = input("📝 Digite o nome do banco de dados: ")
    COLLECTION_NAME = input("📝 Digite o nome da collection (ex: norms): ")

    try:
        # Conectar
        client = MongoClient(CONNECTION_STRING)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        print("✅ Conectado com sucesso!")

        # Contar documentos
        total = collection.count_documents({})
        print(f"📊 Total de documentos encontrados: {total}")

        if total == 0:
            print("❌ Nenhum documento encontrado!")
            return

        # Baixar todos os documentos
        print("⬇️ Baixando dados...")
        documentos = list(collection.find({}))

        # Gerar nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"norms_mongodb_{timestamp}.json"

        # Salvar arquivo
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(documentos, f, ensure_ascii=False, indent=2, default=str)

        print(f"✅ Arquivo salvo: {nome_arquivo}")
        print(f"📂 Localização: {os.path.abspath(nome_arquivo)}")
        print(f"📊 Tamanho: {os.path.getsize(nome_arquivo)} bytes")

    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\n💡 Dicas:")
        print("- Verifique se a connection string está correta")
        print("- Verifique se você tem acesso ao banco")
        print("- Instale pymongo: pip install pymongo")

    finally:
        try:
            client.close()
        except:
            pass


def verificar_dependencias():
    """Verifica se pymongo está instalado"""
    try:
        import pymongo
        print(f"✅ PyMongo instalado - versão: {pymongo.__version__}")
        return True
    except ImportError:
        print("❌ PyMongo não encontrado!")
        print("🔧 Para instalar: pip install pymongo")
        return False


if __name__ == "__main__":
    print("🔽 BAIXAR NORMS DO MONGODB")
    print("=" * 40)

    if not verificar_dependencias():
        exit(1)

    baixar_norms_mongodb()

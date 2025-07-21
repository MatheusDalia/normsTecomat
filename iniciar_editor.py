#!/usr/bin/env python3
"""
Script para iniciar o editor simples e gerar link de compartilhamento
"""

import subprocess
import socket
import time
import webbrowser
import os
import sys


def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        # Conecta a um servidor externo para descobrir o IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"


def check_port_available(port):
    """Verifica se a porta está disponível"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0
    except:
        return False


def find_available_port(start_port=8501):
    """Encontra uma porta disponível"""
    port = start_port
    while not check_port_available(port):
        port += 1
    return port


def main():
    print("🚀 Iniciando Editor Simples para o Gerente")
    print("=" * 50)

    # Verificar se o arquivo existe
    if not os.path.exists('SGQP-Tecomat.norms.json'):
        print("❌ Arquivo SGQP-Tecomat.norms.json não encontrado!")
        print("Certifique-se de que o arquivo está na mesma pasta.")
        sys.exit(1)

    # Encontrar porta disponível
    port = find_available_port()
    local_ip = get_local_ip()

    print(f"📁 Arquivo JSON encontrado")
    print(f"🌐 IP Local: {local_ip}")
    print(f"🔌 Porta: {port}")
    print(f"🔗 Link local: http://localhost:{port}")
    print(f"🔗 Link rede: http://{local_ip}:{port}")

    print("\n📋 INSTRUÇÕES PARA COMPARTILHAR:")
    print("=" * 50)
    print("1. Se o gerente estiver na mesma rede WiFi:")
    print(f"   Envie este link: http://{local_ip}:{port}")
    print("\n2. Se o gerente estiver em rede diferente:")
    print("   Use ngrok ou similar para criar um link público")
    print("\n3. Para usar ngrok (se instalado):")
    print(f"   ngrok http {port}")

    print("\n🎯 COMO O GERENTE USA:")
    print("=" * 50)
    print("1. Abre o link no navegador")
    print("2. Edita os campos de título e texto")
    print("3. Clica em 'SALVAR TUDO'")
    print("4. Baixa o arquivo 'JSON COMPLETO'")
    print("5. Te envia por email/WhatsApp")

    print(f"\n⏳ Iniciando servidor na porta {port}...")
    print("Pressione Ctrl+C para parar")

    try:
        # Iniciar Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "editor_simples.py",
            "--server.port", str(port),
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]

        # Abrir navegador automaticamente
        time.sleep(2)
        webbrowser.open(f"http://localhost:{port}")

        # Executar o comando
        subprocess.run(cmd)

    except KeyboardInterrupt:
        print("\n\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""run_on_tag.py

Listen for RFID tag reads and execute mapped shell commands when a tag is detected.

Usage:
  - Copy `tag_commands.json.example` to `tag_commands.json` and edit mappings.
  - Run: python run_on_tag.py

Notes:
  - Designed to run on Raspberry Pi with `mfrc522` and `RPi.GPIO` installed.
  - For testing without hardware, pass --simulate to simulate a tag read.
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
import time

try:
    from mfrc522 import SimpleMFRC522
    import RPi.GPIO as GPIO
    HAS_HARDWARE = True
except Exception:
    HAS_HARDWARE = False


DEFAULT_MAPPING_FILE = os.path.join(os.path.dirname(__file__), 'tag_commands.json')


def load_mappings(path):
    if not os.path.exists(path):
        print(f"Mapping file not found: {path}")
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_command(command, shell=False):
    """Execute a command. If shell=False, command is split using shlex."""
    print(f"→ Executando comando: {command}")
    try:
        if shell:
            completed = subprocess.run(command, shell=True)
        else:
            parts = shlex.split(command)
            completed = subprocess.run(parts)
        print(f"Comando finalizado com código: {completed.returncode}")
    except Exception as e:
        print(f"Erro ao executar comando: {e}")


def listen_and_run(mapping, simulate_tag=None, once=False):
    """Listen for tags and execute mapped commands.

    mapping: dict where keys are tag IDs (as strings) and values are either a string command or
             an object {"command": "...", "shell": true/false}
    """

    if not HAS_HARDWARE and simulate_tag is None:
        print("Aviso: bibliotecas de hardware não encontradas; use --simulate para testes.")
        return

    leitor = None
    try:
        if HAS_HARDWARE:
            leitor = SimpleMFRC522()

        while True:
            if simulate_tag is not None:
                tag_id = str(simulate_tag)
                tag_text = "(simulado)"
                print(f"Simulando leitura da tag {tag_id}")
            else:
                print("Aproxime a tag do leitor...")
                id, texto = leitor.read()
                tag_id = str(id)
                tag_text = texto.strip() if texto else ""

            print(f"Tag detectada: ID={tag_id} texto={tag_text}")

            entry = mapping.get(tag_id)
            if entry:
                if isinstance(entry, str):
                    run_command(entry)
                elif isinstance(entry, dict):
                    cmd = entry.get('command')
                    shell = bool(entry.get('shell', False))
                    run_command(cmd, shell=shell)
                else:
                    print(f"Formato inválido para o mapeamento da tag {tag_id}")
            else:
                print("Nenhum comando mapeado para essa tag.")

            if once or simulate_tag is not None:
                break

            print("Aguardando próximo leitura em 1s...\n")
            time.sleep(1)

    finally:
        if HAS_HARDWARE:
            GPIO.cleanup()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Executa comandos quando uma tag RFID é detectada')
    parser.add_argument('--mappings', '-m', default=DEFAULT_MAPPING_FILE, help='Arquivo JSON com mapeamento tag->comando')
    parser.add_argument('--simulate', '-s', help='Simular tag com o ID fornecido (apenas para testes)')
    parser.add_argument('--once', action='store_true', help='Ler apenas uma vez e sair')
    args = parser.parse_args(argv)

    mapping = load_mappings(args.mappings)
    listen_and_run(mapping, simulate_tag=args.simulate, once=args.once)


if __name__ == '__main__':
    main()

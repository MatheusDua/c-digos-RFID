# run_on_tag

Script para executar comandos quando uma tag RFID é detectada.

Como usar:

1. Copie o arquivo de exemplo:

   cp tag_commands.json.example tag_commands.json

2. Edite `tag_commands.json` e mapeie IDs de tag para comandos. Exemplo:

   {
     "123456789": "echo 'Tag detectada'",
     "999888777": { "command": "python meu_script.py", "shell": false }
   }

3. Execute o script (no Raspberry Pi com as bibliotecas instaladas):

   python run_on_tag.py

Opções úteis:

- `--mappings` ou `-m` : caminho para arquivo JSON de mapeamento
- `--simulate` ou `-s` : simula a leitura de uma tag (use o ID como string)
- `--once` : ler uma vez e sair

Exemplo (simulação):

```powershell
python run_on_tag.py --simulate 123456789 --once
```

Observações:

- O script tenta importar `mfrc522` e `RPi.GPIO`. Se as bibliotecas não estiverem disponíveis
  (por exemplo, desenvolvendo em Windows), use `--simulate` para testar a lógica.
- Para integrações com `painel.py`, basta chamar `run_on_tag.py` em background ou a partir da
  interface Kivy (ex.: subprocess.Popen).

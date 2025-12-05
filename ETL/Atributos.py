import csv, requests
URL_DADOS_GPU = "https://raw.githubusercontent.com/voidful/gpu-info-api/gpu-data/gpu.json"

resposta = requests.get(URL_DADOS_GPU)
resposta.raise_for_status() # Levantar uma exceção para erros HTTP
dados_gpu = resposta.json()

atributos_unicos = set()

if isinstance(dados_gpu, dict):
    for chave_entrada_gpu, valor_entrada_gpu in dados_gpu.items():
        if isinstance(valor_entrada_gpu, dict):
            atributos_unicos.update(valor_entrada_gpu.keys())
elif isinstance(dados_gpu, list):
    for item in dados_gpu:
        if isinstance(item, dict):
            atributos_unicos.update(item.keys())

# Classificar os atributos
atributos_ordenados = sorted(list(atributos_unicos))

# Definir o nome do arquivo CSV
nome_arquivo_csv = 'atributos.csv'

# Escrever os atributos no arquivo CSV
with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    # Escrever um cabeçalho (opcional)
    escritor_csv.writerow(['Atributo'])
    for atributo in atributos_ordenados:
        escritor_csv.writerow([atributo])

print(f"Os atributos foram salvos em '{nome_arquivo_csv}' com sucesso.") 
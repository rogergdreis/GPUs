import csv
import os

# Nomes dos arquivos
arquivo_entrada = 'GPU_ETL.csv'
arquivo_saida = 'VRAM_Evo.csv'

# Colunas que queremos extrair (devem ser idênticas ao cabeçalho do GPU_ETL.csv)
# Nota: No passo anterior, nomeamos a coluna de VRAM como "VRAM (GB)"
colunas_alvo = ['Modelo', 'Lançamento', 'VRAM (GB)']

def gerar_vram_evo():
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado. Rode o script anterior primeiro.")
        return

    dados_filtrados = []

    try:
        with open(arquivo_entrada, mode='r', encoding='utf-8') as f_in:
            leitor = csv.DictReader(f_in)
            
            # Verifica se as colunas existem no arquivo original
            if not all(col in leitor.fieldnames for col in colunas_alvo):
                print(f"Erro: O arquivo de entrada não tem as colunas esperadas: {colunas_alvo}")
                print(f"Colunas encontradas: {leitor.fieldnames}")
                return

            for linha in leitor:
                # 1. Extrai apenas os valores das colunas alvo
                modelo = linha.get('Modelo')
                lancamento = linha.get('Lançamento')
                vram = linha.get('VRAM (GB)')

                # 2. Critério de Validação:
                # Verifica se todos os campos existem e não são strings vazias
                if modelo and modelo.strip() and \
                   lancamento and lancamento.strip() and \
                   vram and vram.strip():
                    
                    dados_filtrados.append({
                        'Modelo': modelo,
                        'Lançamento': lancamento,
                        'VRAM (GB)': vram
                    })

        # 3. Escreve o novo arquivo apenas se houver dados
        if dados_filtrados:
            with open(arquivo_saida, mode='w', newline='', encoding='utf-8') as f_out:
                escritor = csv.DictWriter(f_out, fieldnames=colunas_alvo)
                escritor.writeheader()
                escritor.writerows(dados_filtrados)
            
            print(f"Sucesso! Arquivo '{arquivo_saida}' gerado.")
            print(f"Total de linhas processadas: {len(dados_filtrados)}")
        else:
            print("Aviso: Nenhuma linha atendeu aos critérios (todas tinham algum campo vazio).")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    gerar_vram_evo()
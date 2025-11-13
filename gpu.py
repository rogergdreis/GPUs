import pandas as pd
import sys
import requests
import numpy as np
import re
import warnings

# Nome do arquivo CSV de saída
OUTPUT_CSV = "lista_de_chaves_usadas.csv"

# 1. Estas são todas as listas de chaves (atributos) extraidas do arquivo json

listas_de_chaves = [
    # Modelo
    ['Model name', 'Model', 'Model (Codename)', 'Model (Code name)',
     'Model name (Architecture)', 'Branding and Model',
     'Branding and Model Branding and Model.1'],

    # Codigo
    ['Code name', 'Code name(s)', 'Codename', 'Model (codename)',
     'Code name (console model)', 'GPU code name and/or architecture'],

    # Data
    ['Launch'],

    # Preço
    ['Release Price (USD)', 'Release price (USD) MSRP',
     'Release price (USD) Founders Edition', 'Release price (USD)'],

    # Clock do Processador
    ['Clock rate Base (MHz)', 'Clock Speeds Base (MHz)',
     'Clock speeds Base core (MHz)', 'Clock speeds Base core clock (MHz)',
     'Core Clock (MHz) Base', 'Clock speeds Boost core (MHz)',
     'Clock speeds Boost core clock (MHz)', 'Core Clock (MHz) Turbo',
     'Clock rate (MHz) Boost (MHz)', 'Clock speeds Boost clock (MHz)',
     'Core clock (MHz)', 'Clock rate Core (MHz)', 'Clock speed Core (MHz)',
     'Core Clock (MHz)', 'Core Clock rate (MHz)', 'Clock rate (MHz) Core (MHz)',
     'Clock rate (MHz)'],

    # Clock da Memoria
    ['Memory clock (MHz)', 'Clock rate Memory (MHz)', 'Clock speed Memory (MHz)',
     'Memory Clock', 'Memory Effective clock (MHz)', 'Memory Clock (MHz)',
     'Memory (MHz)'],

    # VRAM
    ['Memory Size (MiB)', 'Memory configuration Size (MiB)',
     'Memory configuration Size (GiB)', 'Memory Size (GiB)',
     'Memory Size (GB)', 'Memory Size', 'Memory Size (KiB)', 'Memory Size (MB)'],

    # Tipo de Memoria
    ['Memory Bus type', 'Memory configuration DRAM type', 'Memory Type',
     'Memory RAM type'],

    # Barramento
    ['Memory Bus width (bit)', 'Memory configuration Bus width (bit)',
     'Memory Bus width', 'Memory Bus width (Bit)'],

    # TDP
    ['TDP (Watts)', 'TDP (W)', 'TDP', 'TDP (Watts) Max.', 'TDP (Watts) Max',
     'TDP (Watts) Idle', 'TDP (W) Idle Max', 'TDP /idle (Watts)',
     'TDP /idle (watts)'],

    # Compostos e Vendor
    ['Release Date & Price', 'Vendor']
]

def criar_lista_de_chaves():
    """
    Pega todas as chaves de normalização, remove duplicatas e salva em CSV.
    """

    print("Coletando todas as chaves de normalização especificadas...")

    # Usamos 'set' para garantir que cada nome de chave apareça apenas uma vez
    chaves_unicas = set()

    # Adiciona todos os itens de todas as listas ao 'set'
    for lista in listas_de_chaves:
        chaves_unicas.update(lista)

    # Converte o 'set' de volta para uma lista e ordena
    lista_final_chaves = sorted(list(chaves_unicas))

    print(f"Total de {len(lista_final_chaves)} nomes de atributos únicos encontrados.")

    # Cria um DataFrame do Pandas com uma única coluna
    df = pd.DataFrame(lista_final_chaves, columns=['Atributo_Fonte_JSON'])

    # Salva o DataFrame em um arquivo CSV
    try:
        df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
        print(f"\nArquivo '{OUTPUT_CSV}' criado com sucesso!")
        print("Amostra dos atributos (5 primeiros):")
        print(df.head())

    except Exception as e:
        print(f"Ocorreu um erro ao salvar o CSV: {e}", file=sys.stderr)

# --- Executa a função ---
if __name__ == "__main__":
    criar_lista_de_chaves()

# URL da "API" JSON
URL_GPU_DATA = "https://raw.githubusercontent.com/voidful/gpu-info-api/gpu-data/gpu.json"
OUTPUT_CSV = "GPUs_final.csv"

# --- Listas ---

# 1. Modelo
COLS_MODELO = [
    'Model', 'Model (Code name)', 'Model (Codename)', 'Model (codename)',
    'Model name', 'Model name (Architecture)', 'Branding and Model',
    'Branding and Model Branding and Model.1', 'GPU code name and/or architecture'
]
# 2. Código
COLS_CODIGO = [
    'Code name', 'Code name (console model)', 'Code name(s)', 'Codename',
    'GPU code name and/or architecture'
]
# 3. Preço
COLS_PRECO = [
    'Release Price (USD)', 'Release price (USD)',
    'Release price (USD) Founders Edition', 'Release price (USD) MSRP'
]
# 4. Clock GPU (Ordem: Base, Genérico, Boost)
COLS_CLOCK_GPU = [
    'Clock Speeds Base (MHz)', 'Clock rate Base (MHz)',
    'Clock speeds Base core (MHz)', 'Clock speeds Base core clock (MHz)',
    'Core Clock (MHz) Base', 'Clock rate (MHz)', 'Clock rate (MHz) Core (MHz)',
    'Clock rate Core (MHz)', 'Clock speed Core (MHz)', 'Core Clock (MHz)',
    'Core Clock rate (MHz)', 'Core clock (MHz)', 'Clock rate (MHz) Boost (MHz)',
    'Clock speeds Boost clock (MHz)', 'Clock speeds Boost core (MHz)',
    'Clock speeds Boost core clock (MHz)', 'Core Clock (MHz) Turbo'
]
# 5. Clock VRAM
COLS_CLOCK_MEM = [
    'Memory (MHz)', 'Memory Clock', 'Memory Clock (MHz)', 'Memory clock (MHz)',
    'Clock rate Memory (MHz)', 'Clock speed Memory (MHz)', 'Memory Effective clock (MHz)'
]
# 6. VRAM (Tamanho)
COLS_VRAM = [
    'Memory Size', 'Memory Size (GB)', 'Memory Size (GiB)',
    'Memory Size (KiB)', 'Memory Size (MB)', 'Memory Size (MiB)',
    'Memory configuration Size (GiB)', 'Memory configuration Size (MiB)'
]
# 7. Tipo de Memória
COLS_TIPO_MEM = [
    'Memory Bus type', 'Memory RAM type', 'Memory Type',
    'Memory configuration DRAM type'
]
# 8. Bus (Barramento)
COLS_BARRAMENTO = [
    'Memory Bus width', 'Memory Bus width (Bit)', 'Memory Bus width (bit)',
    'Memory configuration Bus width (bit)'
]
# 9. TDP (Ordem: Máximo, Ocioso)
COLS_TDP = [
    'TDP', 'TDP (W)', 'TDP (Watts)', 'TDP (Watts) Max', 'TDP (Watts) Max.',
    'TDP (W) Idle Max', 'TDP (Watts) Idle', 'TDP /idle (Watts)', 'TDP /idle (watts)'
]

# --- Funções Auxiliares de Normalização ---

# (O pré-processamentofará com que 'pd.notna()' funcione como esperado)

def find_first_value(row, column_list):
    """
    Percorre uma lista de colunas e retorna o primeiro valor não-nulo.
    """
    for col in column_list:
        # pd.notna() agora funciona, pois "nan" (string) virou np.nan (real)
        if col in row.index and pd.notna(row[col]):
            return row[col]
    return np.nan

def parse_lancamento(row):
    """
    Busca a data, primeiro em 'Launch', depois no campo composto.
    Formata para dd/mm/YYYY.
    """
    if 'Launch' in row.index and pd.notna(row['Launch']):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                date_obj = pd.to_datetime(row['Launch'], errors='raise')
                return date_obj.strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            pass

    if 'Release Date & Price' in row.index and pd.notna(row['Release Date & Price']):
        text = str(row['Release Date & Price'])
        date_text = re.sub(r'[;\$].*', '', text).strip()
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                date_obj = pd.to_datetime(date_text, errors='raise')
                return date_obj.strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            pass

    return pd.NaT

def parse_preco(row, column_list):
    """
    Busca o preço, primeiro na lista de colunas, depois no campo composto.
    """
    preco = find_first_value(row, column_list)
    if pd.notna(preco):
        if isinstance(preco, str):
            preco = preco.replace('$', '').replace(',', '')
        try:
            return float(preco)
        except (ValueError, TypeError):
            pass

    if 'Release Date & Price' in row.index and pd.notna(row['Release Date & Price']):
        text = str(row['Release Date & Price'])
        match = re.search(r'[\$](\d+[\,\d]*)', text)
        if match:
            try:
                return float(match.group(1).replace(',', ''))
            except (ValueError, TypeError):
                pass

    return np.nan

def parse_fabricante(row, index_val, modelo_val):
    """
    Define o Fabricante, inferindo do modelo ou índice se necessário.
    """
    if 'Vendor' in row.index and pd.notna(row['Vendor']):
        return row['Vendor']

    texto_busca = (str(index_val) + str(modelo_val)).lower()

    if 'nvidia' in texto_busca or 'geforce' in texto_busca or 'rtx' in texto_busca:
        return 'NVIDIA'
    if 'amd' in texto_busca or 'radeon' in texto_busca or 'rx' in texto_busca:
        return 'AMD'
    if 'intel' in texto_busca or 'arc' in texto_busca:
        return 'Intel'

    return np.nan

def parse_vram(row, column_list):
    """
    Encontra o primeiro valor de VRAM e formata a string (ex: "12 GB").
    """
    for col in column_list:
        if col in row.index and pd.notna(row[col]):
            value_str = str(row[col]).replace(',', '')
            match = re.search(r'([\d\.]+)', value_str)
            if not match:
                continue

            try:
                value_f = float(match.group(1))
                if value_f.is_integer():
                    value = int(value_f)
                else:
                    value = value_f
            except ValueError:
                continue

            col_lower = col.lower()
            if 'gib' in col_lower or 'gb' in col_lower:
                return f"{value} GB"
            if 'mib' in col_lower or 'mb' in col_lower:
                return f"{value} MB"
            if 'kib' in col_lower or 'kb' in col_lower:
                return f"{value} KB"

            if col == 'Memory Size':
                return f"{value} GB"

    return np.nan

# --- Execução Principal ---

def processar_gpus():
    print(f"Buscando dados da API em {URL_GPU_DATA}...")
    try:
        response = requests.get(URL_GPU_DATA)
        response.raise_for_status()
        dados_json = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return

    print("Dados recebidos. Convertendo para DataFrame...")
    df_raw = pd.DataFrame.from_dict(dados_json, orient='index')

    # --- [NOVA ETAPA DE LIMPEZA] ---
    # Define os padrões de texto que devem ser nulos
    # (?i) -> Ignora maiúsculas/minúsculas (ex: 'nan', 'NaN', 'NAN')
    # ^...$ -> Garante que a string inteira seja 'nan' (e não 'banana')
    # \s* -> Permite espaços em branco antes ou depois (ex: '  nan  ')

    regex_nulos = r'(?i)^\s*(nan|n/a|null)\s*$'
    regex_vazios = r'^\s*$' # Regex para strings vazias ou só com espaços

    print("Limpando valores de texto nulos (ex: 'nan', 'n/a')...")
    df_raw.replace(regex_nulos, np.nan, regex=True, inplace=True)
    df_raw.replace(regex_vazios, np.nan, regex=True, inplace=True)
    df_raw.reset_index(inplace=True)
    df_raw.rename(columns={'index': 'JSON_Index'}, inplace=True)

    print("Iniciando normalização (ETL)...")

    dados_limpos = []

    # O loop funciona como esperado, pois as strings 'nan'
    # foram convertidas para np.nan e serão puladas.

    for _, row in df_raw.iterrows():
        nova_linha = {}
        json_index = row['JSON_Index']

        # 1. Modelo
        nova_linha['Modelo'] = find_first_value(row, COLS_MODELO)
        if pd.isna(nova_linha['Modelo']):
            nova_linha['Modelo'] = json_index

        # 2. Código
        nova_linha['Código'] = find_first_value(row, COLS_CODIGO)

        # 3. Lançamento
        nova_linha['Lançamento'] = parse_lancamento(row)

        # 4. Preço
        nova_linha['Preço'] = parse_preco(row, COLS_PRECO)

        # 5. Fabricante
        nova_linha['Fabricante'] = parse_fabricante(row, json_index, nova_linha['Modelo'])

        # 6. Clock GPU (MHz)
        nova_linha['Clock GPU (MHz)'] = find_first_value(row, COLS_CLOCK_GPU)

        # 7. Clock VRAM (MHz)
        nova_linha['Clock VRAM (MHz)'] = find_first_value(row, COLS_CLOCK_MEM)

        # 8. VRAM
        nova_linha['VRAM'] = parse_vram(row, COLS_VRAM)

        # 9. Tipo
        nova_linha['Tipo'] = find_first_value(row, COLS_TIPO_MEM)

        # 10. Bus
        nova_linha['Bus'] = find_first_value(row, COLS_BARRAMENTO)

        # 11. TDP
        nova_linha['TDP'] = find_first_value(row, COLS_TDP)

        dados_limpos.append(nova_linha)

    # Criar o DataFrame final
    df_clean = pd.DataFrame(dados_limpos)

    colunas_finais = [
        'Modelo', 'Fabricante', 'Código', 'Lançamento', 'Preço',
        'Clock GPU (MHz)', 'Clock VRAM (MHz)', 'VRAM', 'Tipo', 'Bus', 'TDP'
    ]
    df_clean = df_clean[colunas_finais]

    # Salvar em CSV
    try:
        df_clean.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
        print(f"\nArquivo '{OUTPUT_CSV}' criado com sucesso!")
        print(f"Total de {len(df_clean)} GPUs processadas.")
        print("\nAmostra dos dados normalizados:")
        print(df_clean.head())
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")

# --- Executar o script ---
if __name__ == "__main__":
    processar_gpus()

# Nome do arquivo CSV gerado na etapa anterior
INPUT_CSV = "GPUs_final.csv"
OUTPUT_FILTRADO_CSV = "GPUs_2020_2024.csv" # Novo nome para o arquivo

def filtrar_e_ordenar_gpus(ano_minimo=2020):
    """
    Carrega o CSV 'GPUs_final.csv', filtra por ano de lançamento >= 2020
    e ordena os resultados por data (decrescente).
    """
    print(f"Tentando carregar o arquivo '{INPUT_CSV}'...")
    try:
        # Carrega o arquivo CSV
        df = pd.read_csv(INPUT_CSV)
        print(f"Arquivo carregado com sucesso. Total de {len(df)} GPUs encontradas.")

        # 1. Converter a coluna 'Lançamento' para o formato datetime
        # Isso é essencial para filtrar E ordenar corretamente
        df['Data_Lancamento_dt'] = pd.to_datetime(df['Lançamento'], format='%d/%m/%Y', errors='coerce')

        # 2. Filtrar o DataFrame
        # Remove linhas com ano < 2020 e também as datas nulas (NaT)
        df_filtrado = df[df['Data_Lancamento_dt'].dt.year >= ano_minimo].copy()

        # 3. [NOVO] Ordenar o DataFrame
        # Ordena pela coluna de data, com ascending=False (decrescente/mais novo primeiro)
        print("Ordenando resultados por data decrescente...")
        df_filtrado = df_filtrado.sort_values(by='Data_Lancamento_dt', ascending=False)

        # (Opcional) Remove a coluna de data temporária que criamos
        df_filtrado = df_filtrado.drop(columns=['Data_Lancamento_dt'])

        print("\n--- GPUs Lançadas a partir de 2020 (Mais novas primeiro) ---")
        if df_filtrado.empty:
            print("Nenhuma GPU encontrada com data de lançamento a partir de 2020.")
        else:
            print(f"Total de {len(df_filtrado)} GPUs encontradas e ordenadas.")
            print("Amostra dos dados filtrados (5 primeiras linhas):")
            print(df_filtrado.head()) # Mostra as 5 primeiras (as mais novas)

            # 4. Salvar o resultado filtrado e ordenado
            df_filtrado.to_csv(OUTPUT_FILTRADO_CSV, index=False, encoding='utf-8-sig')
            print(f"\nDados filtrados e ordenados salvos em '{OUTPUT_FILTRADO_CSV}'.")

    except FileNotFoundError:
        print(f"\nERRO: O arquivo '{INPUT_CSV}' não foi encontrado.", file=sys.stderr)
        print("Por favor, verifique se o nome do arquivo está correto e no mesmo diretório.", file=sys.stderr)
    except KeyError:
        print(f"\nERRO: A coluna 'Lançamento' não foi encontrada no CSV.", file=sys.stderr)
        print("Verifique se o arquivo CSV foi gerado corretamente.", file=sys.stderr)
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}", file=sys.stderr)

# --- Executar a função ---
if __name__ == "__main__":
    filtrar_e_ordenar_gpus()
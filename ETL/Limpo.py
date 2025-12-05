import pandas as pd
import re

ARQUIVO_ORIGEM = "VRAM_Evo.csv"
ARQUIVO_DESTINO = "Clean.csv"

def extrair_numero(texto):
    """Apenas pega o número cru do texto"""
    if pd.isna(texto): return 0.0
    s = str(texto).upper().strip().replace(',', '.')
    match = re.search(r"([\d\.]+)", s)
    return float(match.group(1)) if match else 0.0

def normalizar_para_mb(row, col_vram_nome):
    """
    Normaliza tudo para MEGABYTES (MB)
    Usa o ANO e o VALOR para decidir se converte.
    """
    raw_val = row[col_vram_nome]
    ano = row['ANO']
    
    val_str = str(raw_val).upper()
    numero = extrair_numero(raw_val)
    
    # 1. Se tem unidade explícita, respeita a unidade
    if "GB" in val_str:
        return numero * 1024
    if "TB" in val_str: # Vai que...
        return numero * 1024 * 1024
    if "MB" in val_str:
        return numero
    if "KB" in val_str:
        return numero / 1024
        
    # 2. Se não tem unidade (é só número), usa a heurística do "Bom Senso"
    # Anos 2010+ com valores pequenos (tipo 1, 2, 4, 8) são GBs.
    # Usamos 128 como corte: Ninguém listaria "128 GB" em 2010, seria "128 MB".
    if ano >= 2010:
        if numero < 128: 
            return numero * 1024 # Era GB, virou MB
        else:
            return numero # Já era MB (ex: 512, 1024)
            
    # Antes de 2010, assume que tudo sem unidade já é MB
    return numero

print("🔄 Iniciando ETL (Normalização para MB)...")

try:
    # Ler CSV
    try:
        df = pd.read_csv(ARQUIVO_ORIGEM, sep=None, engine='python')
    except:
        df = pd.read_csv(ARQUIVO_ORIGEM, encoding='latin1', sep=None, engine='python')

    # Achar colunas
    col_vram = next((c for c in df.columns if "vram" in c.lower() or "memory" in c.lower()), None)
    col_data = next((c for c in df.columns if "lançamento" in c.lower() or "date" in c.lower()), None)

    if col_vram and col_data:
        # Extrair ANO
        df['Data_Temp'] = pd.to_datetime(df[col_data], errors='coerce')
        df['ANO'] = df['Data_Temp'].dt.year
        
        # Fallback para ano em texto
        mask_nulos = df['ANO'].isna()
        if mask_nulos.any():
            df.loc[mask_nulos, 'ANO'] = df.loc[mask_nulos, col_data].astype(str).str.extract(r'(\d{4})')[0]
            
        df = df.dropna(subset=['ANO'])
        df['ANO'] = df['ANO'].astype(int)

        # APLICAR A NORMALIZAÇÃO (MB) linha a linha
        df['VRAM_MB'] = df.apply(lambda row: normalizar_para_mb(row, col_vram), axis=1)

        # Agrupar pelo Máximo
        df_final = df.groupby('ANO')['VRAM_MB'].max().reset_index().sort_values('ANO')
        
        # Salvar
        df_final.to_csv(ARQUIVO_DESTINO, index=False)
        print(f"✅ Sucesso! {ARQUIVO_DESTINO} gerado com valores em MB.")
        print(df_final.tail()) # Mostra os últimos anos para conferir
    else:
        print("❌ Colunas não encontradas.")

except Exception as e:
    print(f"❌ Erro: {e}")
import streamlit as st
import pandas as pd
import os
import sys

st.set_page_config(page_title="VRAM Timeline", layout="centered")

# CSS para estilo
st.markdown("""
    <style>
    .stButton button {width: 100%; font-weight: bold; background-color: #FF4B4B; color: white;}
    .big-font {font-size:20px !important; color: #333;}
    </style>
    """, unsafe_allow_html=True)

st.title("VRAM Evo Timeline 💾")
st.caption("Evolução da capacidade máxima de memória de vídeo (em MB) ao longo dos anos.")

ARQUIVO = "Clean.csv"

if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO)
    anos_disponiveis = sorted(df['ANO'].unique())

    # --- Filtros ---
    st.write("### Selecione o período de pesquisa")
    
    # Definindo padrões 1995-2025
    idx_inicio = list(anos_disponiveis).index(1995) if 1995 in anos_disponiveis else 0
    idx_fim = list(anos_disponiveis).index(2025) if 2025 in anos_disponiveis else len(anos_disponiveis) - 1

    c1, c2 = st.columns(2)
    with c1:
        inicio = st.selectbox("Início", anos_disponiveis, index=idx_inicio)
    with c2:
        # Filtra anos finais válidos
        anos_fim = [a for a in anos_disponiveis if a >= inicio]
        # Tenta manter a seleção em 2025 ou no último disponível
        alvo = 2025 if 2025 in anos_fim else anos_fim[-1]
        termino = st.selectbox("Término", anos_fim, index=anos_fim.index(alvo))

    st.markdown("---")

    if st.button("Gerar Gráfico"):
        # Filtragem
        df_chart = df[(df['ANO'] >= inicio) & (df['ANO'] <= termino)]
        
        if not df_chart.empty:
            # Gráfico
            st.success(f"Visualizando {inicio} - {termino}")
            
            # Formata os dados para o gráfico (Index=Ano, Coluna=VRAM_MB)
            chart_data = df_chart.set_index('ANO')['VRAM_MB']
            st.line_chart(chart_data)
            
            # Dados Curiosos
            max_val = df_chart['VRAM_MB'].max()
            
            # Lógica simples para converter para GB apenas no texto de destaque, pra ficar bonito
            txt_destaque = f"{max_val:.0f} MB"
            if max_val >= 1024:
                txt_destaque += f" ({max_val/1024:.1f} GB)"
                
            st.info(f"🏆 Recorde no período: **{txt_destaque}**")
        else:
            st.warning("Sem dados para este período.")
else:
    st.error("Arquivo 'Clean.csv' não encontrado. Rode o ETL primeiro!")

if __name__ == "__main__":
    if "streamlit" not in sys.modules:
        os.system(f"python -m streamlit run {sys.argv[0]}")
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import kagglehub

# Configuração da página
st.set_page_config(
    page_title="Mapa de Acidentes Rodoviários",
    layout="wide"
)

# Função para carregar e preparar os dados
@st.cache_data
def load_data():
    dtypes = {
        'latitude': 'float32',
        'longitude': 'float32',
        'causa_acidente': 'category'
    }
    
    usecols = ['data_inversa', 'latitude', 'longitude', 'causa_acidente']
    
    df = pd.read_csv(
        'accidents_2017_to_2023_portugues.csv',
        usecols=usecols,
        dtype=dtypes,
        quotechar='"',
        doublequote=True,
        encoding='utf-8',
        engine='c',
        chunksize=50000
    )
    
    chunks = []
    for chunk in df:
        chunk['data'] = pd.to_datetime(chunk['data_inversa'], errors='coerce')
        chunk['data'] = chunk['data'].dt.strftime('%d/%m/%Y')
        
        # Mask to keep only data points within Brazil
        mask = (
            chunk['latitude'].between(-34, 5) &  # Latitude range for Brazil
            chunk['longitude'].between(-74, -29) &  # Longitude range for Brazil
            chunk['latitude'].notna() &
            chunk['longitude'].notna()
        )
        chunk = chunk[mask]
        chunks.append(chunk)
    
    df_final = pd.concat(chunks, ignore_index=True)
    return df_final

# Função para amostrar dados
def sample_data(df, n=50000):
    """Retorna uma amostra dos dados se o DataFrame tiver mais de n linhas"""
    if len(df) > n:
        return df.sample(n=n, random_state=42)
    return df

# Carregar os dados com feedback de progresso
with st.spinner('Carregando dados...'):
    try:
        df = load_data()
        total_accidents = len(df)
        st.subheader("Acidentes Rodoviários no Brasil - 2017 a 2023")
        st.write(f"Exibindo uma amostra de 50,000 pontos de {total_accidents:,} acidentes.")
    except Exception as e:
        st.error(f'Ocorreu um erro ao carregar os dados: {e}')
        df = pd.DataFrame()

# Adicionando filtros
if not df.empty:
    # Filtro de data
    st.sidebar.header("Filtros")
    min_date = pd.to_datetime(df['data'].min(), format='%d/%m/%Y')
    max_date = pd.to_datetime(df['data'].max(), format='%d/%m/%Y')
    date_range = st.sidebar.date_input("Selecione o intervalo de datas:", [min_date, max_date])

    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['data'] >= start_date.strftime('%d/%m/%Y')) & (df['data'] <= end_date.strftime('%d/%m/%Y'))]

    # Filtro de causa do acidente
    causa_options = df['causa_acidente'].unique()

# Definindo a opção padrão como "Demais falhas mecânicas ou elétricas"
    default_causa = ["Demais falhas mecânicas ou elétricas"] if "Demais falhas mecânicas ou elétricas" in causa_options else []

    causa_selecionada = st.sidebar.multiselect(
    'Selecione a(s) causa(s) do acidente:',
    options=causa_options,
    default=default_causa  # Define a opção padrão
)

# Filtrar o DataFrame com base na seleção do usuário
if causa_selecionada:
    df = df[df['causa_acidente'].isin(causa_selecionada)]
    total_accidents = len(df)
    st.write(f"{total_accidents:,} acidentes.")
    
    if causa_selecionada:
        df = df[df['causa_acidente'].isin(causa_selecionada)]
        total_accidents = len(df)
        st.write(f"{total_accidents:,} acidentes.")

    # Amostragem para melhorar a performance
    df_map = sample_data(df, n=50000)
    df_map = df_map[['latitude', 'longitude']]

    # Certifique-se de que as colunas de coordenadas estão no tipo correto e sem valores ausentes
    df_map = df_map.dropna(subset=['latitude', 'longitude'])
    df_map['latitude'] = df_map['latitude'].astype(float)
    df_map['longitude'] = df_map['longitude'].astype(float)

    # Exibindo os dados no mapa do Streamlit
    if not df_map.empty:
        st.map(df_map, size=10, zoom=5, color="#21bbe2")
    else:
        st.write("Nenhum ponto a ser exibido no mapa.")

    # Exibindo tabela de contagem por motivo
    st.subheader("Quantidade de acidentes por motivo")
    causa_count = df['causa_acidente'].value_counts().reset_index()
    causa_count.columns = ['Causa do Acidente', 'Quantidade']
    st.table(causa_count)
else:
    st.write("Nenhum dado disponível para exibição.")

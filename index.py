import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import kagglehub

# Configuração da página com tema e layout mais profissional
st.set_page_config(
    page_title="Análise de Acidentes Rodoviários | Brasil",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicando estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 1rem 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Função para carregar e preparar os dados (mantida igual)
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
        
        mask = (
            chunk['latitude'].between(-34, 5) &
            chunk['longitude'].between(-74, -29) &
            chunk['latitude'].notna() &
            chunk['longitude'].notna()
        )
        chunk = chunk[mask]
        chunks.append(chunk)
    
    df_final = pd.concat(chunks, ignore_index=True)
    return df_final

def sample_data(df, n=50000):
    if len(df) > n:
        return df.sample(n=n, random_state=42)
    return df

# Header do Dashboard
st.title("🚗 Dashboard de Acidentes Rodoviários")
st.markdown("### Análise Detalhada de Acidentes nas Rodovias Brasileiras (2017-2023)")

# Carregar dados com barra de progresso mais elegante
with st.spinner('📊 Carregando dados...'):
    try:
        df = load_data()
        total_accidents = len(df)
        
        # Metrics Container
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Acidentes", f"{total_accidents:,}")
        with col2:
            st.metric("Período", f"2017-2023")
        with col3:
            st.metric("Estados Cobertos", "27")
            
    except Exception as e:
        st.error('⚠️ Erro ao carregar os dados: Verifique a conexão com a fonte de dados.')
        st.exception(e)
        df = pd.DataFrame()

# Sidebar mais organizada
if not df.empty:
    with st.sidebar:
        st.sidebar.image("https://www.gov.br/transportes/pt-br/assuntos/transito/arquivos-senatran/logo-senatran.png", width=200)
        st.sidebar.title("Filtros de Análise")
        
        # Filtro de data com layout melhorado
        st.subheader("📅 Período")
        min_date = pd.to_datetime(df['data'].min(), format='%d/%m/%Y')
        max_date = pd.to_datetime(df['data'].max(), format='%d/%m/%Y')
        date_range = st.date_input(
            "Selecione o intervalo:",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        # Filtro de causa com search
        st.subheader("🔍 Causa do Acidente")
        causa_options = ['Todos os motivos'] + list(df['causa_acidente'].unique())
        causa_selecionada = st.multiselect(
            'Selecione as causas:',
            options=causa_options,
            default=['Todos os motivos']
        )

        # Botão de exportação
        if st.button('📥 Exportar Dados Filtrados'):
            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='acidentes_rodoviarios.csv',
                mime='text/csv'
            )

    # Aplicando filtros
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['data'] >= start_date.strftime('%d/%m/%Y')) & 
                (df['data'] <= end_date.strftime('%d/%m/%Y'))]

    if "Todos os motivos" in causa_selecionada or not causa_selecionada:
        filtered_df = df
    else:
        filtered_df = df[df['causa_acidente'].isin(causa_selecionada)]

    # Layout principal com tabs
    tab1, tab2, tab3 = st.tabs(["📍 Mapa", "📊 Análise por Causa", "📈 Tendências"])
    
    with tab1:
        st.subheader("Distribuição Geográfica dos Acidentes")
        df_map = sample_data(filtered_df, n=50000)
        df_map = df_map[['latitude', 'longitude']]
        df_map = df_map.dropna(subset=['latitude', 'longitude'])
        
        if not df_map.empty:
            st.map(df_map, size=10, zoom=5, color="#FF4B4B")
        
    with tab2:
        st.subheader("Análise por Causa de Acidente")
        
        # Gráfico de barras com Plotly
        causa_count = filtered_df['causa_acidente'].value_counts()
        fig = px.bar(
            x=causa_count.values,
            y=causa_count.index,
            orientation='h',
            title='Distribuição de Acidentes por Causa',
            labels={'x': 'Número de Acidentes', 'y': 'Causa'},
            color=causa_count.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(showlegend=False, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    with tab3:
        st.subheader("Tendência Temporal")
        filtered_df['data'] = pd.to_datetime(filtered_df['data'], format='%d/%m/%Y')
        acidentes_por_mes = filtered_df.groupby(filtered_df['data'].dt.strftime('%Y-%m')).size().reset_index()
        acidentes_por_mes.columns = ['Mês', 'Quantidade']
        
        fig = px.line(
            acidentes_por_mes,
            x='Mês',
            y='Quantidade',
            title='Evolução Mensal dos Acidentes',
            markers=True
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("""---""")
    st.markdown("""
        <div style='text-align: center'>
            <p>Dashboard desenvolvido para análise de acidentes rodoviários no Brasil.</p>
            <p>Fonte: Base Nacional de Acidentes de Trânsito</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("Não foi possível carregar os dados. Verifique a conexão com a fonte de dados.")

# 🚗 Dashboard de Análise de Acidentes Rodoviários

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40.0-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.3-green.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.19.0-blue.svg)](https://plotly.com/)

## 📌 Sobre o Projeto

Dashboard interativo desenvolvido para análise e visualização de dados de acidentes rodoviários no Brasil, cobrindo o período de 2017 a 2023. A ferramenta processa dados da publciada na plataforma Kaggle, oferecendo insights cruciais para a segurança viária através de visualizações interativas e análises detalhadas.

## 🎯 Funcionalidades

- 📊 Visualização geográfica dos acidentes em mapa interativo
- 📈 Análise temporal da evolução dos acidentes
- 🔍 Filtros dinâmicos por período e causa do acidente
- 📋 Ranking das principais causas de acidentes
- 📊 Gráficos interativos com Plotly
- 💾 Possibilidade de exportação dos dados filtrados

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/acidentes-rodoviarios.git
cd acidentes-rodoviarios
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Execute a aplicação
```bash
streamlit run index.py
```

## 📦 Estrutura do Projeto

```
acidentes-rodoviarios/
│
├── index.py                    # Arquivo principal da aplicação
├── requirements.txt            # Dependências do projeto
├── accidents_2017_to_2023_portugues.csv    # Dataset dos acidentes
│
└── README.md                   # Documentação do projeto
```

## 📋 Dependências Principais

- `streamlit==1.40.0`
- `pandas==2.2.3`
- `plotly==5.19.0`
- `kagglehub==0.3.4`
- `gdown==5.2.0`

## 🔧 Configuração

O projeto utiliza as configurações padrão do Streamlit. Para personalizar as configurações, você pode criar um arquivo `.streamlit/config.toml` com suas preferências.

## 💡 Uso

1. Ao iniciar a aplicação, você verá o dashboard principal com o mapa de acidentes
2. Use os filtros na barra lateral para:
   - Selecionar período de análise
   - Filtrar por causa do acidente
3. Explore as diferentes visualizações nas abas disponíveis
4. Utilize a funcionalidade de exportação para baixar os dados filtrados

## 📊 Visualizações Disponíveis

1. **Mapa de Acidentes**
   - Distribuição geográfica dos acidentes
   - Densidade de ocorrências por região

2. **Análise por Causa**
   - Ranking das principais causas
   - Distribuição percentual

3. **Análise Temporal**
   - Evolução mensal dos acidentes
   - Tendências ao longo do período

## 🤝 Como Contribuir

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça o Commit de suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📫 Contato

[Rodrigo Troskaitis Santos] - [rodrigo.troskaitis@gmail.com]

Link do projeto: [[https://github.com/seu-usuario/acidentes-rodoviarios](https://github.com/Troskaitis/AcidentesRodoviarios)


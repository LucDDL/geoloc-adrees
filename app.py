import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlencode

def geolocalizar(endereco):
    base_url = "https://nominatim.openstreetmap.org/search?"
    parametros = {'q': endereco, 'format': 'json'}
    headers = {'User-Agent': 'Mozilla/5.0'}
    url_completa = base_url + urlencode(parametros)
    response = requests.get(url_completa, headers=headers)
    if response.status_code == 200 and response.json():
        dados = response.json()[0]
        return dados['lat'], dados['lon']
    return None, None

def main():
    st.title("Geolocalização de Endereços")
    
    uploaded_file = st.file_uploader("Carregar arquivo CSV contendo os endereços", type="csv")
    if uploaded_file is not None:
        enderecos_df = pd.read_csv(uploaded_file)
        enderecos_df['Latitude'], enderecos_df['Longitude'] = zip(*enderecos_df['Endereço'].apply(geolocalizar))
        st.write(enderecos_df)

if __name__ == "__main__":
    main()

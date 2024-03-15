import streamlit as st
import requests
from urllib.parse import urlencode
import pandas as pd

# Função para geolocalizar endereço usando a API do OpenStreetMap
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

# Função principal
def main():
    st.title("Geolook")
    
    # Campo de texto (text area) para inserir os endereços
    enderecos_input = st.text_area("Insira os endereços (um por linha):", height=200)

    # Botão para localizar coordenadas
    if st.button("Localizar"):
        if enderecos_input:
            # Dividir os endereços em uma lista
            enderecos = enderecos_input.split("\n")
            
            # Lista para armazenar os resultados
            resultados = []
            
            # Iterar sobre cada endereço e localizar as coordenadas
            for endereco in enderecos:
                if endereco.strip():
                    lat, lng = geolocalizar(endereco.strip())
                    if lat and lng:
                        resultados.append({'Endereço': endereco.strip(), 'Latitude': lat, 'Longitude': lng})
                    else:
                        st.error(f"Não foi possível encontrar as coordenadas para o endereço: {endereco.strip()}")
            
            # Criar DataFrame com os resultados
            df_resultados = pd.DataFrame(resultados)
            
            # Exibir DataFrame na interface
            st.write("Resultados:")
            st.write(df_resultados)
            
            # Botão para baixar os resultados em CSV
            csv = df_resultados.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="Baixar Resultados em CSV", data=csv, file_name='resultados_geolocalizacao.csv', mime='text/csv')
            
        else:
            st.warning("Por favor, insira pelo menos um endereço para realizar a busca.")

if __name__ == "__main__":
    main()

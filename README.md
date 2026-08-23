# 🌦️ Weather Explorer

# 🌦️ Weather Explorer

[![Streamlit App] (https://weather-explorer-st.streamlit.app/)

> 🔗 **[Clique aqui para testar a aplicação online sem instalar nada!](https://SEU-APP.streamlit.app)**

---

Uma aplicação web interativa e de alta performance desenvolvida em Python e Streamlit para consulta de dados meteorológicos em tempo real a partir do CEP.

---

## Funcionalidades

* **Busca por CEP:** Consulta dados de endereço via integração com a API ViaCEP.
* **Geocodificação Direta:** Conversão de endereço em coordenadas geográficas (latitude/longitude) via Geopy.
* **Previsão Detalhada:** Dados meteorológicos atuais, previsão hora a hora para as próximas 24 horas e previsão estendida para 7 dias via Open-Meteo API.
* **Visualização Gráfica:** Gráfico dinâmico de variação da temperatura e mapa interativo da localização.
* **Privacidade por Design (LGPD):** Minimização de dados pessoais exibidos na interface e processamento 100% em memória volátil, sem persistência em banco de dados.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.14+
* **Framework Web:** Streamlit
* **Manipulação de Dados:** Pandas
* **Geolocalização & APIs:** Geopy, Requests (ViaCEP & Open-Meteo)


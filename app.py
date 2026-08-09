import requests
import streamlit as st

def limpar_cep(cep):
    return cep.replace("-", "").strip()

def buscar_cep(cep):
    cep = limpar_cep(cep)
    url = f"https://viacep.com.br/ws/{cep}/json/"

    resposta = requests.get(url)

    return resposta.json()


st.set_page_config(
    page_title="Weather Explorer",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Explorer")

st.write(
    "Consulte informações meteorológicas "
    "a partir de um CEP."
)

cep = st.text_input("Digite seu CEP")

if st.button("Consultar"):
    dados = buscar_cep(cep)

    if "erro" in dados:
        st.warning("CEP não encontrado.")
    else:
        st.success("CEP encontrado!")

        st.subheader("📍 Localização")

        st.write(f"**CEP:** {dados['cep']}")
        st.write(f"**Logradouro:** {dados['logradouro']}")
        st.write(f"**Bairro:** {dados['bairro']}")
        st.write(f"**Cidade:** {dados['localidade']}")
        st.write(f"**Estado:** {dados['uf']}")
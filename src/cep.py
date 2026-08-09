import requests


def limpar_cep(cep):
    return cep.replace("-", "").strip()


def buscar_cep(cep):
    cep = limpar_cep(cep)

    url = f"https://viacep.com.br/ws/{cep}/json/"

    resposta = requests.get(url)

    return resposta.json()
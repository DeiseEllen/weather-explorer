import requests


def buscar_cep(cep):
    cep = cep.replace("-", "").strip()

    if not cep.isdigit() or len(cep) != 8:
        return None

    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        resposta = requests.get(
            url,
            timeout=10
        )

        resposta.raise_for_status()

        dados = resposta.json()

        if dados.get("erro"):
            return None

        return dados

    except (requests.RequestException, ValueError):
        return None
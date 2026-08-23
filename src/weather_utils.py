def descricao_tempo(codigo):
    descricoes = {
        0: "Ceu limpo",
        1: "Principalmente limpo",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Neblina",
        48: "Neblina com geada",
        51: "Chuvisco leve",
        53: "Chuvisco moderado",
        55: "Chuvisco intenso",
        61: "Chuva leve",
        63: "Chuva moderada",
        65: "Chuva intensa",
        71: "Neve leve",
        73: "Neve moderada",
        75: "Neve intensa",
        80: "Pancadas de chuva leves",
        81: "Pancadas de chuva moderadas",
        82: "Pancadas de chuva fortes",
        95: "Trovoada",
        96: "Trovoada com granizo",
        99: "Trovoada forte com granizo"
    }

    return descricoes.get(
        codigo,
        "Condicao desconhecida"
    )


def icone_tempo(codigo):
    if codigo == 0:
        return "sol"

    if codigo in [1, 2]:
        return "parcialmente_nublado"

    if codigo == 3:
        return "nublado"

    if codigo in [45, 48]:
        return "neblina"

    if codigo in [51, 53, 55]:
        return "chuvisco"

    if codigo in [61, 63, 65, 80, 81, 82]:
        return "chuva"

    if codigo in [95, 96, 99]:
        return "trovoada"

    return "desconhecido"
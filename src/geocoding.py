from geopy.geocoders import Nominatim


geolocator = Nominatim(
    user_agent="weather-explorer"
)


def obter_coordenadas(endereco, cidade, estado):
    consultas = [
        endereco,
        f"{cidade}, {estado}, Brasil"
    ]

    for consulta in consultas:
        try:
            localizacao = geolocator.geocode(
                consulta,
                timeout=10,
                country_codes="br"
            )

            if localizacao:
                return {
                    "latitude": localizacao.latitude,
                    "longitude": localizacao.longitude
                }

        except Exception:
            continue

    return None
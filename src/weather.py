import requests


def buscar_previsao(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "weather_code,"
            "wind_speed_10m"
        ),

        "hourly": (
            "temperature_2m,"
            "weather_code,"
            "precipitation_probability"
        ),

        "daily": (
            "weather_code,"
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max"
        ),

        "timezone": "auto",
        "forecast_days": 7
    }

    resposta = requests.get(
        url,
        params=parametros,
        timeout=10
    )

    resposta.raise_for_status()

    return resposta.json()
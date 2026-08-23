import pandas as pd
import streamlit as st

from src.cep import buscar_cep
from src.geocoding import obter_coordenadas
from src.weather import buscar_previsao
from src.weather_utils import descricao_tempo, icone_tempo


st.set_page_config(
    page_title="Weather Explorer",
    page_icon="🌦️",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }

    .weather-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .weather-subtitle {
        font-size: 1.1rem;
        color: #9ca3af;
        margin-bottom: 2rem;
    }

    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }

    div[data-testid="stFormSubmitButton"] button {
        height: 42px;
        margin-top: 28px;
    }

    .weather-card {
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid #30343b;
        background: #171a20;
        margin-bottom: 1rem;
    }

    .temperature {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }

    .weather-description {
        font-size: 1.1rem;
        color: #d1d5db;
        margin-top: 0.5rem;
    }

    .hour-card {
        padding: 1rem 0.5rem;
        text-align: center;
        border-radius: 12px;
        border: 1px solid #30343b;
        background: #171a20;
        min-height: 180px;
    }

    .day-card {
        padding: 1rem;
        text-align: center;
        border-radius: 12px;
        border: 1px solid #30343b;
        background: #171a20;
        min-height: 230px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

EMOJIS_TEMPO = {
    "sol": "☀️",
    "parcialmente_nublado": "🌤️",
    "nublado": "☁️",
    "neblina": "🌫️",
    "chuvisco": "🌦️",
    "chuva": "🌧️",
    "trovoada": "⛈️",
    "desconhecido": "🌡️"
}

if "dados_consulta" not in st.session_state:
    st.session_state.dados_consulta = None

if "previsao" not in st.session_state:
    st.session_state.previsao = None

st.markdown(
    '<div class="weather-title">🌦️ Weather Explorer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="weather-subtitle">'
    'Consulte informações meteorológicas a partir de um CEP.'
    '</div>',
    unsafe_allow_html=True
)

with st.form("consulta_cep"):
    col_input, col_button = st.columns([5, 1], vertical_alignment="bottom")

    with col_input:
        cep = st.text_input(
            "Digite seu CEP",
            placeholder="Ex.: 50000-000"
        )

    with col_button:
        consultar = st.form_submit_button(
            "Consultar",
            type="primary",
            use_container_width=True
        )

if consultar:
    if not cep.strip():
        st.warning("Digite um CEP para realizar a consulta.")
        st.stop()

    with st.spinner("Consultando CEP..."):
        try:
            dados = buscar_cep(cep)
        except Exception:
            dados = None

    if not dados:
        st.error("Não foi possível encontrar esse CEP. Verifique o número informado.")
        st.stop()

    cidade = dados.get("localidade", "")
    estado = dados.get("uf", "")
    logradouro = dados.get("logradouro", "")
    bairro = dados.get("bairro", "")
    cep_formatado = dados.get("cep", cep)

    endereco = f"{logradouro}, {bairro}, {cidade}, {estado}, Brasil"

    with st.spinner("Localizando endereço..."):
        try:
            coordenadas = obter_coordenadas(endereco, cidade, estado)
        except Exception:
            coordenadas = None

    if not coordenadas:
        st.warning("O endereço foi encontrado, mas não foi possível obter as coordenadas.")
        st.stop()

    latitude = coordenadas.get("latitude")
    longitude = coordenadas.get("longitude")

    with st.spinner("Consultando previsão do tempo..."):
        try:
            previsao = buscar_previsao(latitude, longitude)
        except Exception:
            previsao = None

    if not previsao:
        st.error("Não foi possível obter os dados meteorológicos no momento.")
        st.stop()

    st.session_state.dados_consulta = {
        "cidade": cidade,
        "estado": estado,
        "latitude": latitude,
        "longitude": longitude
    }
    st.session_state.previsao = previsao

dados_consulta = st.session_state.dados_consulta
previsao = st.session_state.previsao

if dados_consulta and previsao:
    cidade = dados_consulta["cidade"]
    estado = dados_consulta["estado"]
    latitude = dados_consulta["latitude"]
    longitude = dados_consulta["longitude"]

    atual = previsao.get("current", {})
    temperatura = atual.get("temperature_2m", 0)
    sensacao = atual.get("apparent_temperature", 0)
    umidade = atual.get("relative_humidity_2m", 0)
    vento = atual.get("wind_speed_10m", 0)
    codigo = atual.get("weather_code", 0)

    emoji_atual = EMOJIS_TEMPO.get(icone_tempo(codigo), "🌡️")

    st.divider()

    st.subheader(f"📍 {cidade}, {estado}")
    st.caption("🔒 Dados de localização processados temporariamente para consulta meteorológica.")

    col_weather, col_description = st.columns([1, 2])

    with col_weather:
        st.markdown(
            f'<div class="weather-card"><p class="temperature">{emoji_atual} {temperatura:.0f}°C</p></div>',
            unsafe_allow_html=True
        )

    with col_description:
        st.markdown(
            f'<div class="weather-card"><p class="weather-description">{descricao_tempo(codigo)}</p><p>Sensação térmica de <strong>{sensacao:.0f}°C</strong></p></div>',
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💧 Umidade", f"{umidade}%")

    with col2:
        st.metric("💨 Vento", f"{vento:.0f} km/h")

    with col3:
        st.metric("🌡️ Sensação", f"{sensacao:.0f}°C")

    st.divider()

    st.subheader("🕐 Próximas 24 horas")

    hourly = previsao.get("hourly", {})
    horarios = hourly.get("time", [])[:24]
    temperaturas = hourly.get("temperature_2m", [])[:24]
    chuvas = hourly.get("precipitation_probability", [])[:24]
    codigos_horarios = hourly.get("weather_code", [])[:24]

    quantidade_horas = min(
        len(horarios),
        len(temperaturas),
        len(chuvas),
        len(codigos_horarios)
    )

    if quantidade_horas > 0:
        st.markdown("#### Previsão por horário")

        quantidade_cards = min(8, quantidade_horas)
        colunas = st.columns(quantidade_cards)

        for i in range(quantidade_cards):
            horario = pd.to_datetime(horarios[i]).strftime("%H:%M")
            temperatura_hora = temperaturas[i]
            chuva_hora = chuvas[i]
            codigo_hora = codigos_horarios[i]
            emoji_hora = EMOJIS_TEMPO.get(icone_tempo(codigo_hora), "🌡️")

            with colunas[i]:
                card_html = (
                    f'<div class="hour-card">'
                    f'<strong>{horario}</strong>'
                    f'<div style="font-size: 2rem; margin: 10px 0;">{emoji_hora}</div>'
                    f'<strong>{temperatura_hora:.0f}°C</strong>'
                    f'<div style="font-size: 0.8rem; margin-top: 8px;">{descricao_tempo(codigo_hora)}</div>'
                    f'<div style="font-size: 0.8rem; margin-top: 8px;">🌧️ {chuva_hora}%</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

        st.markdown("#### Variação da temperatura")

        grafico = pd.DataFrame({
            "Horário": pd.to_datetime(horarios),
            "Temperatura (°C)": temperaturas
        }).set_index("Horário")

        st.line_chart(grafico, y="Temperatura (°C)")

    else:
        st.info("Não foi possível carregar a previsão por hora.")

    st.divider()

    st.subheader("📅 Previsão para 7 dias")

    daily = previsao.get("daily", {})
    datas = daily.get("time", [])
    maximas = daily.get("temperature_2m_max", [])
    minimas = daily.get("temperature_2m_min", [])
    codigos_diarios = daily.get("weather_code", [])
    chuvas_diarias = daily.get("precipitation_probability_max", [])

    quantidade_dias = min(
        len(datas),
        len(maximas),
        len(minimas),
        len(codigos_diarios),
        len(chuvas_diarias)
    )

    if quantidade_dias > 0:
        colunas = st.columns(quantidade_dias)

        for i in range(quantidade_dias):
            data_formatada = pd.to_datetime(datas[i]).strftime("%d/%m")
            emoji_dia = EMOJIS_TEMPO.get(icone_tempo(codigos_diarios[i]), "🌡️")

            with colunas[i]:
                card_dia_html = (
                    f'<div class="day-card">'
                    f'<strong>{data_formatada}</strong>'
                    f'<div style="font-size: 2rem; margin: 12px 0;">{emoji_dia}</div>'
                    f'<strong>{maximas[i]:.0f}°C</strong>'
                    f'<div>Mínima: {minimas[i]:.0f}°C</div>'
                    f'<div style="font-size: 0.8rem; margin-top: 8px;">{descricao_tempo(codigos_diarios[i])}</div>'
                    f'<div style="font-size: 0.8rem; margin-top: 8px;">🌧️ {chuvas_diarias[i]}%</div>'
                    f'</div>'
                )
                st.markdown(card_dia_html, unsafe_allow_html=True)

    else:
        st.info("Não foi possível carregar a previsão dos próximos dias.")

    st.divider()

    st.subheader("🗺️ Localização")

    mapa = pd.DataFrame({
        "latitude": [latitude],
        "longitude": [longitude]
    })

    st.map(mapa, latitude="latitude", longitude="longitude", zoom=12)

    st.caption(f"Coordenadas: {latitude:.5f}, {longitude:.5f}")

    st.divider()

    if st.button("🔄 Atualizar previsão"):
        with st.spinner("Atualizando previsão..."):
            try:
                nova_previsao = buscar_previsao(latitude, longitude)
                st.session_state.previsao = nova_previsao
                st.rerun()
            except Exception:
                st.error("Não foi possível atualizar a previsão neste momento.")
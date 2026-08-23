import pandas as pd
import streamlit as st

from src.cep import buscar_cep
from src.geocoding import obter_coordenadas
from src.weather import buscar_previsao



# CONFIGURAÇÃO DA PÁGINA


st.set_page_config(
    page_title="Weather Explorer",
    page_icon="🌦️",
    layout="wide"
)



# FUNÇÕES AUXILIARES


def descricao_tempo(codigo):
    descricoes = {
        0: "Céu limpo",
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
        "Condição desconhecida"
    )


def icone_tempo(codigo):
    if codigo == 0:
        return "☀️"

    if codigo in [1, 2]:
        return "🌤️"

    if codigo == 3:
        return "☁️"

    if codigo in [45, 48]:
        return "🌫️"

    if codigo in [51, 53, 55]:
        return "🌦️"

    if codigo in [61, 63, 65, 80, 81, 82]:
        return "🌧️"

    if codigo in [95, 96, 99]:
        return "⛈️"

    return "🌡️"



# ESTADO DA APLICAÇÃO


if "cep_consultado" not in st.session_state:
    st.session_state.cep_consultado = ""



# CABEÇALHO


st.title("🌦️ Weather Explorer")

st.write(
    "Consulte informações meteorológicas "
    "a partir de um CEP."
)

st.divider()



# CAMPO DE CEP

# CAMPO DE CEP

with st.form("form_cep"):

    col_input, col_button = st.columns([5, 1])

    with col_input:
        cep = st.text_input(
            "Digite seu CEP",
            placeholder="Ex.: 50000-000",
            value=st.session_state.cep_consultado
        )

    with col_button:
        st.write("")

        consultar = st.form_submit_button(
            "Consultar",
            type="primary",
            use_container_width=True
        )


# BOTÃO DE ATUALIZAR
atualizar = st.button(
    "🔄 Atualizar previsão",
    use_container_width=True
)

# CONSULTA


if consultar or atualizar:

    
    # SALVA O CEP CONSULTADO
    

    if consultar:

        st.session_state.cep_consultado = cep

    else:

        cep = st.session_state.cep_consultado


    
    # VALIDAÇÃO DO CEP
    

    if not cep.strip():

        st.warning(
            "Digite um CEP para realizar a consulta."
        )

        st.stop()


    
    # BUSCA DO CEP
    

    with st.spinner("Consultando CEP..."):

        try:

            dados = buscar_cep(cep)

        except Exception:

            dados = None


    if not dados:

        st.error(
            "Não foi possível encontrar esse CEP. "
            "Verifique o número informado."
        )

        st.stop()


    
    # DADOS DO ENDEREÇO
    

    cidade = dados.get(
        "localidade",
        ""
    )

    estado = dados.get(
        "uf",
        ""
    )

    logradouro = dados.get(
        "logradouro",
        ""
    )

    bairro = dados.get(
        "bairro",
        ""
    )

    cep_formatado = dados.get(
        "cep",
        cep
    )


    
    # MONTA ENDEREÇO
    

    endereco = (
        f"{logradouro}, "
        f"{bairro}, "
        f"{cidade}, "
        f"{estado}, Brasil"
    )


    
    # GEOCODIFICAÇÃO
    

    with st.spinner("Localizando endereço..."):

        try:

            coordenadas = obter_coordenadas(
                endereco,
                cidade,
                estado
            )

        except Exception:

            coordenadas = None


    if not coordenadas:

        st.warning(
            "O endereço foi encontrado, "
            "mas não foi possível obter "
            "as coordenadas."
        )

        st.stop()


    latitude = coordenadas["latitude"]
    longitude = coordenadas["longitude"]


    
    # PREVISÃO DO TEMPO
    

    with st.spinner(
        "Consultando previsão do tempo..."
    ):

        try:

            previsao = buscar_previsao(
                latitude,
                longitude
            )

        except Exception:

            previsao = None


    if not previsao:

        st.error(
            "Não foi possível obter os dados "
            "meteorológicos no momento."
        )

        st.stop()


    
    # DADOS ATUAIS
    

    atual = previsao.get(
        "current",
        {}
    )

    temperatura = atual.get(
        "temperature_2m"
    )

    sensacao = atual.get(
        "apparent_temperature"
    )

    umidade = atual.get(
        "relative_humidity_2m"
    )

    vento = atual.get(
        "wind_speed_10m"
    )

    codigo = atual.get(
        "weather_code"
    )


    
    # LOCALIZAÇÃO
    

    st.divider()

    st.subheader(
        f"📍 {cidade}, {estado}"
    )

    st.caption(
        f"CEP {cep_formatado} • "
        f"{logradouro}, {bairro}"
    )


    
    # CLIMA ATUAL
    

    col_weather, col_description = st.columns([1, 2])

    with col_weather:

        st.metric(
            label="Condição atual",
            value=(
                f"{icone_tempo(codigo)} "
                f"{temperatura:.0f}°C"
            )
        )


    with col_description:

        st.metric(
            label="Condição",
            value=descricao_tempo(codigo),
            delta=(
                f"Sensação térmica: "
                f"{sensacao:.0f}°C"
            )
        )


    
    # MÉTRICAS
    

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "💧 Umidade",
            f"{umidade}%"
        )


    with col2:

        st.metric(
            "💨 Vento",
            f"{vento:.0f} km/h"
        )


    with col3:

        st.metric(
            "🌡️ Sensação",
            f"{sensacao:.0f}°C"
        )


    
    # PREVISÃO POR HORA
    

    st.divider()

    st.subheader(
        "🕐 Próximas 24 horas"
    )

    hourly = previsao.get(
        "hourly",
        {}
    )

    horarios = hourly.get(
        "time",
        []
    )[:24]

    temperaturas = hourly.get(
        "temperature_2m",
        []
    )[:24]

    chuvas = hourly.get(
        "precipitation_probability",
        []
    )[:24]

    codigos_horarios = hourly.get(
        "weather_code",
        []
    )[:24]


    quantidade_horas = min(
        len(horarios),
        len(temperaturas),
        len(chuvas),
        len(codigos_horarios)
    )


    if quantidade_horas > 0:


        # CARDS


        st.markdown(
            "#### Previsão por horário"
        )

        quantidade_cards = min(
            8,
            quantidade_horas
        )

        colunas = st.columns(
            quantidade_cards
        )


        for i in range(
            quantidade_cards
        ):

            with colunas[i]:

                horario = pd.to_datetime(
                    horarios[i]
                ).strftime("%H:%M")

                temperatura_hora = temperaturas[i]

                chuva_hora = chuvas[i]

                codigo_hora = codigos_horarios[i]


                st.markdown(
                    f"**{horario}**"
                )

                st.markdown(
                    f"### "
                    f"{icone_tempo(codigo_hora)}"
                )

                st.markdown(
                    f"**{temperatura_hora:.0f}°C**"
                )

                st.caption(
                    descricao_tempo(
                        codigo_hora
                    )
                )

                st.caption(
                    f"🌧️ {chuva_hora}%"
                )



        # GRÁFICO


        st.markdown(
            "#### Variação da temperatura"
        )

        grafico = pd.DataFrame(
            {
                "Horário": pd.to_datetime(
                    horarios
                ),

                "Temperatura (°C)": temperaturas
            }
        )


        grafico = grafico.set_index(
            "Horário"
        )


        st.line_chart(
            grafico,
            y="Temperatura (°C)"
        )


    else:

        st.info(
            "Não foi possível carregar "
            "a previsão por hora."
        )


    
    # PREVISÃO PARA 7 DIAS
    

    st.divider()

    st.subheader(
        "📅 Previsão para 7 dias"
    )

    daily = previsao.get(
        "daily",
        {}
    )

    datas = daily.get(
        "time",
        []
    )

    maximas = daily.get(
        "temperature_2m_max",
        []
    )

    minimas = daily.get(
        "temperature_2m_min",
        []
    )

    codigos_diarios = daily.get(
        "weather_code",
        []
    )

    chuvas_diarias = daily.get(
        "precipitation_probability_max",
        []
    )


    quantidade_dias = min(
        len(datas),
        len(maximas),
        len(minimas),
        len(codigos_diarios),
        len(chuvas_diarias)
    )


    if quantidade_dias > 0:

        colunas = st.columns(
            quantidade_dias
        )


        for i in range(
            quantidade_dias
        ):

            with colunas[i]:

                data_formatada = pd.to_datetime(
                    datas[i]
                ).strftime("%d/%m")


                st.markdown(
                    f"**{data_formatada}**"
                )


                st.markdown(
                    f"### "
                    f"{icone_tempo(codigos_diarios[i])}"
                )


                st.write(
                    f"**{maximas[i]:.0f}°C**"
                )


                st.caption(
                    f"Mínima: "
                    f"{minimas[i]:.0f}°C"
                )


                st.caption(
                    descricao_tempo(
                        codigos_diarios[i]
                    )
                )


                st.caption(
                    f"🌧️ Chuva: "
                    f"{chuvas_diarias[i]}%"
                )


    else:

        st.info(
            "Não foi possível carregar "
            "a previsão dos próximos dias."
        )


    
    # MAPA
    

    st.divider()

    st.subheader(
        "🗺️ Localização"
    )


    mapa = pd.DataFrame(
        {
            "latitude": [latitude],
            "longitude": [longitude]
        }
    )


    st.map(
        mapa,
        latitude="latitude",
        longitude="longitude",
        zoom=12
    )


    
    # COORDENADAS
    

    st.caption(
        f"Coordenadas: "
        f"{latitude:.5f}, "
        f"{longitude:.5f}"
    )
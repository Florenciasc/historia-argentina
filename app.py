import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Ruta del Deporte Argentino",
    page_icon="🗺️",
    layout="centered"
)

df = pd.read_csv("data/preguntas_trivia.csv")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f7efe0, #d8b98b);
    color: #1f1308;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

[data-testid="stHeader"] {
    background: rgba(247,239,224,.9);
}

h1, h2, h3, p, label, span, div {
    color: #1f1308 !important;
}

div.stButton > button {
    background: #6b2f14 !important;
    color: #fff8e8 !important;
    border: 2px solid #1f1308 !important;
    border-radius: 8px !important;
    font-weight: 900 !important;
    padding: .85rem 1.2rem !important;
}

div.stButton > button:disabled {
    background: #bda98b !important;
    color: #4a3825 !important;
}

[data-testid="stRadio"] label {
    background: #fff8e8 !important;
    border: 2px solid #1f1308 !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    margin: 8px 0 !important;
}

[data-testid="stRadio"] label * {
    color: #1f1308 !important;
    font-weight: 800 !important;
}

[data-testid="stMetric"] {
    background: #fff8e8;
    border: 2px solid #1f1308;
    border-radius: 10px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)

if "inicio" not in st.session_state:
    st.session_state.inicio = True

if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = 0
    st.session_state.order = list(df.index)
    random.shuffle(st.session_state.order)
    st.session_state.answered = False
    st.session_state.feedback = None

def reset():
    st.session_state.inicio = True
    st.session_state.i = 0
    st.session_state.score = 0
    st.session_state.order = list(df.index)
    random.shuffle(st.session_state.order)
    st.session_state.answered = False
    st.session_state.feedback = None

if st.session_state.inicio:
    st.title("🗺️ Ruta del Deporte Argentino")
    st.subheader("🏹 ─ 🐎 ─ ⚽ ─ 🥇 ─ 🏆")

    st.write(
        "Un viaje por etapas para repasar la historia del deporte argentino: "
        "pueblos originarios, prácticas criollas, inmigración, clubes, Juegos Olímpicos y memoria."
    )

    c1, c2, c3 = st.columns(3)
    c1.info("🏹 Orígenes")
    c2.info("⚽ Clubes")
    c3.info("🏆 Hazañas")

    if st.button("Iniciar recorrido", use_container_width=True):
        st.session_state.inicio = False
        st.rerun()

    st.stop()

if st.session_state.i >= len(df):
    pct = (st.session_state.score / len(df)) * 100

    st.title("🏁 Resultado final")

    col1, col2 = st.columns(2)
    col1.metric("Puntaje", f"{st.session_state.score}/{len(df)}")
    col2.metric("Porcentaje", f"{pct:.0f}%")

    if pct >= 85:
        st.success("🏆 Guía experto del deporte argentino")
    elif pct >= 60:
        st.info("🥈 Viajero histórico bien preparado")
    elif pct >= 35:
        st.warning("📚 Explorador curioso")
    else:
        st.error("🔎 Hay que volver a recorrer la bibliografía")

    if st.button("Reiniciar recorrido", use_container_width=True):
        reset()
        st.rerun()

    st.stop()

q_idx = st.session_state.order[st.session_state.i]
row = df.loc[q_idx]

st.progress(st.session_state.i / len(df))

st.write(f"**Etapa {st.session_state.i + 1} de {len(df)}**  |  **Puntaje:** {st.session_state.score}")

st.subheader(f"📍 {row['era']}")
st.title(row["pregunta"])

options = [
    row["opcion_1"],
    row["opcion_2"],
    row["opcion_3"],
    row["opcion_4"]
]

choice = st.radio(
    "Elegí una opción:",
    options,
    index=None,
    disabled=st.session_state.answered
)

if st.button(
    "Responder",
    disabled=choice is None or st.session_state.answered,
    use_container_width=True
):
    correct = int(row["correcta"])

    if options.index(choice) == correct:
        st.session_state.score += 1
        st.session_state.feedback = "correcta"
    else:
        st.session_state.feedback = f"incorrecta|{options[correct]}"

    st.session_state.answered = True
    st.rerun()

if st.session_state.answered:
    if st.session_state.feedback == "correcta":
        st.success("✔ Correcto")
    else:
        correcta = st.session_state.feedback.split("|", 1)[1]
        st.error(f"✘ Incorrecto. La respuesta correcta era: {correcta}")

    st.info(f"📌 Dato de ruta: {row['fact']}")

    if st.button("Avanzar a la siguiente etapa", use_container_width=True):
        st.session_state.i += 1
        st.session_state.answered = False
        st.session_state.feedback = None
        st.rerun()
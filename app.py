from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
from streamlit_lottie import st_lottie
import json

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Análisis de Sentimiento",
    page_icon="😊",
    layout="centered"
)

# ------------------ ESTILOS VISIBLES ------------------
st.markdown("""
<style>

/* Título principal */
h1 {
    color: #f5be8e !important;
    text-align: center;
}

/* Subtítulo */
h3 {
    color: #8cedb0 !important;
}

/* Expander (card real) */
div[data-testid="stExpander"] {
    border: 2px solid #FF5733;
    border-radius: 12px;
    background-color: #FFF4F2;
    padding: 10px;
}

/* Header del expander */
div[data-testid="stExpander"] > div:first-child {
    background-color: #FF5733;
    color: white;
    font-weight: bold;
    border-radius: 10px;
}

/* Caja de resultados */
.result-box {
    background-color: #D4EFDF;
    border-left: 8px solid #2ECC71;
    padding: 15px;
    border-radius: 10px;
    color: black;
    font-size: 16px;
    margin-top: 10px;
}

/* Input */
input {
    border: 2px solid #FF5733 !important;
    border-radius: 8px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #4287a1;
}

/* Imagen centrada */
img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.title('Análisis de Sentimiento')

image = Image.open('sentimental.jpg')
st.image(image, width=250)

st.subheader("Escribe la frase que deseas analizar")

translator = Translator()

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.subheader("📊 Polaridad y Subjetividad")
    st.write("""
    **Polaridad:** de -1 (negativo) a 1 (positivo)  
    **Subjetividad:** de 0 (objetivo) a 1 (subjetivo)
    """)

# ------------------ EXPANDER ------------------
with st.expander('📝 Analizar texto'):
    text = st.text_input('Escribe aquí:')

    if text:
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        # RESULTADOS (MUY VISIBLES)
        st.markdown(f"""
        <div class="result-box">
        🔹 <b>Polaridad:</b> {polarity} <br>
        🔹 <b>Subjetividad:</b> {subjectivity}
        </div>
        """, unsafe_allow_html=True)

        # CLASIFICACIÓN
        if polarity > 0.0 and polarity < 1.0:
            st.success('Es un sentimiento Positivo 😊')
            with open('cat2.json') as source:
                animation = json.load(source)
            st_lottie(animation, width=120)

        elif polarity > -1 and polarity < 0:
            st.error('Es un sentimiento Negativo 😔')
            with open('cat.json') as source:
                animation = json.load(source)
            st_lottie(animation, width=120)

        else:
            st.warning('Es un sentimiento Neutral 😐')
            with open('cat3.json') as source:
                animation = json.load(source)
            st_lottie(animation, width=120)

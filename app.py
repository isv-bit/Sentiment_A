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

# ------------------ ESTILOS (SIN CAMBIAR FONDO GENERAL) ------------------
st.markdown("""
<style>

/* Título */
h1 {
    color: #2E86C1;
    text-align: center;
}

/* Subtítulos */
h3 {
    color: #117A65;
}

/* Expander (simula card simple) */
.streamlit-expanderHeader {
    background-color: #D6EAF8;
    border-radius: 8px;
    padding: 8px;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F4F6F7;
}

/* Texto destacado */
.result-box {
    background-color: #EBF5FB;
    padding: 10px;
    border-radius: 8px;
    margin-top: 10px;
    color: #1B4F72;
    font-weight: 500;
}

/* Input */
.stTextInput>div>div>input {
    border-radius: 8px;
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

image = Image.open('emoticones.jpg')
st.image(image, width=250)

st.subheader("Escribe la frase que deseas analizar")

translator = Translator()

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.subheader("📊 Polaridad y Subjetividad")
    st.write("""
    **Polaridad:**  
    Va de -1 (negativo) a 1 (positivo).

    **Subjetividad:**  
    Va de 0 (objetivo) a 1 (subjetivo).
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

        # RESULTADOS
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

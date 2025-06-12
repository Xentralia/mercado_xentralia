###################################################
#              Generador de leads                 #
# V.2.0.0 //25 04 2025//                          #
# V.2.0.3 //30 05 2025//                          #
# V.2.1.3 //30 05 2025//                          #
# V.2.2.3 //05 06 2025//                          #
# Desplegado con streamlit                        #
# Agente impulsado con OpenAI                     #
# Desarrollador: Sergio Emiliano López Bautista   #
###################################################


# ------------------------- Requerimentos y librerías -------------------------------
import io
import os
import time
import codecs
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from utils.prompts import construir_prompt

# --------------------------- Seteadores ----------------------------------------------
st.set_page_config(page_title="Estudio de mercado", layout="wide")

dotenv_path = find_dotenv()
load_dotenv(dotenv_path, override=True)
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
#client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

st.title("Estudio de mercado")

# --------------------------- Funciones -----------------------------------------------
def agente(tema):
    datos = {"tema": tema}
    prompt = construir_prompt('data/plantilla01_OpenAI.txt', datos)
    try:
        agente = client.responses.create(
        model= "gpt-4.1",
        input= prompt
        )
        return agente.output_text
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def maquina_de_escribir(respuesta):
    for word in respuesta.split(" "):
        yield word + " "
        time.sleep(0.02)

def instrucciones():
    if not os.path.exists("data/instrucciones.txt"):
        raise FileNotFoundError(f"El archivo {"data/instrucciones.txt"} no existe.")

    with codecs.open("data/instrucciones.txt", "r", encoding="utf-8") as f:
        fi = f.read()
    file = fi.split('\n')

    for linea in file:
        st.markdown(linea)

# -------------------------------- Interfaz (MAIN)-------------------------------------

with st.sidebar:
    st.markdown("## ¡Bienvenido!")
    instrucciones()
    tema = st.text_input("¿De qué tema buscas información?")
    inv = st.button("Investigar")

    
if inv:
    if tema:
        with st.spinner("investigando..."):
            st.markdown("### Vista previa de la información")
            st.write_stream(maquina_de_escribir(agente(tema)))
    else:
        st.markdown("Por favor, completa el campo.")
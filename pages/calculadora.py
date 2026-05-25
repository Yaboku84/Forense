import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math
import serial
import time


@st.cache_resource
def iniciar_arduino():
    try:
        
        puerto = serial.Serial(port='COM3', baudrate=9600, timeout=1)
        time.sleep(2) 
        return puerto
    
    except Exception as e:
        st.error(f"No se pudo conectar al Arduino: {e}")
        return None

arduino = iniciar_arduino()

from calculos import estimar, obtener_k, Factor_Eh
from database import crear_db, guardar_caso, cargar_casos, eliminar_caso

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculos import estimar, obtener_k, Factor_Eh
from database import crear_db, guardar_caso, cargar_casos, eliminar_caso
# Crear la BD al iniciar (si no existe)
crear_db()

if st.button("← Volver al menú"):
    st.switch_page("pages/inicio.py")

st.title(
    "Estimador de Tiempo de Muerte" 
)

# ── Sidebar ──────────────────────────────
with st.sidebar:
    st.header("Parámetros de entrada")

    temp_corp = st.slider("Temperatura corporal (°C)", 20.0, 37.0, 30.0, 0.5)
    temp_rect = st.slider("Temperatura rectal (°C)", 20.0, 40.0, 35.0, 0.5)
    temp_amb  = st.slider("Temperatura ambiente (°C)", 5.0, 40.0, 20.0, 0.5)
    humedad   = st.slider("Humedad (%)", 0, 100, 50)
    peso      = st.slider("Peso corporal (kg)", 40, 150, 70, 5)

    condicion = st.selectbox("Condición del entorno", [
        "Aire libre, sin ropa", "Ropa ligera",
        "Ropa gruesa / cobija",
        "Sumergido en agua fría", "Sumergido en agua tibia"
    ])
    grado_rigor = st.selectbox(
        "Rigor mortis",
        ["Ausente", "Parcial", "Completo", "Cediendo"]
    )
    estado_livor = st.selectbox(
        "Livor mortis", ["No fijado", "Fijado"]
    )

    st.divider()
    nombre_caso = st.text_input("Nombre del caso", placeholder="Caso #001")
    guardar_btn = st.button("💾 Guardar caso", use_container_width=True)

# ── Cálculo ──────────────────────────────
res = estimar(temp_corp, temp_amb, condicion, peso, grado_rigor, estado_livor, temp_rect)

# ── Métricas ─────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("⏱ Estimación central", f"{res['centro']} h")
col2.metric(" Rango (en horas)", f"{res['rango'][0]} – {res['rango'][1]} h")
col3.metric(" Confianza", f"{res['confianza']}%")

st.divider()

# ── Indicadores + Gráfica ────────────────
left, right = st.columns([1, 1.6])

with left:
    st.subheader("Indicadores")

    with st.expander("🌡 Algor mortis", expanded=True):
        if res["algor_h"]:
            st.metric("Estimación", f"{res['algor_h']} h")
            st.caption(f"Constante k = {res['k']} h⁻¹")
            st.markdown("[Para conocer mas CLIK](https://www.formacionfuneraria.com/signos-positivos-de-la-muerte-algor-mortis/)", unsafe_allow_html=True)
        else:
            st.warning("Temperatura corporal ≤ ambiente.")

    with st.expander(" Rigor mortis", expanded=False):
        lo, hi, desc = res["rigor"]
        st.write(desc)
        st.caption(f"Rango: {lo} – {hi} h")
        st.markdown("[Para conocer mas CLIK](https://www-sciencedirect-com.translate.goog/topics/medicine-and-dentistry/rigor-mortis?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc)", unsafe_allow_html=True)

    with st.expander(" Livor mortis", expanded=False):
        lo, hi, desc = res["livor"]
        st.write(desc)
        st.caption(f"Rango: {lo} – {hi} h")
        st.markdown("[Para conocer mas CLIK](https://www.univadis.es/viewarticle/hablemos-del-color-muerte-livor-mortis-2024a1000idb)", unsafe_allow_html=True)
        
    with st.expander(" Glaiseter ", expanded=False):
        hgla  = res["hgla"]
        st.metric("Estimación", f"{res['hgla']} h")
        st.caption(f" Factor de enfriamiento= {res['Eh']}°C/h")

with right:
    st.subheader("Curva de enfriamiento (Algor Mortis)")
    if res["algor_h"]:
        horas = [i * 0.25 for i in range(121)]
        temps = [temp_amb + (37 - temp_amb) * math.exp(-res["k"] * t)
                 for t in horas]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=horas, y=temps, mode="lines",
            name="Temperatura corporal",
            line=dict(color="#1D289B", width=3.5)
        ))
        fig.add_hline(
            y=temp_amb, line_dash="dash", line_color="#888",
            annotation_text=f"T° ambiente ({temp_amb}°C)",
            annotation_position="bottom right"
        )
        fig.add_vrect(
            x0=max(0, res["algor_h"] - 2),
            x1=res["algor_h"] + 2,
            fillcolor="rgba(0,0,160,0.12)",
            line_width=0,
            annotation_text="Rango estimado"
        )
        fig.update_layout(
            xaxis_title="Horas desde la muerte",
            yaxis_title="Temperatura (°C)",
            template="plotly_white",
            height=380,
            margin=dict(t=30, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Narrativa ────────────────────────────
st.divider()
st.info(
    f" Con temperatura corporal de {temp_corp}°C "
    f"(ambiente {temp_amb}°C) y rigor mortis **{grado_rigor}**, "
    f"la muerte ocurrió hace aprox. **{res['rango'][0]} – {res['rango'][1]} horas**. "
    f"Confianza: **{res['confianza']}%**."
)
st.info(
    "Proyecto Final Lenguajes de Programación 🙏"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Creditos", use_container_width=True):
        st.switch_page("pages/creditos.py")

# ── Guardar ──────────────────────────────
if guardar_btn:
    if nombre_caso.strip():
        guardar_caso(nombre_caso, {
            "temp_corp": temp_corp, "temp_amb": temp_amb,
            "humedad": humedad, "factor_en": res["k"],
            "peso": peso, "temp_rect": temp_corp,
            "rigor": grado_rigor, "livor": estado_livor,
            "temp_rect": temp_rect
        }, res)
        st.sidebar.success(f" '{nombre_caso}' guardado.")
    else:
        st.sidebar.error("Escribe un nombre para el caso.")

# ── Historial ────────────────────────────
st.divider()
st.subheader("📁 Casos anteriores")

casos = cargar_casos()
if casos:
    df = pd.DataFrame([{
        "ID":       c["id"],
        "Nombre":   c["nombre"],
        "Fecha":    c["fecha"],
        "Est. (h)": c["tiempo_estimado"],
        "Rango":    f"{c['rango_lo']} – {c['rango_hi']} h",
        "Confianza":f"{c['nivel_confianza']}%",
    } for c in casos])
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Eliminar caso por ID
    with st.expander("🗑 Eliminar un caso"):
        id_borrar = st.number_input("ID del caso a eliminar",
                                     min_value=1, step=1)
        if st.button("Eliminar"):
            eliminar_caso(id_borrar)
            st.success(f"Caso {id_borrar} eliminado.")
            st.rerun()
else:
    st.caption("Aún no hay casos guardados.")


if arduino:

    if condicion == "Aire libre, sin ropa":   arduino.write(b'A')
    elif condicion == "Ropa ligera":          arduino.write(b'B') 
    elif condicion == "Ropa gruesa / cobija": arduino.write(b'C')
    elif condicion == "Sumergido en agua fría": arduino.write(b'D')
    elif condicion == "Sumergido en agua tibia": arduino.write(b'E')

    if grado_rigor == "Ausente":   arduino.write(b'F')
    elif grado_rigor == "Parcial":  arduino.write(b'G')
    elif grado_rigor == "Completo": arduino.write(b'H')
    elif grado_rigor == "Cediendo": arduino.write(b'I')

    if estado_livor == "No fijado": arduino.write(b'J')
    elif estado_livor == "Fijado":    arduino.write(b'K')
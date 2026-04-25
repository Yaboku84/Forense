import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math

# ← Importamos nuestros propios módulos
from calculos import estimar, obtener_k
from database import crear_db, guardar_caso, cargar_casos, eliminar_caso

# Crear la BD al iniciar (si no existe)
crear_db()

# ── Configuración ────────────────────────
st.set_page_config(
    page_title="Estimador Forense",
    page_icon="🔬",
    layout="wide"
)
st.title(" Estimador de Tiempo de Muerte")
st.caption("Análisis multiparamétrico · Algor, Rigor y Livor Mortis")

# ── Sidebar ──────────────────────────────
with st.sidebar:
    st.header("Parámetros de entrada")

    temp_corp = st.slider("Temperatura corporal (°C)", 20.0, 37.0, 30.0, 0.5)
    temp_amb  = st.slider("Temperatura ambiente (°C)", 5.0, 35.0, 20.0, 0.5)
    humedad   = st.slider("Humedad (%)", 0, 100, 50)
    peso      = st.slider("Peso corporal (kg)", 40, 150, 70, 5)

    condicion = st.selectbox("Condición del entorno", [
        "Aire libre, sin ropa", "Ropa ligera",
        "Ropa gruesa / cobija",
        "Sumergido en agua fría", "Sumergido en agua tibia"
    ])
    grado_rigor = st.selectbox(
        "Rigor mortis",
        ["ausente", "parcial", "completo", "cediendo"]
    )
    estado_livor = st.selectbox(
        "Livor mortis", ["no fijado", "fijado"]
    )

    st.divider()
    nombre_caso = st.text_input("Nombre del caso", placeholder="Caso #001")
    guardar_btn = st.button("💾 Guardar caso", use_container_width=True)

# ── Cálculo ──────────────────────────────
res = estimar(temp_corp, temp_amb, condicion, peso, grado_rigor, estado_livor)

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
        else:
            st.warning("Temperatura corporal ≤ ambiente.")

    with st.expander(" Rigor mortis", expanded=True):
        lo, hi, desc = res["rigor"]
        st.write(desc)
        st.caption(f"Rango: {lo} – {hi} h")

    with st.expander(" Livor mortis", expanded=True):
        lo, hi, desc = res["livor"]
        st.write(desc)
        st.caption(f"Rango: {lo} – {hi} h")

with right:
    st.subheader("Curva de enfriamiento")
    if res["algor_h"]:
        horas = [i * 0.25 for i in range(121)]
        temps = [temp_amb + (37 - temp_amb) * math.exp(-res["k"] * t)
                 for t in horas]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=horas, y=temps, mode="lines",
            name="Temperatura corporal",
            line=dict(color="#E24B4A", width=2.5)
        ))
        fig.add_hline(
            y=temp_amb, line_dash="dash", line_color="#888",
            annotation_text=f"T° ambiente ({temp_amb}°C)",
            annotation_position="bottom right"
        )
        fig.add_vrect(
            x0=max(0, res["algor_h"] - 2),
            x1=res["algor_h"] + 2,
            fillcolor="rgba(226,75,74,0.12)",
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

# ── Guardar ──────────────────────────────
if guardar_btn:
    if nombre_caso.strip():
        guardar_caso(nombre_caso, {
            "temp_corp": temp_corp, "temp_amb": temp_amb,
            "humedad": humedad, "factor_en": res["k"],
            "peso": peso, "temp_rect": temp_corp,
            "rigor": grado_rigor, "livor": estado_livor
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
st.rerun()
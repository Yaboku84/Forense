import streamlit as st
import pandas as pd

@st.cache_data
def cargar_casos_detective():
    df = pd.read_excel("casos_detective.xlsx", sheet_name="Casos")

    for col in ["opcion_a", "opcion_b", "opcion_c", "opcion_correcta"]:
        if col in df.columns:
            df[col] = df[col].fillna("")
    return df.to_dict("records")

def tiene_opciones(caso):
    return bool(caso.get("opcion_a", "").strip())

def validar_numerica(estimado, correcto):
    diff = estimado - correcto
    if abs(diff) <= 3:
        return "correcto"
    elif diff < -3:
        return "muy_temprano"
    else:
        return "muy_tarde"

COLORES_DIFICULTAD = {
    "Fácil":   ("🟢", "#2E7D32"),
    "Medio":   ("🟡", "#F57F17"),
    "Difícil": ("🔴", "#B71C1C"),
}

for key, default in [
    ("det_caso_activo", None),
    ("det_resultado", None),
    ("det_pista1", False),
    ("det_pista2", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


if st.session_state.det_caso_activo is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.title("🕵️ Modo Detective")
        st.markdown("Pon a prueba tus habilidades forenses. Analiza la escena y estima el tiempo de muerte.")
        
    with col3:
        st.markdown("""
    <div style='text-align:center'>
        <img src='https://images.librotea.com/uploads/media/2022/06/28/los-otros-sherlock-holmes-los-mejores-detectives-literarios.jpg' width='300'>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("Tutorial"):
            st.switch_page("pages\Tutorial.py")
          
   
    st.divider()

    try:
        casos = cargar_casos_detective()
    except FileNotFoundError:
        st.error("No se encontró `casos_detective.xlsx`")
        st.stop()

    st.subheader("Selecciona un caso")

    for caso in casos:
        emoji, color = COLORES_DIFICULTAD.get(caso["dificultad"], ("⚪", "#555"))
        tipo_badge = "🔘 Opción múltiple" if tiene_opciones(caso) else "🔢 Estimación numérica"

        with st.container(border=True):
            col_txt, col_btn = st.columns([4, 1])
            with col_txt:
                st.markdown(
                    f"**{caso['titulo']}** &nbsp;"
                    f"<span style='color:{color};font-weight:bold'>{emoji} {caso['dificultad']}</span> &nbsp;"
                    f"<span style='color:#888;font-size:0.85em'>{tipo_badge}</span>",
                    unsafe_allow_html=True
                )
                preview = caso["descripcion"][:120]
                if len(caso["descripcion"]) > 120:
                    preview += "…"
                st.caption(preview)
            with col_btn:
                if st.button("Investigar →", key=f"caso_{caso['id']}", use_container_width=True):
                    st.session_state.det_caso_activo = caso
                    st.session_state.det_resultado = None
                    st.session_state.det_pista1 = False
                    st.session_state.det_pista2 = False
                    st.rerun()

    st.divider()
    if st.button("← Volver al inicio"):
        st.switch_page("pages\inicio.py")

else:
    caso = st.session_state.det_caso_activo
    emoji, color = COLORES_DIFICULTAD.get(caso["dificultad"], ("⚪", "#555"))
    es_multiple = tiene_opciones(caso)

    st.title(f" {caso['titulo']}")
    st.markdown(
        f"<span style='color:{color};font-weight:bold'>{emoji} {caso['dificultad']}</span>",
        unsafe_allow_html=True
    )
    st.divider()

    st.subheader(" Descripción de la escena")
    st.info(caso["descripcion"])
    st.divider()

    st.subheader(" Datos forenses")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡 Temp. rectal",   f"{caso['temp_rect']} °C")
    c2.metric("🌤 Temp. ambiente", f"{caso['temp_amb']} °C")
    c3.metric(" Peso",           f"{caso['peso']} kg")
    c4.metric(" Condición",      caso["condicion"])

    c5, c6 = st.columns(2)
    c5.metric(" Rigor mortis", caso["rigor"])
    c6.metric(" Livor mortis", caso["livor"])
    st.divider()

    st.subheader(" Pistas")
    p1, p2 = st.columns(2)
    with p1:
        if st.button("Desbloquear Pista 1", use_container_width=True):
            st.session_state.det_pista1 = True
        if st.session_state.det_pista1:
            st.success(f"**Pista 1:** {caso['pista_1']}")
    with p2:
        if st.button("Desbloquear Pista 2", use_container_width=True):
            st.session_state.det_pista2 = True
        if st.session_state.det_pista2:
            st.warning(f"**Pista 2:** {caso['pista_2']}")
    st.divider()

    if es_multiple:
        st.subheader(" ¿Cuándo ocurrió la muerte?")
        opciones = [
            caso["opcion_a"],
            caso["opcion_b"],
            caso["opcion_c"],
        ]
        seleccion = st.radio(
            "Selecciona el rango más probable:",
            opciones,
            index=None,
            key="det_radio"
        )

        if st.button(" Enviar respuesta", use_container_width=True):
            if seleccion is None:
                st.warning("Selecciona una opción antes de enviar.")
            else:
                correcta = caso["opcion_correcta"].strip()
                if seleccion.strip() == correcta:
                    st.session_state.det_resultado = ("correcto", correcta)
                else:
                    st.session_state.det_resultado = ("incorrecto", correcta)

        if st.session_state.det_resultado:
            estado, correcta = st.session_state.det_resultado
            if estado == "correcto":
                st.success(f" **¡Correcto!** La respuesta era **{correcta}**. Excelente trabajo, detective.")
            else:
                st.error(f" **Incorrecto.** La respuesta correcta era **{correcta}**.")

    else:
        st.subheader("⏱ Tu estimación")
        estimado = st.number_input(
            "¿Hace cuántas horas ocurrió la muerte?",
            min_value=0.0, max_value=100.0, value=8.0, step=0.5
        )

        if st.button(" Enviar respuesta", use_container_width=True):
            categoria = validar_numerica(estimado, caso["respuesta_correcta_h"])
            st.session_state.det_resultado = (categoria, caso["respuesta_correcta_h"])

        if st.session_state.det_resultado:
            estado, correcto = st.session_state.det_resultado
            if estado == "correcto":
                st.success(f" **¡Correcto!** La muerte ocurrió hace aprox. **{correcto} h**.")
            elif estado == "muy_temprano":
                st.error("⬆️ **Muy temprano.** La muerte fue más antigua de lo que calculaste.")
                st.caption(f"Respuesta correcta: **{correcto} h**")
            else:
                st.error("⬇️ **Muy tarde.** La muerte fue más reciente de lo que calculaste.")
                st.caption(f"Respuesta correcta: **{correcto} h**")

    st.divider()

    col_volver, col_menu = st.columns(2)
    with col_volver:
        if st.button("← Volver a casos", use_container_width=True):
            st.session_state.det_caso_activo = None
            st.session_state.det_resultado = None
            st.rerun()
    with col_menu:
        if st.button("🏠 Menú principal", use_container_width=True):
            st.session_state.det_caso_activo = None
            st.switch_page("pages\inicio.py")
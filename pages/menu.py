import streamlit as st

if "iniciado" not in st.session_state:
    st.session_state.iniciado = False

if not st.session_state.iniciado:
    pg = st.navigation(
        [
            st.Page("app.py", title="Inicio", icon="🏠"),
            st.Page("pages/detective.py", title="Detective", icon="🔍"),
        ], position="hidden"
    )
    
    st.markdown("<h1 style='text-align:center'>ESTIMADOR FORENSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Sistema de análisis multiparamétrico</p>", unsafe_allow_html=True)
        
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(" Iniciar Calculadora", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        if st.button("🕵️ Modo Detective", use_container_width=True):
           st.switch_page("pages/detective.py")
    
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
    <div style='text-align:center'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/d/d4/True_Detective_logo.png' width='300'>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
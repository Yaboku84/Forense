import streamlit as st

st.set_page_config(
    page_title="Estimador Forense",
    page_icon="🔬",
    layout="wide"
)

pg = st.navigation(
    [
        st.Page("pages/inicio.py", title="Inicio", icon="🏠"),
        st.Page("pages/calculadora.py", title="Calculadora", icon="🔬"),
        st.Page("pages/detective.py", title="Detective", icon="🔍"),
        st.Page("pages/info.py", title="Acerca de..."),
        st.Page("pages/creditos.py", title="Creditos"),
        st.Page("pages/Tutorial.py", title="Tuturial")
    ], position="hidden"
)

pg.run()
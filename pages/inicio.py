import streamlit as st

st.markdown("<h1 style='text-align:center'>ESTIMADOR FORENSE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Sistema de análisis multiparamétrico</p>", unsafe_allow_html=True)

st.divider()

col1, col2,col3 = st.columns(3)

with col1:
    if st.button("Iniciar Calculadora", use_container_width=True):
        st.switch_page("pages/calculadora.py")

with col2:
    if st.button("🕵️ Modo Detective", use_container_width=True):
        st.switch_page("pages/detective.py")

with col3:
    if st.button(" Acerca de...", use_container_width=True):
        st.switch_page("pages/info.py")

st.divider()
st.markdown("""
<div style='text-align:center'>
    <img src='https://vyorsa.com.mx/media/amasty/blog/uploads/null-5.jpeg' width='300'>
</div>
""", unsafe_allow_html=True)
    

st.divider()
col1, col2,col3 = st.columns([1, 2, 1])


with col2:
    st.markdown("""
<div style='text-align:center'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/d/d4/True_Detective_logo.png' width='300'>
</div>
""", unsafe_allow_html=True)
    

st.divider()


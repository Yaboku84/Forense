import streamlit as st

if st.button("← Volver al menú"):
    st.switch_page("pages/inicio.py")

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h1 style='text-align:center'>Proyecto final Lenguajes de Programación</p>", unsafe_allow_html=True)
    st.markdown("""
<div style='text-align:center'>
    <img src='https://www.fundacionunam.org.mx/wp-content/uploads/2019/07/FELIZ2.jpg' width='300'>
</div>
""", unsafe_allow_html=True)
    

with col2:
    st.markdown("<h1 style='text-align:center'>Integrantes</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Ana Carolina Venzor Moreno</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Adriana Ibeth Moreno Montalvo</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Alfredo Emiliano Corcuera Castañeda</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Axel Gael Becerra Galliazzi</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Juan Pablo Villaseñor Lozoya</p>", unsafe_allow_html=True)


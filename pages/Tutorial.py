import streamlit as st

if st.button("← Volver al menú"):
    st.switch_page("pages/detective.py")

st.divider()
st.markdown("<h1 style='text-align:center'>Tutorial</p>", unsafe_allow_html=True)

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h1 style='text-align:center'>Paso 1: Analizar el Enfriamiento (Algor Mortis)</p>", unsafe_allow_html=True)

    st.markdown("""

La temperatura es el dato más preciso en las primeras 24 horas. El cuerpo humano sano está a 37 °C.

Calcula la pérdida: Resta la temperatura rectal del caso a los 37 °C teóricos.

Aplica la Regla de Glaister (Estándar): En condiciones templadas, un cuerpo pierde aproximadamente 1 °C por hora durante las primeras 12 horas, y 0.5 °C por hora las siguientes 12.

Modifica por el Entorno y Peso:

¿Hace calor o el cuerpo está muy abrigado? El enfriamiento se ralentiza (perderá menos de 1 °C/h).

¿Hace frío o el cuerpo está desnudo/delgado? El enfriamiento se acelera (perderá más de 1 °C/h).
""")
    st.markdown("""
<div style='text-align:center'>
    <img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0uzuRQWtQkDd3IdF12Lx9KEJaSvku19HgZA&s' width='300'>
</div>
""", unsafe_allow_html=True)
    

with col2:
    st.markdown("<h1 style='text-align:center'>Paso 2: Evaluar la Rigidez (Rigor Mortis)</p>", unsafe_allow_html=True)

    st.markdown("""
La rigidez es un proceso químico (falta de ATP en los músculos) que sigue una dirección constante de arriba hacia abajo (Ley de Nysten): Mandíbula ➡️ Cuello ➡️ Tronco ➡️ Brazos ➡️ Piernas.

Usa esta escala de tiempo estándar para orientarte:

Fase de Inicio (3 a 6 horas): La rigidez solo se nota en la mandíbula, el cuello y empieza en las manos.

Fase de Estado / Máxima Rigidez (8 a 15 horas): Todo el cuerpo está completamente rígido ("tieso"). Si intentas mover un brazo, cuesta mucho trabajo.

Fase de Resolución (24 a 36 horas): La rigidez desaparece en el mismo orden en que empezó (la mandíbula vuelve a estar laxa, pero las piernas siguen rígidas).
""")
    
    st.markdown("""
<div style='text-align:center'>
    <img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-1Xh9_edFgsFwEjzve9kayKaQxvFjyzSILg&s' width='300'>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center'>Paso 3: Revisar las Livideces (Livor Mortis)</p>", unsafe_allow_html=True)

st.markdown("""

Son las manchas de color violáceo que aparecen en las zonas bajas del cuerpo debido a la gravedad, ya que el corazón dejó de bombear la sangre.

Menos de 12 horas (Modificables): Si cambias el cuerpo de posición o presionas fuertemente la mancha con el dedo, la sangre se mueve y la piel se pone blanca por un momento.

Más de 12 a 15 horas (Fijadas): La sangre ya se salió de los vasos capilares y tiñó el tejido. Aunque muevas el cuerpo o presiones la mancha, el color violáceo ya no cambia ni desaparece.
""")

st.markdown("""
    <div style='text-align:center'>
        <img src='https://www.perspectivas.med.br/wp-content/uploads/2019/02/Fig1.jpg' width='300'>
    </div>
    """, unsafe_allow_html=True)
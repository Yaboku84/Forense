import streamlit as st

if st.button("← Volver al menú"):
    st.switch_page("pages/inicio.py")

st.divider()
st.markdown("<h1 style='text-align:center'>Acerca de...</p>", unsafe_allow_html=True)

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h1 style='text-align:center'>Introducción</p>", unsafe_allow_html=True)

    st.markdown("""

El estudio de los fenómenos cadavéricos es uno de los pilares fundamentales de la medicina forense, crucial para resolver incógnitas en investigaciones criminales y judiciales. Tras el deceso de un individuo, el cuerpo humano experimenta una serie de cambios físicos, químicos y biológicos predecibles. El análisis preciso de estos cambios permite a los peritos forenses determinar el Intervalo Post-Mórtem (IPM), es decir, el tiempo estimado que ha transcurrido desde el momento de la muerte hasta el hallazgo del cadáver.

Para comprender cómo se calcula este intervalo, es imperativo analizar la tríada clásica de los fenómenos cadavéricos tempranos: Algor mortis, Livor mortis y Rigor mortis.

Los Fenómenos Cadavéricos Tempranos
Algor Mortis (Enfriamiento Cadavérico): Es el proceso mediante el cual el cuerpo pierde calor gradualmente hasta igualar la temperatura del medio ambiente. Dado que el centro termorregulador deja de funcionar, la pérdida de temperatura corporal sigue una curva relativamente predecible, influenciada por factores externos (clima, ropa) e internos (masa corporal). Es uno de los indicadores más cuantitativos para las primeras 24 horas.

Livor Mortis (Livideces Cadavéricas): Tras el cese de la función cardíaca, la sangre refluye por gravedad hacia las zonas declives del cuerpo, acumulándose en los capilares y tiñendo la piel de un color purpúreo o rojizo. Las livideces comienzan a aparecer entre las primeras 2 a 4 horas, y su fijación (cuando ya no cambian de posición al mover el cuerpo) aporta datos clave sobre la posición original del cadáver y el tiempo transcurrido.

Rigor Mortis (Rigidez Cadavérica): Es el estado de endurecimiento y retracción de los músculos del cuerpo. Ocurre debido a la degradación del ATP celular; al no haber energía, las proteínas musculares (actina y miosina) se quedan acopladas permanentemente. La rigidez inicia típicamente en los músculos pequeños de la cara (mandíbula) y desciende gradualmente por el tronco y las extremidades, desapareciendo en el mismo orden cuando inicia la putrefacción.
""")
    st.markdown("""
<div style='text-align:center'>
    <img src='https://vyorsa.com.mx/media/amasty/blog/uploads/null-5.jpeg' width='300'>
</div>
""", unsafe_allow_html=True)
    

with col2:
    st.markdown("<h1 style='text-align:center'>Sobre la Aplicación: Calculadora Forense e Interfaz Dinámica</p>", unsafe_allow_html=True)

    st.markdown("""


Con el objetivo de optimizar, digitalizar y agilizar el trabajo en el campo de la criminalística, se ha desarrollado esta herramienta tecnológica interactiva. La aplicación funciona como un sistema de soporte para el análisis forense a través de dos componentes principales:

1. Calculadora de Intervalo Post-Mórtem (IPM)
Esta sección automatiza el cálculo matemático del tiempo de muerte utilizando modelos estandarizados de la medicina forense, principalmente el Nomograma de Henssge. Al ingresar variables críticas y objetivas —como la temperatura rectal del cadáver, la temperatura ambiental en el lugar del hallazgo, el peso del individuo y los factores de corrección por las condiciones del entorno (ropa, humedad, cuerpo en el agua, etc.)—, el sistema procesa los algoritmos instantáneamente. Esto reduce el margen de error humano y proporciona una estimación precisa del IPM con sus respectivos límites de confianza.

2. El "Modo Detective"
Diseñado como una interfaz de diagnóstico cualitativo y exploración guiada, el Modo Detective permite al usuario evaluar un escenario de manera integral. A través de la observación y el cotejo de los fenómenos físicos del cadáver (la extensión y fijación de las livideces, el avance de la rigidez muscular y los signos macroscópicos de deshidratación u otros cambios), el usuario puede interactuar con la aplicación para reconstruir las condiciones del hallazgo. Esta modalidad complementa los datos numéricos de la calculadora, ofreciendo una perspectiva contextual y deductiva indispensable para cualquier investigación pericial.
""")
    
    st.markdown("""
<div style='text-align:center'>
    <img src='https://www.esneca.com/wp-content/uploads/que-es-ciencia-forense-1200x720.jpg' width='300'>
</div>
""", unsafe_allow_html=True)

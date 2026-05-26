import streamlit as st
from streamlit_option_menu import option_menu

import base64


def get_img_as_base64(file):
    with open(file,"rb") as f:
        data=f.read()
    return base64.b64encode(data).decode()

#img=get_img_as_base64("logofer.png")

# bg_imagen=f"""
# <style>
# [data-testid="stSidebar"]>div:first-child{{
# background-image:url("data:fondo/png;base64,{img}");
# background-position:center;
# }}
# </style>
#    """

# def menu():
#     #variable para mostrar o ocultar el contnedor de botones
#     st.session_state.mostrar_contenedor_botones=False
#     st.markdown(bg_imagen,unsafe_allow_html=True)
#     with st.sidebar:
#         selected=option_menu(
#             menu_title="Menu",
#             options=["Principal","Entrega","Traslado","Chat","Reportes","Planificación","Asignacion"],
#             icons=["house","box-seam","truck","chat-left-text","list-check","list-check","list-check"],
            
#         )
        
#         st.sidebar.success("Selecciona página")
#     if selected == "Principal":
#         Principal.principal()
#     elif selected == "Entrega":
#         Entrega.entrega()
#     elif selected == "Reportes":
#         Reportes.reportes()
#     elif selected == "Chat":
#         chat.chat()
#     elif selected == "Traslado":
#         Traslado.traslado()
#     elif selected == "Planificación":
#         Planificacion.planificar()
#     elif selected == "Asignacion":
#         asignacion.Asignacion()
def menu_camion():
    st.session_state.mostrar_contenedor_botones=False
    #st.markdown(bg_imagen,unsafe_allow_html=True)
    
    pag_Asignacion_camion=st.Page(
        page="views/Asignacion_pendiente_camion.py",
        title="Asignaciones",
        icon=":material/bar_chart:",
        default=True,
    )
        
    
    pg=st.navigation(pages=[pag_Asignacion_camion])

    pg.run()
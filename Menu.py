import streamlit as st
from streamlit_option_menu import option_menu

import base64


def get_img_as_base64(file):
    with open(file,"rb") as f:
        data=f.read()
    return base64.b64encode(data).decode()

#cimg=get_img_as_base64("logofer.png")
#img_principal=get_img_as_base64("qwe2.png")

# bg_imagen_sidebar=f"""
# <style>
# [data-testid="stSidebar"]>div:first-child{{
# background: rgb(44 73 144);
# background-image:url("data:logofer/png;base64,{img}");
# background-position:right bottom -650px ;
# background-size: auto;
# background-attachment: fixed; 
# }}
# </style>
#    """
# bg_imagen_principal=f"""
# <style>
# [data-testid="stAppViewContainer"]{{
# background-image:url("data:qwe2/png;base64,{img_principal}");
# background-position:center;
# background-repeat: no-repeat;
# background-size: cover;
# height: 100vh; 
# background-attachment: fixed; 


# }}
# [data-testid="stHeader"]{{
# background-color:rgba(0,0,0,0);
# }}
# </style>
#    """
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5
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
def menu():
    st.session_state.mostrar_contenedor_botones=False
    #st.markdown(bg_imagen_sidebar,unsafe_allow_html=True)
    #st.markdown(bg_imagen_principal,unsafe_allow_html=True)
    pag_Principal=st.Page(
        page="views/Principal.py",
        title="Dashboard",
        icon=":material/bar_chart:",
        default=True,
    )
    pag_Planificacion=st.Page(
        page="views/sistema_experto.py",
        title="Sistema",
        icon=":material/bar_chart:",
        
    )
   
    pag_reporte=st.Page(
        page="views/Reportes.py",
        title="Historial",
        icon=":material/bar_chart:",
    )
    pag_cosechadora=st.Page(
        page="views/gestion_insumos.py",
        title="Gestion Insumos",
        icon=":material/bar_chart:",
    )
    # pag_camion=st.Page(
    #     page="views/Camion.py",
    #     title="Camiones",
    #     icon=":material/bar_chart:",
    # )
    pag_ges_user=st.Page(
        page="views/gestion_usuarios.py",
        title="Usuarios",
        icon=":material/bar_chart:",
    )
    pg=st.navigation(pages=[pag_Principal,pag_Planificacion,pag_reporte,pag_cosechadora,pag_ges_user])

    pg.run()
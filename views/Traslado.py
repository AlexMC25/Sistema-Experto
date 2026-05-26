#se importa el framework streamlit
import streamlit as st
from views.dbTraslado import insertarTraslado
#se crea una lista que contiene los estados que puede tener el grano de arroz
estados_grano=["Verde","Maduro"]
def traslado():
    #se le da un titulo 
    st.title("Traslado 🚚")

    #se oculta las opciones de streamlit para tener una mejor visualizacion
    ocultar_elemento="""<style>
                        #MainMenu{visibility:hidden;}
                        #footer{visibility:hidden;}
                        #header{visibility:hidden;}
                        </style>"""
    st.markdown(ocultar_elemento,unsafe_allow_html=True)

    #se le da un encabezado
    st.header("Datos del Traslado")

    #se definen 2 columnas en la pagina, en las cuales se ubican los demas componentes
    izquierda,derecha=st.columns(2)
    contenedor_formulario = st.container()
    #se crea el formulario con streamlit
    formulario=st.form("datos_entrega",clear_on_submit=True,border=False)

    with contenedor_formulario:
    #estos campos van a la izquierda
        with formulario:
            
            with izquierda:
                fecha=st.date_input("Ingrese fecha de traslado")
                chofer=st.text_input("Ingrese nombre del chofer",value=None)
                matricula=st.text_input("Ingrese matricula del camión",value=None)
            with derecha:
                    #estos campos van al derecha
                n_cargas=st.number_input("Cargas en camion",value=None)
                destino=st.text_input("Destino")
                #este es el boton para enviar los datos del formulario
            enviar=st.form_submit_button("Enviar")
        # st.help(st.text_input)
            #se comprueba los datos enviados en el formulario
            if enviar:
                datos={'fecha':fecha,
                    'matricula':matricula,
                    'chofer':chofer,
                    'n_cargas':n_cargas,
                    'destino':destino
                        }
                insertarTraslado(datos)
                #st.write((fecha,matricula,humedad,estado_grano,peso_camion_vacio,peso_camion_lleno,tasa,nombre_piladora,direccion))
                st.success("Datos enviados!")
                
            
            

#se importa el framework streamlit
import streamlit as st
from views.dbEntrega import insertarentrega
#se crea una lista que contiene los estados que puede tener el grano de arroz
estados_grano=["Verde","Maduro"]
def entrega():
    #se le da un titulo 
    st.title("Entrega 📦")

    #se oculta las opciones de streamlit para tener una mejor visualizacion
    ocultar_elemento="""<style>
                        #MainMenu{visibility:hidden;}
                        #footer{visibility:hidden;}
                        #header{visibility:hidden;}
                        </style>"""
    st.markdown(ocultar_elemento,unsafe_allow_html=True)

    #se le da un encabezado
    st.header("Datos de la entrega")

    #se definen 2 columnas en la pagina, en las cuales se ubican los demas componentes
    izquierda,derecha=st.columns(2)
    contenedor_formulario = st.container()
    #se crea el formulario con streamlit
    formulario=st.form("datos_entrega",clear_on_submit=True,border=False)

    with contenedor_formulario:
    #estos campos van a la izquierda
        with formulario:
            
            with izquierda:
                fecha=st.date_input("Ingrese fecha de entrega")
                matricula=st.text_input("Ingrese matricula del camión",value=None)
                humedad=st.number_input("Ingrese humedad del grano",value=None)
                estado_grano=st.selectbox("Estado del grano",estados_grano)
                peso_camion_vacio=st.number_input("Peso vacio del camión",value=None)
            with derecha:
                    #estos campos van al derecha
                peso_camion_lleno=st.number_input("Peso lleno del camión",value=None)
                tasa=st.selectbox("Tasa",(210,215,220))
                nombre_piladora=st.text_input("Nombre de la piladora")
                direccion=st.text_input("Dirección")
                #este es el boton para enviar los datos del formulario
            enviar=st.form_submit_button("Enviar")
        # st.help(st.text_input)
            #se comprueba los datos enviados en el formulario
            if enviar:
                datos={'fecha':fecha,
                    'matricula':matricula,
                    'humedad':humedad,
                    'estado_grano':estado_grano,
                    'peso_camion_vacio':peso_camion_vacio,
                    'peso_camion_lleno':peso_camion_lleno,
                    'tasa':tasa,
                    'nombre_piladora':nombre_piladora,
                    'direccion':direccion
                        }
                insertarentrega(datos)
                #st.write((fecha,matricula,humedad,estado_grano,peso_camion_vacio,peso_camion_lleno,tasa,nombre_piladora,direccion))
                st.success("Datos enviados!")
                
            
            



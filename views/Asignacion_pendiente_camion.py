#se importa el framework streamlit
import streamlit as st

import pandas as pd
from datetime import datetime,time


from views.dbCamion import consultar_chofer
from views.dbAsignacion import coleccion,actualizar_asignacion,cambio_disp_disponible
@st.cache_data(ttl=15)
def cargar_datos():
    
    cursor=coleccion.find({'camion':consultar_chofer(st.session_state["name"])})
    df=pd.DataFrame(list(cursor))
    return df

df=cargar_datos()
contenedor_formulario = st.empty()
derecha = st.empty()
izquierda=st.empty()

centro1=st.empty()
centro2=st.empty()
izquierda1=st.empty()
derecha1=st.empty()
izquierda2=st.empty()
derecha2=st.empty()
btactualizar=st.empty()
bteliminar=st.empty()
contenedor_bt=st.empty()
contenedor_fr_actualizar=st.empty()
contenedor_fr_eliminar=st.empty()
# Inicializar una variable de estado para controlar la visibilidad del widget
if 'cosechadoras' not in st.session_state:
    st.session_state.cosechadoras = []
# Inicializar una variable de estado para controlar la visibilidad del widget
if 'btn_actualizar' not in st.session_state:
    st.session_state.btn_actualizar = False
# Inicializar una variable de estado para controlar la visibilidad del widget
if 'btn_eliminar' not in st.session_state:
    st.session_state.btn_eliminar = False

# Inicializar una variable de estado para controlar la visibilidad del widget
st.session_state.mostrar_contenedor_actualizar = False
# Inicializar una variable de estado para controlar la visibilidad del widget
st.session_state.mostrar_contenedor_eliminar = False


# Función para alternar la visibilidad del widget

def mostrar_ocultar_actualizar():
    st.session_state.mostrar_contenedor_actualizar = not st.session_state.mostrar_contenedor_actualizar
def mostrar_ocultar_eliminar():
    st.session_state.mostrar_contenedor_eliminar = not st.session_state.mostrar_contenedor_eliminar


def completar_asignacion():
    
    #formulario=st.form("actualizacion",clear_on_submit=True,border=False)
    izquierda,derecha=st.columns(2,gap="small")
    with st.container():
        c1,c2,c3=st.columns([1,1,1])
        with c1:
            with st.container():
                selected_id = st.selectbox("Seleccione ID de la asignación completada", df['_id'])
                peso_saca = st.selectbox("Peso de Saca", (200,205,210,215,220))
                precio_saca=st.number_input("Precio del Quintal de Arroz")
                # Obtener la fila seleccionada
                selected_row = df[df['_id'] == selected_id]
                # Mostrar campos de entrada para editar los valores
                if not selected_row.empty:
                
                    conductor = st.session_state["name"]
                    carga=selected_row['carga'].values[0]

                    fecha=selected_row['fecha_hora'].values[0]
                    id_camion=selected_row['camion'].values[0]
                    planificacion_id=selected_row['planificacion_id'].values[0]
                    estado =selected_row['estado']

                    
            c1_1,c1_2=st.columns([1,1])
            with c1_1:
                enviar=st.button('Terminar')
    if enviar:
        datos={ "_id":selected_id,
                   "conductor":conductor,
                   "peso_saca":peso_saca,
                   "precio_saca":precio_saca
                   
                   }
        cambio_disp_disponible(id_camion)
        actualizar_asignacion(datos)
        #st.toast('Registro actualizado!')


#eliminar registro

if "actualizar_eliminar" not in st.session_state:
    st.session_state.actualizar_eliminar=False
def Asignacion_Camion():
    
    #se le da un titulo 
    st.title("Asignaciones Pendientes 🚚")
    #st.write(st.session_state.cantidad_entregar)
    #se oculta las opciones de streamlit para tener una mejor visualizacion
    # ocultar_elemento="""<style>
    #                     #MainMenu{visibility:hidden;}
    #                     #footer{visibility:hidden;}
    #                     #header{visibility:hidden;}
    #                     </style>"""
    # st.markdown(ocultar_elemento,unsafe_allow_html=True)

    #se le da un encabezado
    st.header(f'Asignaciones para *{st.session_state["name"]}*')
    with st.container():
        col1,col2,col3=st.columns([1,10,1])
        with col2:
            st.write(df)
            
           
    contenedor_bt=st.container()
   
    with contenedor_bt:
        opciones=st.button('Opciones')
        
        if opciones or st.session_state.actualizar_eliminar:
            st.session_state.actualizar_eliminar=True
            opt=st.radio('Completar asignación:',['Completar'])
            if opt:
                completar_asignacion()
            
        

Asignacion_Camion()
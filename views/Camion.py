#se importa el framework streamlit
import streamlit as st

import pandas as pd
from datetime import datetime,time

from views.dbPlanificacion import insertarPlanificacion
from views.dbCamion import coleccion,insertarCamion,actualizarCamion,eliminarCamion
@st.cache_data(ttl=15)
def cargar_datos():
    cursor=coleccion.find()
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

def nuevo_camion():
    #formulario=st.form("actualizacion",clear_on_submit=True,border=False)
    izquierda,derecha=st.columns(2,gap="small")
    with st.container():
        c1,c2=st.columns([1,1])
        with c1:
            with st.container():
                nuevo_id=df['_id'].max()
                
                conductor = st.text_input("Conductor")
                placa = st.text_input("Placa de Camión")
                capacidad_max=st.number_input("Capacidad maxima")
                
            c1_1,c1_2=st.columns([1,1])
        with c2:
            peso_vacio=st.number_input("Peso vacio del camion")

            estado =st.selectbox("Estado", ['disponible','En uso','Averia'])
                
            observacion=st.text_input("Observación")
                    
                
        enviar=st.button('Agregar',use_container_width=True)
    if enviar:
        datos={ #max(idEntrega)+
                   "conductor":conductor,
                   "placa":placa, 
                   "capacidad_max":int(capacidad_max),
                   "peso_vacio":int(peso_vacio),
                   "estado":estado, 
                   "observacion":observacion,
                   
                   }
        insertarCamion(datos)
        #st.toast('Cosechadora registrada!')

def actualizar_datos():
    
    #formulario=st.form("actualizacion",clear_on_submit=True,border=False)
    izquierda,derecha=st.columns(2,gap="small")
    with st.container():
        c1,c2=st.columns([1,1])
        with c1:
            with st.container():
                selected_id = st.selectbox("Selecciona un ID para editar", df['_id'])
                # Obtener la fila seleccionada
                selected_row = df[df['_id'] == selected_id]
                # Mostrar campos de entrada para editar los valores
                if not selected_row.empty:
                
                    conductor = st.text_input("Conductor", value=selected_row['conductor'].values[0])
                    placa = st.text_input("Placa de Camión", value=selected_row['placa'].values[0])
                    
                    
                   
            c1_1,c1_2=st.columns([1,1])
        with c2:
            if not selected_row.empty:
                    capacidad_max = st.number_input("Capacidad máxima del camión", value=(selected_row['capacidad_max'].values[0]))
                    peso_vacio=st.number_input("Peso vacio",value=(selected_row['peso_vacio'].values[0]))
                    estado =st.selectbox("Estado", ['disponible','En uso','Averia'])
                    if estado=='Averia':
                        observacion=st.text_input("Observación", value=selected_row['observacion'].values[0])
                    else:
                        observacion=""


        enviar=st.button('Actualizar',use_container_width=True)
    if enviar:
        datos={ "_id":selected_id,
                   "conductor":conductor,
                   "placa":str(placa),
                   "capacidad_max":capacidad_max,
                   "peso_vacio":peso_vacio,
                   "estado":estado, 
                   "observacion":observacion,
                   
                   
                   }
        actualizarCamion(datos)
        #st.toast('Registro actualizado!')


#eliminar registro
def m_eliminar():
    formulario=st.container()
    izquierda,derecha=st.columns(2)
    with formulario:
        c1,c2,c3=st.columns([1,1,1],gap="large")
        with c1:
            with st.container():
                selected_id = st.selectbox("Selecciona un ID para eliminar", df['_id'])
                
            c3_1,c3_2=st.columns([1,1])
            with c3_1:
                enviar=st.button('Eliminar')
        if enviar:
            datos={'_id':selected_id}
            eliminarCamion(datos)
            #st.toast('Registro eliminado!')

if "actualizar_eliminar" not in st.session_state:
    st.session_state.actualizar_eliminar=False
def Camion():
    
    #se le da un titulo 
    st.title("Camiones 🚚")
    #st.write(st.session_state.cantidad_entregar)
    #se oculta las opciones de streamlit para tener una mejor visualizacion
    # ocultar_elemento="""<style>
    #                     #MainMenu{visibility:hidden;}
    #                     #footer{visibility:hidden;}
    #                     #header{visibility:hidden;}
    #                     </style>"""
    # st.markdown(ocultar_elemento,unsafe_allow_html=True)

    #se le da un encabezado
    st.header("Datos de los camiones")
    with st.container():
        col1,col2,col3=st.columns([1,10,1])
        with col2:
            st.write()
    contenedor_bt=st.container()
    izquierda,centro1,centro2,derecha=st.columns([1,2,2,1])
    contenedor_fr_actualizar=st.container()
    contenedor_fr_eliminar=st.container()
    with contenedor_bt:
        if st.session_state.actualizar_eliminar:
            st.session_state.actualizar_eliminar=True
            opt=st.radio('Que desea hacer?:',['Agregar','Actualizar','Eliminar'],horizontal=True)
            if opt=='Actualizar':
                actualizar_datos()
            elif opt=='Agregar':
                nuevo_camion()
            else:
                m_eliminar()
        

Camion()
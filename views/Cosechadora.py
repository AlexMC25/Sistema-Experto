#se importa el framework streamlit
import streamlit as st
from views.dbAsignacion import insertarAsignacion
from views.dbCosechadora import coleccion
import pandas as pd
from datetime import datetime,time

from views.dbPlanificacion import insertarPlanificacion
from views.dbCosechadora import insertarCosechadora,actualizarCosechadora,eliminarCosechadora
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
def  regresar_planificacion():

    
    st.session_state.asignar = not st.session_state.asignar
    st.session_state.planificar = not st.session_state.planificar

def  ir_asignacion():
    datos={
        'fecha':(st.session_state.fecha),
        'cantidad_entregar':st.session_state.cantidad_entregar,
        'destino':st.session_state.destino,
        'estado':'pendiente',
    }
    insertarPlanificacion(datos)
    st.session_state.asignar = not st.session_state.asignar

def mostrar_ocultar_actualizar():
    st.session_state.mostrar_contenedor_actualizar = not st.session_state.mostrar_contenedor_actualizar
def mostrar_ocultar_eliminar():
    st.session_state.mostrar_contenedor_eliminar = not st.session_state.mostrar_contenedor_eliminar

def nueva_cosechadora():
    #formulario=st.form("actualizacion",clear_on_submit=True,border=False)
    izquierda,derecha=st.columns(2,gap="small")
    with st.container():
        c1,c2,c3=st.columns([1,1,1])
        with c1:
            with st.container():
                nuevo_id=df['_id'].max()
                # st.write(nuevo_id)
                conductor = st.text_input("Conductor")
                cap_tolva = st.number_input("Capacidad de tolva",format="%d",value=1000)
                # estado =st.selectbox("Estado", ['disponible','En uso','Averia'])
                # if estado=='Averia':
                #     observacion=st.text_input("Observación", value=selected_row['observacion'].values[0])
                    
            c1_1,c1_2=st.columns([1,1])
            with c1_1:
                enviar=st.button('Agregar')
    if enviar:
        datos={ #max(idEntrega)+
                   "conductor":conductor,
                   "capacidad_tolva":int(cap_tolva), 
                   }
        insertarCosechadora(datos)
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
                    
                    
            c1_1,c1_2=st.columns([1,1])
        with c2:
            if not selected_row.empty:
                cap_tolva = st.number_input("Capacidad de tolva", value=selected_row['capacidad_tolva'].values[0],format="%d")
                estado =st.selectbox("Estado", ['disponible','En uso','Averia'])
                if estado=='Averia':
                    observacion=st.text_input("Observación", value=selected_row['observacion'].values[0])
                else:
                    observacion=None
        enviar=st.button('Actualizar',use_container_width=True)
    if enviar:
        datos={ "_id":selected_id,
                   "conductor":conductor,
                   "capacidad_tolva":int(cap_tolva), 
                   "estado":estado,
                   "observacion":observacion
                   }
        actualizarCosechadora(datos)
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
            eliminarCosechadora(datos)
            #st.toast('Registro eliminado!')

if "actualizar_eliminar" not in st.session_state:
    st.session_state.actualizar_eliminar=False
def Cosechadora():
    
    #se le da un titulo 
    st.title("Cosechadoras 🚜")
    #st.write(st.session_state.cantidad_entregar)
    #se oculta las opciones de streamlit para tener una mejor visualizacion
    # ocultar_elemento="""<style>
    #                     #MainMenu{visibility:hidden;}
    #                     #footer{visibility:hidden;}
    #                     #header{visibility:hidden;}
    #                     </style>"""
    # st.markdown(ocultar_elemento,unsafe_allow_html=True)

    #se le da un encabezado
    st.header("Datos de las cosechadoras")
    with st.container():
        col1,col2,col3=st.columns([1,6,1])
        with col2:
            #st.write(df)
            st.write()
    contenedor_bt=st.container()
    izquierda,centro1,centro2,derecha=st.columns([1,2,2,1])
    contenedor_fr_actualizar=st.container()
    contenedor_fr_eliminar=st.container()
    with contenedor_bt:
        # opciones=st.button('Opciones')
        st.session_state.actualizar_eliminar=True
        if st.session_state.actualizar_eliminar:
            
            opt=st.radio('Que desea hacer?:',['Agregar','Actualizar','Eliminar'],horizontal=True)
            if opt=='Actualizar':
                actualizar_datos()
            elif opt=='Agregar':
                nueva_cosechadora()
            else:
                m_eliminar()
        

Cosechadora()
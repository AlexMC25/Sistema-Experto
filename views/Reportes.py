#se importa el framework streamlit y pandas
import streamlit as st
import pandas as pd
from views.dbPlanificacion import coleccion as coleccion_planificacion
from views.dbAsignacion import coleccion as coleccion_asignaciones
from views.dbCamion import coleccion as coleccion_camion
from views.dbCosechadora import coleccion as coleccion_cosechadora

#convertir a dataframe los dato de la coleccion
# @st.cache_data
def carga_planificaciones():
    cursor=coleccion_planificacion.find()
    df=pd.DataFrame(list(cursor))
    df=df[["_id","fecha","propietario","cultivo_tipo","etapa","deficiencias","recomendacion"]]
    
    df=df.rename(columns={"_id":"ID",
                       "fecha":"Fecha",
                       "propietario":"Propietario del Cultivo",
                       "cultivo_tipo":"Cultivo",
                       "etapa":"Etapa del cultivo",
                       "deficiencias":"Deficiencias detectadas",
                       "recomendacion":"Recomendaciones",

                       
                       })
    return df

df_planificaciones=carga_planificaciones()

def carga_asignaciones():
    cursor=coleccion_asignaciones.find()
    df=pd.DataFrame(list(cursor))
    return df
df_aasignaciones=carga_asignaciones()

def carga_camiones():
    cursor=coleccion_camion.find()
    df=pd.DataFrame(list(cursor))
    return df
df_camiones=carga_camiones()

def carga_cosechadoras():
    cursor=coleccion_cosechadora.find()
    df=pd.DataFrame(list(cursor))
    return df
df_cosechadoras=carga_cosechadoras()

formulario=st.empty()
izquierda=st.empty()
derecha=st.empty()
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
if 'btn_actualizar' not in st.session_state:
    st.session_state.btn_actualizar = False
# Inicializar una variable de estado para controlar la visibilidad del widget
if 'btn_eliminar' not in st.session_state:
    st.session_state.btn_eliminar = False

# Inicializar una variable de estado para controlar la visibilidad del widget
st.session_state.mostrar_contenedor_actualizar = False
# Inicializar una variable de estado para controlar la visibilidad del widget
st.session_state.mostrar_contenedor_eliminar = False


# def  mostrar_actualizar():
#     st.session_state.btn_actualizar = not st.session_state.btn_actualizar
#     st.session_state.btn_nuevo_usuario_des = not st.session_state.btn_nuevo_usuario_des
# def datos_actualizar():

    #Seleccionar un registro para editar
    
        # Actualizar el DataFrame con los nuevos valores
        # if st.button("Enviar"):
        #     df.loc[df['_id'] == selected_id, 'humedad'] = humedad
        #     df.loc[df['_id'] == selected_id, 'calidad_grano'] = calidad_grano
        #     df.loc[df['_id'] == selected_id, 'matricula'] = matricula
        #     df.loc[df['_id'] == selected_id, 'peso_camion_vacio'] = peso_camion_vacio
        #     df.loc[df['_id'] == selected_id, 'peso_camion_lleno'] = peso_camion_lleno
        #     df.loc[df['_id'] == selected_id, 'nombre_piladora'] = nombre_piladora
        #     df.loc[df['_id'] == selected_id, 'direccion'] = direccion
        #     df.loc[df['_id'] == selected_id, 'tasa'] = tasa
        #     df.loc[df['_id'] == selected_id, 'fechaHora'] = fechaHora
        #     st.success('Registro actualizado!')

#funciones para mostrar/ocultar forumlarios
def mostrar_ocultar_actualizar():
    st.session_state.mostrar_contenedor_actualizar = not st.session_state.mostrar_contenedor_actualizar
def mostrar_ocultar_eliminar():
    st.session_state.mostrar_contenedor_eliminar = not st.session_state.mostrar_contenedor_eliminar


# #actualizar registro
# def actualizar_datos():
    
#     formulario=st.form("actualizacion",clear_on_submit=True,border=False)
#     izquierda,derecha=st.columns(2,gap="small")
#     with formulario:
#         c1,c2,c3=st.columns([1,1,1])
#         with c1:
#             with st.container():
#                 selected_id = st.selectbox("Selecciona un ID para editar", df['_id'])
#                 # Obtener la fila seleccionada
#                 selected_row = df[df['_id'] == selected_id]
#                 # Mostrar campos de entrada para editar los valores
#                 if not selected_row.empty:
#                     humedad = st.number_input("Humedad", value=int(selected_row['humedad'].values[0]))
#                     calidad_grano = st.text_input("Calidad del grano", value=selected_row['calidad_grano'].values[0])
#                     matricula = st.text_input("Matricula", value=selected_row['matricula'].values[0])
#                     peso_camion_vacio = st.number_input("Peso del camión vacio", value=int(selected_row['peso_camion_vacio'].values[0]))
#             # Mostrar campos de entrada para editar los valores
#                     peso_camion_lleno = st.number_input("Peso del camión lleno", value=int(selected_row['peso_camion_lleno'].values[0]))
#                     nombre_piladora = st.text_input("Nombre de Piladora", value=selected_row['nombre_piladora'].values[0])
#                     direccion = st.text_input("Dirección", value=selected_row['direccion'].values[0])
#                     tasa = st.number_input("Tasa", value=int(selected_row['tasa'].values[0]))
#                     fechaHora=st.date_input("Ingrese fecha de entrega")
#             c1_1,c1_2=st.columns([1,1])
#             with c1_1:
#                 enviar=st.form_submit_button("Enviar")
#     if enviar:
#         st.success('Registro actualizado!')


# #eliminar registro
# def m_eliminar():
#     formulario=st.form("eliminacion",clear_on_submit=True,border=False)
#     izquierda,derecha=st.columns(2)
#     with formulario:
#         c1,c2,c3=st.columns([1,1,1],gap="large")
#         with c3:
#             with st.container():
#                 selected_id = st.selectbox("Selecciona un ID para eliminar", df['_id'])
#                 # Obtener la fila seleccionada
#                 selected_row = df[df['_id'] == selected_id]
#                 # Mostrar campos de entrada para editar los valores
#                 if not selected_row.empty:
#                     humedad = st.number_input("Humedad", value=int(selected_row['humedad'].values[0]))
#             c3_1,c3_2=st.columns([1,1])
#             with c3_2:
#                 enviar=st.form_submit_button("Eliminar")
#         if enviar:
#             st.success('Registro eliminado!')


def reportes():
    
    #se le da un titulo 
    st.title("Historial 📑")
    
    # with contenedor:
    #     st.dataframe(df,hide_index=True)
   # Mostrar el DataFrame
    
    #opciones=st.button('Opciones')
        
    # if opciones or st.session_state.actualizar_eliminar:
    #     st.session_state.actualizar_eliminar=True
    opt=st.radio('',['Analisis previo','Sin analisis'],horizontal=True)
    if opt=='Analisis previo':
        st.subheader("Recomendaciones")
        st.write(df_planificaciones)
    elif opt=='Sin analisis':
        st.subheader("Recomendaciones")
        st.write(df_aasignaciones)
    # elif opt=='Camiones':
    #     st.subheader("Tabla de Camiones 🚚")
    #     st.write(df_camiones)
    # elif opt=='Cosechadoras':
    #     st.subheader("Tabla de Cosechadoras 🚜")
    #     st.write(df_cosechadoras)

    contenedor_bt=st.container()
    izquierda,centro1,centro2,derecha=st.columns([1,2,2,1])
    contenedor_fr_actualizar=st.container()
    contenedor_fr_eliminar=st.container()
    # with contenedor_bt:

        
            
        # with izquierda:
        #     btactualizar=st.button("Actualizar",on_click=mostrar_ocultar_actualizar,use_container_width=True)
        #     if st.session_state.mostrar_contenedor_actualizar:
        #         with contenedor_fr_actualizar:
        #             st.session_state.mostrar_contenedor_eliminar=False
        #             actualizar_datos()
        # with derecha:
        #     bteliminar=st.button("Eliminar",on_click=mostrar_ocultar_eliminar,use_container_width=True)
        #     if st.session_state.mostrar_contenedor_eliminar:
        #         with contenedor_fr_actualizar:
        #             st.session_state.mostrar_contenedor_actualizar=False
        #             m_eliminar()

    # if st.session_state.btn_actualizar:
    #     m_actualizar()
    #     st.session_state.mostrar_contenedor_eliminar=False
    
    # if st.session_state.btn_eliminar:
    #     m_eliminar()
    #     st.session_state.mostrar_contenedor_actualizar=False
    
            # if st.session_state.btn_eliminar:
            #         datos_actualizar()
# with contenedor_actualizar:
#     
    
reportes()
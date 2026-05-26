#se importa el framework streamlit
import streamlit as st
from views.dbAsignacion import insertarAsignacion,cambio_disp_en_uso
from views.dbCamion import disponibilidadCamion,capacidad_max_Camion
from views.dbCosechadora import disponibilidadCosechadora
from datetime import datetime,time

from views.dbPlanificacion import insertarPlanificacion,eliminar_ultima_planificacion

contenedor_formulario = st.empty()
derecha = st.empty()
izquierda=st.empty()
# Inicializar una variable de estado para controlar la visibilidad del widget
if 'cantidad_entregar' not in st.session_state:
    st.session_state.cantidad_entregar = 0
if 'destino' not in st.session_state:
    st.session_state.destino = ''
if 'fecha' not in st.session_state:
    st.session_state.fecha = 0
if 'planificar' not in st.session_state:
    st.session_state.planificar = False
# Inicializar una variable de estado para controlar la visibilidad del widget
if 'asignar' not in st.session_state:
    st.session_state.asignar = False
if 'btn_planificar' not in st.session_state:
    st.session_state.btn_planificar = False
if 'btn_regresar' not in st.session_state:
    st.session_state.btn_regresar = False
# Inicializar el estado de la sesión para controlar la visibilidad del contenedor
if 'mostrar_contenedor' not in st.session_state:
    st.session_state.mostrar_contenedor = False
if 'planificaciones' not in st.session_state:
    st.session_state.planificaciones ={'001':{'fecha':datetime(2022,1,1),
                                              'cantidad_entregar':3000,
                                              'destino':'Piladora Lorena',
                                              'estado':'pendiente'},
                                        '002':{'fecha':datetime(2022,4,9),
                                              'cantidad_entregar':3000,
                                              'destino':'Piladora Lorena',
                                              'estado':'completado'}
}

if 'asignaciones' not in st.session_state:
    st.session_state.asignaciones ={'010':{'camion':'001',
                                           'carga':1500,
                                           'hora_salida':time(),
                                           'planificacion_id':'222'
        
    }
}

if 'camiones_disponibles' not in st.session_state:
    st.session_state.camiones_disponibles ={}


# Función para alternar la visibilidad del widget
def  regresar_planificacion():
    if st.session_state.cantidad_entregar!=0:
        eliminar_ultima_planificacion(st.session_state.id_planificacion)

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


# def comprobar_cantidad_entregar(cantidad):
#     if cantidad<=0:
#         regresar_planificacion()
#         return True
#     else: 
#         return False


def planificar():
    
    st.session_state.cantidad_entregar=0
    
    #st.write(st.session_state.asignaciones)
    #se le da un titulo 
    # st.write(st.session_state.pagina)
    #se oculta las opciones de streamlit para tener una mejor visualizacion
    # ocultar_elemento="""<style>
    #                     #MainMenu{visibility:hidden;}
    #                     #footer{visibility:hidden;}
    #                     #header{visibility:hidden;}
    #                     </style>"""
    # st.markdown(ocultar_elemento,unsafe_allow_html=True)

    #se le da un encabezado
   
    
    #se definen 2 columnas en la pagina, en las cuales se ubican los demas componentes
    izquierda,derecha=st.columns(2)
    
    #se crea el formulario con streamlit
    #formulario=st.form("datos_planificacion",clear_on_submit=True,border=False)

    with contenedor_formulario.container():
        st.title("Planificación")
        st.header("Ingrese los siguientes datos para proceder con la planificación")
    #estos campos van a la izquierda
        # with izquierda:
        st.write('---')
        fecha=st.date_input("Fecha")
        st.session_state.fecha=fecha
        cantidad_entregar=st.number_input("Cantidad que desea entregar(kg)",format="%d",value=1000)
        st.session_state.cantidad_entregar=cantidad_entregar
            # vehiculo=st.selectbox("Vehiculo",(int('001'),int('002'),int('003')))
        # with derecha:
            # inicio=st.text_input("Partida",value=None)
        destino=st.text_input("Destino",value=None)
        st.session_state.destino=destino
            #este es el boton para enviar los datos del formulario
        st.write('---')
    # st.help(st.text_input)
        #se comprueba los datos enviados en el formulario
    
    with st.container():
        if (len(disponibilidadCosechadora()) and len(disponibilidadCamion()))==0:
            st.session_state.btn_planificar=True
        else:
            st.session_state.btn_planificar=False
        enviar=st.button("Planificar",use_container_width=True,on_click=ir_asignacion,disabled=st.session_state.btn_planificar,help='Si esta desactivado, es porque no hay camiones ni cosechadoras disponibles')
            
            # datos={'fecha':fecha,
            #     'matricula':matricula,
            #     'humedad':humedad,
            #     'estado_grano':estado_grano,
            #     'peso_camion_vacio':peso_camion_vacio,
            #     'peso_camion_lleno':peso_camion_lleno,
            #     'tasa':tasa,
            #     'nombre_piladora':nombre_piladora,
            #     'direccion':direccion
            #         }
            # insertarentrega(datos)


def Asignacion():
   
    
    #se le da un titulo 
    st.title("Asignación de Transporte 🚚")
    #st.write(st.session_state.cantidad_entregar)
    #se oculta las opciones de streamlit para tener una mejor visualizacion
    # ocultar_elemento="""<style>
    #                     #MainMenu{visibility:hidden;}
    #                     #footer{visibility:hidden;}
    #                     #header{visibility:hidden;}
    #                     </style>"""
    # st.markdown(ocultar_elemento,unsafe_allow_html=True)

    #se le da un encabezado
    st.header("Asigne camiones para transportar la carga planificada")
    st.header(f'Cantidad planificada a entregar : {st.session_state.cantidad_entregar}')
    #se definen 2 columnas en la pagina, en las cuales se ubican los demas componentes
    izquierda,derecha=st.columns(2)
    contenedor_formulario.empty()
    
    with contenedor_formulario.container():
    #estos campos van a la izquierda
    
        with izquierda:
  
            
            
                    #st.toast(f'{dis['disponibilidad']} ❌')
            if len(st.session_state.camiones_disponibles)==0:
                estado=True
                st.toast('Todos los camiones ocupados ❌')
            else:
                estado=False
            camionD=[]
            for camion in st.session_state.camiones_disponibles.items():
                camionD.append(camion[0])
            
            # for dis in range(len(st.session_state.camiones_disponibles)):
            #     camionD.append(st.session_state.camiones_disponibles['_id'])
            vehiculo=st.selectbox("Vehiculo ID",(camionD),disabled=estado)
           
        with derecha:
                #estos campos van al derecha
            if len(st.session_state.camiones_disponibles)==0:
                regresar_planificacion()
            else:
                if st.session_state.cantidad_entregar<=capacidad_max_Camion(vehiculo):
                    carga=st.number_input("Carga a transportar",value=st.session_state.cantidad_entregar,min_value=0,max_value=capacidad_max_Camion(int(vehiculo)),disabled=estado)
                else:
                    carga=st.number_input("Carga a transportar",value=capacidad_max_Camion(vehiculo),min_value=0,max_value=capacidad_max_Camion(int(vehiculo)),disabled=estado)
                    st.toast('Cantidad excede a lo planificado')

                    
                salida=st.time_input("Hora salida",time())
            if st.session_state.cantidad_entregar<=0:
                regresar_planificacion()
            #este es el boton para enviar los datos del formulario
        

    with st.container():
        col1,col2=st.columns(2)
        with col1:
            regresar=st.button("Regresar",use_container_width=True,on_click=regresar_planificacion)
        with col2:
            enviar=st.button("Asignar",use_container_width=True)
    # st.help(st.text_input)
        #se comprueba los datos enviados en el formulario
        
        if enviar:

            cambio_disp_en_uso(vehiculo)
            st.session_state.cantidad_entregar-=carga
            if st.session_state.cantidad_entregar<=0:
                regresar_planificacion()
            else:
                datos={
                        'camion':int(vehiculo),
                        'carga':carga,
                        'fecha_hora':(st.session_state.fecha,salida),
                        'planificacion_id':st.session_state.id_planificacion,
                        'estado':'pendiente'
                        }
                insertarAsignacion(datos)
            
            with st.container():
                
                st.toast("Asignacion registrada")
               

                # cambio_disp_en_uso(vehiculo)
                # st.write(st.session_state.camiones)
        
    
# Condicional para mostrar u ocultar el widget
if st.session_state.asignar:
    Asignacion()
    
else:
    planificar()

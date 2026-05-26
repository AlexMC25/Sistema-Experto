#se importa el framework streamlit
import streamlit as st
import datetime
from views.dbTraslado import insertarTraslado

#se crea una lista que contiene los estados que puede tener el grano de arroz
vehiculos={'001':{'carga_maxima':9000,
                  'peso_vacio':1200,
                  'placa':'grg1233'},
            '002':{'carga_maxima':8500,
            'peso_vacio':1400,
            'placa':'rrr4423'}}
def Asignacion():
    from views.Planificacion import planificar
    st.session_state.pagina='Asignacion'
    #se le da un titulo 
    st.title("Asignación de Transporte 🚚")
    #st.write(st.session_state.cantidad_entregar)
    #se oculta las opciones de streamlit para tener una mejor visualizacion
    ocultar_elemento="""<style>
                        #MainMenu{visibility:hidden;}
                        #footer{visibility:hidden;}
                        #header{visibility:hidden;}
                        </style>"""
    st.markdown(ocultar_elemento,unsafe_allow_html=True)

    #se le da un encabezado
    st.header("Datos")

    #se definen 2 columnas en la pagina, en las cuales se ubican los demas componentes
    izquierda,derecha=st.columns(2)
    contenedor_formulario = st.empty()
    #se crea el formulario con streamlit
    formulario2=st.form("datos_asignacion",clear_on_submit=True,border=False)

    with contenedor_formulario.container():
    #estos campos van a la izquierda
    
        with izquierda:
            vehiculo=st.selectbox("Vehiculo ID",(vehiculos))
        with derecha:
                #estos campos van al derecha
            carga=st.number_input("Carga en camion",value=vehiculos[vehiculo]['carga_maxima'],min_value=1000,max_value=vehiculos[vehiculo]['carga_maxima'])
            destino=st.time_input("Hora salida",datetime.time())
            #este es el boton para enviar los datos del formulario
        enviar=st.button("Asignar",use_container_width=True)
    # st.help(st.text_input)
        #se comprueba los datos enviados en el formulario
        if enviar:
            # datos={'fecha':fecha,
            #     'matricula':matricula,
            #     'chofer':chofer,
            #     'n_cargas':n_cargas,
            #     'destino':destino
            #         }
            # insertarTraslado(datos)
            #st.write((fecha,matricula,humedad,estado_grano,peso_camion_vacio,peso_camion_lleno,tasa,nombre_piladora,direccion))
            with st.container():
                st.success("Datos enviados!")
                
    if st.session_state.pagina == 'planificar':
        planificar()  

if st.session_state.pagina=='Asignacion':
    Asignacion()
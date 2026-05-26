import streamlit as st
from streamlit_option_menu import option_menu
import importlib
import os
from Menu import menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from views.dbPlanificacion import coleccion as coleccion_planifi,cliente_mas_frecuente,consultar_ciudad_asignaciones,contar_recomendaciones
from views.dbAsignacion import promedio,obtener_carga_por_mes,contar_recomendaciones_sin,maleza_mas_frecuente
from views.dbCamion import camiones_disponibles,camiones_en_uso
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 > div > div > div > div:nth-child(6) > div:nth-child(1) > div > div > div > div

def principal():
 
    # Título del dashboard
   
    
    # Crear un DataFrame de ejemplo
    data = {
        #'Fecha': pd.date_range(start='2024-01-01', periods=5, freq='D'),
        'Destino': [ciudad for ciudad,valor in consultar_ciudad_asignaciones().items()],
        
        'Transportado': [valor for ciudad,valor in consultar_ciudad_asignaciones().items()]
    }
    
    data1 = {
        
        'Cantidad Entregada': [valor for camion,valor in obtener_carga_por_mes().items()],
        'Camión': [camion for camion,valor in obtener_carga_por_mes().items()]
    }
    df = pd.DataFrame(data)

    # Calcular KPIs
    frecuentes = cliente_mas_frecuente()
    total_transportado = df['Transportado'].sum()
    
    
    # Mostrar KPIs
    #st.subheader('Indicadores Clave de Rendimiento (KPI)')

    col1, col2,col3= st.columns(3)
    
    
    with col1:
        with st.container(border=True):
            
            st.metric(label=":green[Total de recomendaciones]", value=f"{contar_recomendaciones()+contar_recomendaciones_sin()}")

        with st.container(border=True):
            st.metric(label=":green[Deficiencias clave]",value="pH N P K")
        
        with st.container(border=True):
            st.metric(label=":green[Cliente Frecuente]",value=frecuentes)
            
            # sum=0
            # for camion,valor in obtener_carga_por_mes().items():
            #     sum=sum+valor
            # st.metric(label="Total Distribuido Mes 📆", value=f"{sum} kg")
    
    with col2:
        with st.container(border=True):
            st.metric(label=":green[Maleza mas común]", value=maleza_mas_frecuente())
        with st.container(border=True):
            nombre_maleza_comun = maleza_mas_frecuente()
            if nombre_maleza_comun:
                nombre_imagen_maleza = nombre_maleza_comun.replace(" ", "_") + ".jpg"
                ruta_imagen_maleza = os.path.join(".\\", nombre_imagen_maleza)
                
            st.image(ruta_imagen_maleza, caption=nombre_maleza_comun)
    with col3:
        with st.container(border=True):
            st.metric(label=":green[Producto mas sugerido]", value=f"Urea 46%")

        with st.container(border=True):
            st.image("./productos/fertilizantes/productos_simples/Urea_46.jpg")
    # with col3:
    #     with st.container(border=True):
    #         obtener_carga_por_mes() 
            
    #         for camion,valor in obtener_carga_por_mes().items():
    #             st.metric(label=f"Carga X Mes Camión: {camion}", value=f"{valor} ")
    
    
    # Crear el gráfico de líneas
    fig_line1= go.Figure()
    # fig_line2= go.Figure()
    # Crear el gráfico de barras
    # with st.container():
    #     col1=st.columns(1)
    #     with col1:
    #         with st.container(border=True):
    #             fig_line1 = px.bar(data, x='Destino', y='Transportado', title='Asignaciones Ciudad 🏙️',orientation="h")
    #             st.plotly_chart(fig_line1)
    #     with col2:
    #         with st.container(border=True):
    #             fig_line2 = px.bar(data1, x='Camión', y='Cantidad Entregada', title='Entregas por Camión 🚚')
    #     # Mostrar el gráfico en la aplicación
    #             st.plotly_chart(fig_line2)


principal()
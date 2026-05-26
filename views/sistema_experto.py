
# Importar Streamlit
import mysql.connector
import streamlit as st
from experta import Fact, Rule, KnowledgeEngine, Field, P ,MATCH,watch
import pandas as pd
import glob
## Macronutrientes según tipo de suelo y edad (ppm)

import mysql.connector
import google.generativeai as genai

#clave para conectarse con gemini
genai.configure(api_key="AIzaSyA2Q6W-c3MGxACZKk_XOi-5oSlxKs6CRSg")
model = genai.GenerativeModel('gemini-1.5-flash')


def plan_fertilizacion(prompt):
# Genera la respuesta usando el modelo y el contexto del negocio
    try:
        business_context = (
            "Eres un sistema experto en generar planes de fertilización. "
            "Utiliza los productos disponibles, las dosis recomendadas y las deficiencias detectadas "
            "para proporcionar un plan de fertilización detallado."
            
            

        )
        full_prompt = f"{business_context}\nUsuario: {prompt}\nAsistente:"
        response = model.generate_content(full_prompt)
        assistant_response = response.text  # Asegúrate de que `.text` es el atributo correcto
    except Exception as e:
        assistant_response = "Lo siento, ocurrió un error al procesar tu solicitud."
        st.error(f"Error: {e}")

    st.write("### Plan de Fertilización Generado:")
    st.write(assistant_response)

malezas_suelo=[]
hongos_suelo=[]
nutri={}
# Definir hechos relacionados con los cultivos y el suelo
class Cultivo(Fact):
    """Representa un cultivo específico"""
    tipo = Field(str, mandatory=True)  # Ejemplo: "maíz", "mango", "cacao"
    etapa = Field(str)  # Ejemplo: "germinación", "floración", "maduración"
    rendimientoEsperado=Field(float)

class Suelo(Fact):
    """Representa las características del suelo"""
    ph = Field(float)  # Ejemplo: pH del suelo
    textura = Field(str)  # Ejemplo: "arenoso", "arcilloso", "limoso"
    
class Planta(Fact):
    """Representa las características del planta"""
    hojas = Field(str)  
    raices = Field(str) 
    tallo=Field(str)
    frutos=Field(str)

class Nutrientes(Fact):
    elementos = Field(dict)

class Malezas(Fact):
    malezas = Field(list)

class Hongos(Fact):
    hongos = Field(list)

class Recomendacion(Fact):
    """Fact para almacenar la recomendación de fertilizante"""
    fertilizante = Field(str, mandatory=True)
    dosis = Field(str, mandatory=True)  # Dosis recomendada (por ejemplo, kg/ha)
    nutriente=Field(str)

# Motor de reglas para la recomendación de fertilizantes
class SistemaRecomendacionFertilizantesConAnalisis(KnowledgeEngine):
    
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_nitrogeno(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1.2857
        profundidad=30
        densidad=1
        nitrogeno=elementos["nitrogeno_suelo"]
        
        suministro_suelo=(((nitrogeno*factor_oxidada)*profundidad)*densidad)*0.1
        demanda_cultivo=12
        # demanda_cultivo=(extra*rendimientoEsperado)+aerea
        eficiencia_recuperacion=1.5
        dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        # dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if nitrogeno>50.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Nitrogeno")
            calculo=round(((dosis_fert)*10)/34)
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="Nitrato de Amonio", dosis=f"{calculo} kg/ha"))
        if nitrogeno<20.0:
            calculo=round(((dosis_fert)*100)/46)
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculo} kg/ha"))
        if (20.0<= nitrogeno <=50.0):
            st.success("El nitrogeno se encuentra dentro de los rangos recomendados")
        
        
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_fosforo(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=2.2914
        profundidad=30
        densidad=1
        fosforo=elementos["fosforo_suelo"]
        suministro_suelo=(((fosforo*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(3.25*rendimientoEsperado)+2.6
        eficiencia_recuperacion=2
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        
        if fosforo>30.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Fosforo")
            calculo=round(((dosis_fert)*10)/46)
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="Super Fosfato Triple", dosis=f"{calculo} kg/ha"))
        if fosforo<15.0:
            calculo=round(((dosis_fert)*100)/46)
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculo} kg/ha"))
        if (15.0<= fosforo <=30.0):
            st.success("El Fosforo se encuentra dentro de los rangos recomendados")
            
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_potasio(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1.2046
        profundidad=30
        densidad=1
        potasio=elementos["potasio_suelo"]
        suministro_suelo=(((potasio*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(17.5*rendimientoEsperado)+15.5
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if potasio>300.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Fosforo")
            calculo=round(((dosis_fert)*10)/46)
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Nitrato de potasio", dosis=f"{calculo} kg/ha"))
        if potasio<150.0:
            calculo=round(((dosis_fert)*100)/50)
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculo} kg/ha"))
        if (150.0<= potasio <=300.0):
            st.success("El potasio se encuentra dentro de los rangos recomendados")
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_calcio(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1.3992
        profundidad=30
        densidad=1
        calcio=elementos["calcio_suelo"]
        suministro_suelo=(((calcio*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(4*rendimientoEsperado)+3.25
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if calcio>2000.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de calcio")
            calculo=round(((dosis_fert)*10)/3)
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="FERPAMIX Todo Cultivo", dosis=f"{calculo} kg/ha"))
        if calcio<1000.0:
            calculo=round(((dosis_fert)*100)/12)
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="FERPAMIX PRIME", dosis=f"{calculo} kg/ha"))
        if (1000.0<= calcio <=2000.0):
            st.success("El calcio se encuentra dentro de los rangos recomendados")

    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_magnesio(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1.6579
        profundidad=30
        densidad=1
        magnesio=elementos["magnesio_suelo"]
        suministro_suelo=(((magnesio*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(2.25*rendimientoEsperado)+1.8
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if magnesio>300.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Magnesio")
            calculo=round(((dosis_fert)*10)/4)
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        if magnesio<100.0:
            calculo=round(((dosis_fert)*100)/26)
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="Kieserite – Sulfato de Magnesio", dosis=f"{calculo} kg/ha"))
        if (100.0<= magnesio <=300.0):
            st.success("El Magnesio se encuentra dentro de los rangos recomendados")
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_azufre(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=3.0000
        profundidad=30
        densidad=1
        azufre=elementos["azufre_suelo"]
        suministro_suelo=(((azufre*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(1.5*rendimientoEsperado)+1.2
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if azufre>20.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Azufre")
            calculo=round(((dosis_fert)*10)/18)
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Sulfato de Potasio", dosis=f"{calculo} kg/ha"))
        if azufre<10.0:
            calculo=round(((dosis_fert)*100)/24)
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Sulfato de Amonio", dosis=f"{calculo} kg/ha"))
        if (10.0<= azufre <=20.0):
            st.success("El Azufre se encuentra dentro de los rangos recomendados")

    #         st.success("El Hierro se encuentra dentro de los rangos recomendados")
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_zinc(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1
        profundidad=30
        densidad=1
        zinc=elementos["zinc_suelo"]
        suministro_suelo=(((zinc*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(0.525*rendimientoEsperado)+0.06
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if zinc>5.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de zinc")
            calculo=round(((dosis_fert)*10)/2)
            self.declare(Recomendacion(nutriente="zinc",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        if zinc<1.0:
            calculo=round(((dosis_fert)*100)/33.5)
            self.declare(Recomendacion(nutriente="zinc",fertilizante="Sulfato de Zinc Monohidratado", dosis=f"{calculo} kg/ha"))
        if (1.0<= zinc <=5.0):
            st.success("El zinc se encuentra dentro de los rangos recomendados")

    #         st.success("El manganeso se encuentra dentro de los rangos recomendados")
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_boro(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1
        profundidad=30
        densidad=1
        boro=elementos["boro_suelo"]
        suministro_suelo=(((boro*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(0.525*rendimientoEsperado)+0.06
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if boro>1.5:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de boro")
            calculo=round(((dosis_fert)*10)/1)
            self.declare(Recomendacion(nutriente="boro",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        if boro<0.5:
            calculo=round(((dosis_fert)*100)/10)
            self.declare(Recomendacion(nutriente="boro",fertilizante="Ferpaboro", dosis=f"{calculo} kg/ha"))
        if (0.5<= boro <=1.5):
            st.success("El boro se encuentra dentro de los rangos recomendados")


    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura,ph=MATCH.ph),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_ph(self,textura,elementos,rendimientoEsperado,etapa,ph):
        factor_conversion=2.55
        profundidad=30
        densidad=1
        pe_calcio=20
        ph=elementos["ph_suelo"]
        aluminio=elementos["aluminio_suelo"]
        dosis_cal=0
        if (textura=="franco-arcilloso" or textura=="arcilloso") and (ph<5.5):
            dosis_cal=aluminio*2.0
            self.declare(Recomendacion(nutriente="pH",fertilizante="Carbonato de Calcio para elevar ph a 5.5", dosis=f"{dosis_cal} kg/ha"))

        if textura=="franco" and (ph<5.5):
            dosis_cal=aluminio*1.5
            self.declare(Recomendacion(nutriente="pH",fertilizante="Carbonato de Calcio para elevar ph a 5.5", dosis=f"{dosis_cal} kg/ha"))

        if (5.5<= ph <=7.0):
            st.success("El pH se encuentra dentro de los rangos recomendados")
        azufre_agricola=0 #kg/ha
        kg_aluminio=aluminio*10
        dosis_azufre=((kg_aluminio*pe_calcio)*profundidad*densidad*0.1)*factor_conversion
        #bajar ph hasta 6.5
        if (7.0<= ph <=7.5):
            self.declare(Recomendacion(nutriente="pH",fertilizante="Azufre Agricola para bajar ph a 6.5", dosis=f"877-1096 kg/ha"))
        
        if (7.5<= ph <=8.0):
            self.declare(Recomendacion(nutriente="pH",fertilizante="Azufre Agricola para bajar ph a 6.5", dosis=f"1645-2193 kg/ha"))
        
        if (8.0<= ph <=8.5):
            self.declare(Recomendacion(nutriente="pH",fertilizante="Azufre Agricola para bajar ph a 6.5", dosis=f"1645-2193 kg/ha"))
    
    #cacao
    
    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_nitrogeno_cacao(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1.2857
        profundidad=30
        densidad=1
        nitrogeno=elementos["nitrogeno_suelo"]
        
        suministro_suelo=(((nitrogeno*factor_oxidada)*profundidad)*densidad)*0.1
        demanda_cultivo=12
        # demanda_cultivo=(extra*rendimientoEsperado)+aerea
        eficiencia_recuperacion=1.5
        dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        # dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if nitrogeno>40.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Nitrogeno")
            calculo=round(((dosis_fert)*10)/16)
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="FERPAMIX Cacao Producción", dosis=f"{calculo} kg/ha"))
        if nitrogeno<15.0:
            calculo=round(((dosis_fert)*100)/16)
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        if (15.0<= nitrogeno <=40.0):
            st.success("El nitrogeno se encuentra dentro de los rangos recomendados")
        
        
    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_fosforo_cacao(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=2.2914
        profundidad=30
        densidad=1
        fosforo=elementos["fosforo_suelo"]
        suministro_suelo=(((fosforo*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(3.25*rendimientoEsperado)+2.6
        eficiencia_recuperacion=2
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        
        if fosforo>25.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Fosforo")
            calculo=round(((dosis_fert)*10)/3)
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="FERPAMIX Cacao Producción", dosis=f"{calculo} kg/ha"))
        if fosforo<10.0:
            calculo=round(((dosis_fert)*100)/30)
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="Radical Phos", dosis=f"{calculo} kg/ha"))
        if (10.0<= fosforo <=25.0):
            st.success("El Fosforo se encuentra dentro de los rangos recomendados")
            
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_potasio_cacao(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1.2046
        profundidad=30
        densidad=1
        potasio=elementos["potasio_suelo"]
        suministro_suelo=(((potasio*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(17.5*rendimientoEsperado)+15.5
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if potasio>250.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Fosforo")
            calculo=round(((dosis_fert)*10)/32)
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Polysop", dosis=f"{calculo} kg/ha"))
        if potasio<100.0:
            calculo=round(((dosis_fert)*100)/37)
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Potassium Plus", dosis=f"{calculo} kg/ha"))
        if (100.0<= potasio <=250.0):
            st.success("El potasio se encuentra dentro de los rangos recomendados")

    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_calcio_cacao(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1.3992
        profundidad=30
        densidad=1
        calcio=elementos["calcio_suelo"]
        suministro_suelo=(((calcio*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(4*rendimientoEsperado)+3.25
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if calcio>1200.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de calcio")
            calculo=round(((dosis_fert)*10)/3)
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="Radical Phos", dosis=f"{calculo} kg/ha"))
        if calcio<500.0:
            calculo=round(((dosis_fert)*100)/9)
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="FERPAMIX Cacao Producción LC", dosis=f"{calculo} kg/ha"))
        if (500.0<= calcio <=1200.0):
            st.success("El calcio se encuentra dentro de los rangos recomendados")

    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_magnesio_cacao(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1.6579
        profundidad=30
        densidad=1
        magnesio=elementos["magnesio_suelo"]
        suministro_suelo=(((magnesio*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(2.25*rendimientoEsperado)+1.8
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if magnesio>150.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Magnesio")
            calculo=round(((dosis_fert)*10)/8)
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="FERPAMIX Cacao Producción", dosis=f"{calculo} kg/ha"))
        if magnesio<80.0:
            calculo=round(((dosis_fert)*100)/26)
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="FERPAMIX Cacao Producción LC", dosis=f"{calculo} kg/ha"))
        if (100.0<= magnesio <=300.0):
            st.success("El Magnesio se encuentra dentro de los rangos recomendados")
    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_azufre_cacao(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=3.0000
        profundidad=30
        densidad=1
        azufre=elementos["azufre_suelo"]
        suministro_suelo=(((azufre*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(1.5*rendimientoEsperado)+1.2
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if azufre>20.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de Azufre")
            calculo=round(((dosis_fert)*10)/9.5)
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Potassium Plus", dosis=f"{calculo} kg/ha"))
        if azufre<10.0:
            calculo=round(((dosis_fert)*100)/24)
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Sulfato de Amonio", dosis=f"{calculo} kg/ha"))
        if (10.0<= azufre <=20.0):
            st.success("El Azufre se encuentra dentro de los rangos recomendados")

    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_zinc_cacao(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1
        profundidad=30
        densidad=1
        zinc=elementos["zinc_suelo"]
        suministro_suelo=(((zinc*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(0.525*rendimientoEsperado)+0.06
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if zinc>3.0:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de zinc")
            calculo=round(((dosis_fert)*10)/2)
            self.declare(Recomendacion(nutriente="zinc",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        if zinc<1.0:
            calculo=round(((dosis_fert)*100)/33.5)
            self.declare(Recomendacion(nutriente="zinc",fertilizante="Sulfato de Zinc Monohidratado", dosis=f"{calculo} kg/ha"))
        if (1.0<= zinc <=3.0):
            st.success("El zinc se encuentra dentro de los rangos recomendados")

    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_boro_cacao(self,textura,elementos,rendimientoEsperado,etapa):
        factor_oxidada=1
        profundidad=30
        densidad=1
        boro=elementos["boro_suelo"]
        suministro_suelo=(((boro*factor_oxidada)*profundidad)*densidad)*0.1
        
        demanda_cultivo=(0.525*rendimientoEsperado)+0.06
        eficiencia_recuperacion=1.7
        #dosis_fert=((demanda_cultivo*0.25)+demanda_cultivo)*eficiencia_recuperacion
        dosis_fert=(suministro_suelo-demanda_cultivo)*eficiencia_recuperacion
        
        if boro>1.5:
            st.warning("Hay exceso, solo aplique una dosis de mantenimiento de boro")
            calculo=round(((dosis_fert)*10)/1)
            self.declare(Recomendacion(nutriente="boro",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        if boro<0.5:
            calculo=round(((dosis_fert)*100)/10)
            self.declare(Recomendacion(nutriente="boro",fertilizante="Ferpaboro", dosis=f"{calculo} kg/ha"))
        if (0.5<= boro <=1.5):
            st.success("El boro se encuentra dentro de los rangos recomendados")


    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado,etapa=MATCH.etapa),
          Suelo(textura=MATCH.textura,ph=MATCH.ph),
          Nutrientes(elementos=MATCH.elementos)
          )
    def recomendar_ph_cacao(self,textura,elementos,rendimientoEsperado,etapa,ph):
        factor_conversion=2.55
        profundidad=30
        densidad=1
        pe_calcio=20
        ph=elementos["ph_suelo"]
        aluminio=elementos["aluminio_suelo"]
        dosis_cal=0
        if (textura=="franco-arcilloso" or textura=="arcilloso") and (ph<5.5):
            dosis_cal=aluminio*2.0
            self.declare(Recomendacion(nutriente="pH",fertilizante="Carbonato de Calcio para elevar ph a 5.5", dosis=f"{dosis_cal} kg/ha"))

        if textura=="franco" and (ph<5.5):
            dosis_cal=aluminio*1.5
            self.declare(Recomendacion(nutriente="pH",fertilizante="Carbonato de Calcio para elevar ph a 5.5", dosis=f"{dosis_cal} kg/ha"))

        if (5.5<= ph <=6.5):
            st.success("El pH se encuentra dentro de los rangos recomendados")
        azufre_agricola=0 #kg/ha
        kg_aluminio=aluminio*10
        dosis_azufre=((kg_aluminio*pe_calcio)*profundidad*densidad*0.1)*factor_conversion
        #bajar ph hasta 6.5
        if (7.0<= ph <=7.5):
            self.declare(Recomendacion(nutriente="pH",fertilizante="Azufre Agricola para bajar ph a 6.5", dosis=f"877-1096 kg/ha"))
        
        if (7.5<= ph <=8.0):
            self.declare(Recomendacion(nutriente="pH",fertilizante="Azufre Agricola para bajar ph a 6.5", dosis=f"1645-2193 kg/ha"))
        
        if (8.0<= ph <=8.5):
            self.declare(Recomendacion(nutriente="pH",fertilizante="Azufre Agricola para bajar ph a 6.5", dosis=f"1645-2193 kg/ha"))

        
    @Rule(Recomendacion(fertilizante=MATCH.fertilizante, dosis=MATCH.dosis,nutriente=MATCH.nutriente))
    def mostrar_recomendacion(self, fertilizante, dosis, nutriente):
        print(f"Deficiencia de {nutriente}, Recomendación: Aplicar {fertilizante} en una dosis de {dosis}.")
        df.loc[len(df)] = [f"Deficiencia de {nutriente}",f"Recomendación: Aplicar {fertilizante} en una dosis de {dosis}."]










# Motor de reglas para la recomendación de fertilizantes
class SistemaRecomendacionFertilizantesSinAnalisis(KnowledgeEngine):
    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Hongos(hongos=MATCH.hongos),
          Planta(hojas=MATCH.hojas,tallo=MATCH.tallo)
          )
    def recomendar_nitrogeno(self,rendimientoEsperado,malezas,hongos,etapa,textura,hojas,tallo):
        factor=0
        if (tallo!="Tallo robusto y firme") and (hojas!="Verdes") and (textura!="franco-arcilloso") and (not("Urtica Dioica" and "Chenopodium") in malezas) and not("Micorrizas" in hongos) and (etapa!="Crecimiento vegetativo"):
            factor=1.5
            calculo=round((((rendimientoEsperado*factor)*100)/34),2)
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="Nitrato de Amonio", dosis=f"{calculo} kg/ha"))
        else:
            factor=1.0
            calculo=round((((rendimientoEsperado*factor)*100)/46),2)
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculo} kg/ha"))
        
       
        

    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(raices=MATCH.raices)
          )
    def recomendar_fosforo(self,rendimientoEsperado,malezas,etapa,raices,textura):
        factor=0
        if (not("Trebol Rojo") in malezas) and (raices!="Raíces largas y fibrosas")and (etapa!="Crecimiento vegetativo" or "Desarrollo del fruto") and (textura!="franco-arcilloso"):
            factor=0.5
            calculo=round((((rendimientoEsperado*factor)*100)/46),2)
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="Super Fosfato Triple", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.3
            calculo=round((((rendimientoEsperado*factor)*100)/46),2)
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculo} kg/ha"))
        

    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_potasio(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Equisetum Arvense") in malezas) and (etapa=="Crecimiento vegetativo"  or "Desarrollo del fruto") and (hojas=="Amarillamiento entre las nervaduras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=2.0
            calculo=round((((rendimientoEsperado*factor)*100)/50),2)
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculo} kg/ha"))
        else:
            factor=1.2
            calculo=round((((rendimientoEsperado*factor)*100)/46),2)
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Nitrato de potasio", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_calcio(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Achillea Millefolium" and "Taraxacum Officinale") in malezas) and (etapa!="Floración y cuajado") and (hojas!="Hojas deformadas o con manchas negras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=0.5
            calculo=round((((rendimientoEsperado*factor)*100)/12),2)
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="FERPAMIX PRIME", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.2
            calculo=round((((rendimientoEsperado*factor)*100)/3),2)
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="FERPAMIX Todo Cultivo", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_magnesio(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Medicago sativa") in malezas) and (etapa!="Desarrollo del fruto") and (hojas!= "Amarillentas" or "Amarillamiento entre las nervaduras") and (textura!="franco-arcilloso"):
            factor=0.4
            calculo=round((((rendimientoEsperado*factor)*100)/26),2)
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="Kieserite – Sulfato de Magnesio", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.2
            calculo=round((((rendimientoEsperado*factor)*100)/4),2)
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_azufre(self,rendimientoEsperado,malezas,hojas,textura):
        factor=0
        if (not("Sinapis Arvensis") in malezas) and (hojas!= "Hojas deformadas o con manchas negras") and (textura!="franco-arcilloso"):
            factor=0.3
            calculo=round((((rendimientoEsperado*factor)*100)/24),2)
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Sulfato de Amonio", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.1
            calculo=round((((rendimientoEsperado*factor)*100)/18),2)
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Sulfato de Potasio", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango",etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos)
          )
    def recomendar_boro(self,rendimientoEsperado,hojas,textura,frutos,etapa):
        factor=0
        if (frutos!="Frutos pequeños o deformes") and (etapa!="Floración y cuajado") and (hojas!= "Hojas deformadas o con manchas negras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=0.01
            calculo=round((((rendimientoEsperado*factor)*100)/10),2)
            self.declare(Recomendacion(nutriente="Boro",fertilizante="Ferpaboro", dosis=f"{calculo:.2f} kg/ha"))
        else:
            factor=0.005
            calculo=round((((rendimientoEsperado*factor)*100)/1),2)
            self.declare(Recomendacion(nutriente="Boro",fertilizante="Ferpagrow", dosis=f"{calculo:.2f} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos),
          Malezas(malezas=MATCH.malezas),
          )
    def recomendar_zinc(self,rendimientoEsperado,hojas,textura,frutos,malezas):
        factor=0
        if (not("Plantago Major") in malezas) and (frutos!="Frutos grandes y sanos") and (hojas!= "Verdes") and (textura!="franco-arcilloso"):
            factor=0.01
            calculo=round((((rendimientoEsperado*factor)*100)/33.5),2)
            self.declare(Recomendacion(nutriente="Zinc",fertilizante="Sulfato de Zinc Monohidratado", dosis=f"{calculo:.2f} kg/ha"))
        else:
            factor=0.005
            calculo=round((((rendimientoEsperado*factor)*100)/2),2)
            self.declare(Recomendacion(nutriente="Zinc",fertilizante="Ferpagrow", dosis=f"{calculo:.2f} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos),
          Malezas(malezas=MATCH.malezas),
          )
    def suelo_agotado(self,rendimientoEsperado,hojas,textura,malezas):
        if (not("Hyparrhenia Rufa") in malezas) and (hojas!= "Amarillentas" or "Amarillamiento entre las nervaduras") and (textura!="franco-arcilloso"):
            factorN=1.25
            factorP=0.4
            factorK=1.6
            calculoN=round((((rendimientoEsperado*factorN)*100)/46),2)
            calculoP=round((((rendimientoEsperado*factorP)*100)/46),2)
            calculoK=round((((rendimientoEsperado*factorK)*100)/50),2)
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculoN} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculoP} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculoK} kg/ha"))
        else:
            factorN=1.0
            factorP=0.3
            factorK=1.2
            calculoN=round((((rendimientoEsperado*factorN)*100)/46),2)
            calculoP=round((((rendimientoEsperado*factorP)*100)/46),2)
            calculoK=round((((rendimientoEsperado*factorK)*100)/50),2)
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculoN} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculoP} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculoK} kg/ha"))
    
    #cacao
    @Rule(Cultivo(tipo="Cacao", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Hongos(hongos=MATCH.hongos),
          Planta(hojas=MATCH.hojas,tallo=MATCH.tallo)
          )
    def recomendar_nitrogeno_cacao(self,rendimientoEsperado,malezas,hongos,etapa,textura,hojas,tallo):
        factor=0
        if (tallo!="Tallo robusto y firme") and (hojas!="Verdes") and (textura!="franco-arcilloso") and (not("Urtica Dioica" and "Chenopodium") in malezas) and not("Micorrizas" in hongos) and (etapa!="Crecimiento vegetativo"):
            factor=25
            calculo=round((((rendimientoEsperado*factor)*100)/16),2)
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        else:
            factor=20
            calculo=round((((rendimientoEsperado*factor)*100)/16),2)
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="FERPAMIX Cacao Producción", dosis=f"{calculo} kg/ha"))
        
       
        # if 6.0 <= ph <= 7.5:
        #     self.declare(Recomendacion(fertilizante="Urea 46%", dosis=f"100 kg/ha"))
        # else:
        #     self.declare(Recomendacion(fertilizante="Fertilizante balanceado NPK", dosis="120 kg/ha"))
    


    @Rule(Cultivo(tipo="Cacao", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(raices=MATCH.raices)
          )
    def recomendar_fosforo_cacao(self,rendimientoEsperado,malezas,etapa,raices,textura):
        factor=0
        if (not("Trebol Rojo") in malezas) and (raices!="Raíces largas y fibrosas")and (etapa!="Crecimiento vegetativo" or "Desarrollo del fruto") and (textura!="franco-arcilloso"):
            factor=8
            calculo=round((((rendimientoEsperado*factor)*100)/30),2)
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="Radical Phos", dosis=f"{calculo} kg/ha"))
        else:
            factor=6
            calculo=round((((rendimientoEsperado*factor)*100)/3),2)
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="FERPAMIX Cacao Producción", dosis=f"{calculo} kg/ha"))
        

    @Rule(Cultivo(tipo="Cacao", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_potasio_cacao(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Equisetum Arvense") in malezas) and (etapa=="Crecimiento vegetativo"  or "Desarrollo del fruto") and (hojas=="Amarillamiento entre las nervaduras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=35
            calculo=round((((rendimientoEsperado*factor)*100)/37),2)
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Potassium Plus", dosis=f"{calculo} kg/ha"))
        else:
            factor=25
            calculo=round((((rendimientoEsperado*factor)*100)/32),2)
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Polysop", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Cacao", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_calcio_cacao(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Achillea Millefolium" and "Taraxacum Officinale") in malezas) and (etapa!="Floración y cuajado") and (hojas!="Hojas deformadas o con manchas negras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=5
            calculo=round((((rendimientoEsperado*factor)*100)/3),2)
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="Radical Phos", dosis=f"{calculo} kg/ha"))
        else:
            factor=7
            calculo=round((((rendimientoEsperado*factor)*100)/9),2)
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="FERPAMIX Cacao Producción LC", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Cacao", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_magnesio_cacao(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Medicago sativa") in malezas) and (etapa!="Desarrollo del fruto") and (hojas!= "Amarillentas" or "Amarillamiento entre las nervaduras") and (textura!="franco-arcilloso"):
            factor=6
            calculo=round((((rendimientoEsperado*factor)*100)/26),2)
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="FERPAMIX Cacao Producción LC", dosis=f"{calculo} kg/ha"))
        else:
            factor=4
            calculo=round((((rendimientoEsperado*factor)*100)/8),2)
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="FERPAMIX Cacao Producción", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_azufre_cacao(self,rendimientoEsperado,malezas,hojas,textura):
        factor=0
        if (not("Sinapis Arvensis") in malezas) and (hojas!= "Hojas deformadas o con manchas negras") and (textura!="franco-arcilloso"):
            factor=4
            calculo=round((((rendimientoEsperado*factor)*100)/24),2)
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Sulfato de Amonio", dosis=f"{calculo} kg/ha"))
        else:
            factor=2
            calculo=round((((rendimientoEsperado*factor)*100)/9.5),2)
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Potassium Plus", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Cacao",etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos)
          )
    def recomendar_boro_cacao(self,rendimientoEsperado,hojas,textura,frutos,etapa):
        factor=0
        if (frutos!="Frutos pequeños o deformes") and (etapa!="Floración y cuajado") and (hojas!= "Hojas deformadas o con manchas negras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=0.06
            calculo=round((((rendimientoEsperado*factor)*100)/10),2)
            self.declare(Recomendacion(nutriente="Boro",fertilizante="Ferpaboro", dosis=f"{calculo:.2f} kg/ha"))
        else:
            factor=0.03
            calculo=round((((rendimientoEsperado*factor)*100)/1),2)
            self.declare(Recomendacion(nutriente="Boro",fertilizante="Ferpagrow", dosis=f"{calculo:.2f} kg/ha"))
        
    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos),
          Malezas(malezas=MATCH.malezas),
          )
    def recomendar_zinc_cacao(self,rendimientoEsperado,hojas,textura,frutos,malezas):
        factor=0
        if (not("Plantago Major") in malezas) and (frutos!="Frutos grandes y sanos") and (hojas!= "Verdes") and (textura!="franco-arcilloso"):
            factor=0.1
            calculo=round((((rendimientoEsperado*factor)*100)/33.5),2)
            self.declare(Recomendacion(nutriente="Zinc",fertilizante="Sulfato de Zinc Monohidratado", dosis=f"{calculo:.2f} kg/ha"))
        else:
            factor=0.05
            calculo=round((((rendimientoEsperado*factor)*100)/2),2)
            self.declare(Recomendacion(nutriente="Zinc",fertilizante="Ferpagrow", dosis=f"{calculo:.2f} kg/ha"))
        
    @Rule(Cultivo(tipo="Cacao",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos),
          Malezas(malezas=MATCH.malezas),
          )
    def suelo_agotado_cacao(self,rendimientoEsperado,hojas,textura,malezas):
        if (not("Hyparrhenia Rufa") in malezas) and (hojas!= "Amarillentas" or "Amarillamiento entre las nervaduras") and (textura!="franco-arcilloso"):
            factorN=27.5
            factorP=7
            factorK=30
            calculoN=round((((rendimientoEsperado*factorN)*100)/46),2)
            calculoP=round((((rendimientoEsperado*factorP)*100)/46),2)
            calculoK=round((((rendimientoEsperado*factorP)*100)/50),2)
            
            
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculoN} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculoP} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculoK} kg/ha"))
        else:
            factorN=20
            factorP=6
            factorK=25
            calculoN=round((((rendimientoEsperado*factorN)*100)/46),2)
            calculoP=round((((rendimientoEsperado*factorP)*100)/46),2)
            calculoK=round((((rendimientoEsperado*factorP)*100)/50),2)
            
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculoN} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculoP} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculoK} kg/ha"))

    
    @Rule(Recomendacion(fertilizante=MATCH.fertilizante, dosis=MATCH.dosis,nutriente=MATCH.nutriente))
    def mostrar_recomendacion(self, fertilizante, dosis, nutriente):
        print(f"Deficiencia de {nutriente}, Recomendación: Aplicar {fertilizante} en una dosis de {dosis}.")
        df.loc[len(df)] = [f"Deficiencia de {nutriente}",f"Recomendación: Aplicar {fertilizante} en una dosis de {dosis}."]



# Crear un DataFrame vacío
df = pd.DataFrame(columns=['Deficiencia', 'Recomendacion'])
# Diccionario de productos simples con dosis estándar por hectárea

# Ejemplo de uso
watch('RULES', 'FACTS')
# Reiniciar el motor
st.title("Sistema Generador de Recomendaciones de Fertilizantes")
tab1, tab2 = st.tabs(["Análisis de Suelo", "Sin análisis de suelo"])
with tab1:
    with st.form(key="sin_suelo",border=False):
#Crear pestañas
        # st.html(
        # """<style>
        # .block-container{
        # background-color: rgb(43 41 237);
        # }
        # .st-c2 {
        # background-color: rgb(43 41 237);}
        # .st-emotion-cache-12fmjuu{
        # height: 5.75rem;
        # }
        # </style>""")

    # Contenido de la primera pestaña
        
        st.subheader("_Aqui debe ingresar los parametros del análisis de suelo realizado previamente._")
        # Primera fila de columnas
        st.subheader(":blue[_Propiedades del suelo_]",divider=True)
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
        # Selector (dropdown)
            st.subheader("Tipo de Cultivo")
            opcioncultivo = st.selectbox(
                "Elige una opción",
                ["Mango", "Cacao"],label_visibility="collapsed",key="opcioncultivo"
            )
            # Selector (dropdown)
            st.subheader("Rendimiento Esperado (Ton/ha)")
            rendimiento_esperado_con = st.number_input("Ingrese rendimiento", min_value=0.0, max_value=None, value=15.0, step=1.0,label_visibility="collapsed",key="rendimiento_esperado_con")
            
            # Selector (dropdown)
            st.subheader("Etapa de Cultivo")
            etapa_cultivo = st.selectbox(
                "Elige una opción",
                ["Crecimiento vegetativo","Desarrollo del fruto","Floración y cuajado"],key="etapa_cultivo",
            help="Germinación:Mango: 1 a 3 semanas.Cacao: 1 a 4 semanas. - Plántula:Mango: 3 a 6 meses. Cacao: 4 a 6 meses. - Crecimiento vegetativo:Mango: De 1 a 4 años. Cacao: De 1 a 3 años. - Floración:Mango: Una vez al año, dependiendo de la variedad y manejo (puede durar 2-3 meses). Cacao: Floración continua durante el año, con picos estacionales. - Fructificación:Mango: 100-150 días desde la floración hasta la maduración del fruto.Cacao: 5-6 meses desde la floración hasta la maduración de las mazorcas. - Maduración del fruto:Mango: 2-3 semanas en el período de maduración.Cacao: Mazorcas maduran de manera continua según las estaciones. - Senescencia (en árboles viejos):Puede variar dependiendo del manejo del cultivo.    "
            )
            # Input numérico
            st.subheader("PH del suelo")
            ph_suelo = st.number_input("Ingrese PH", min_value=0.0, max_value=14.0, value=5.5, step=0.01,label_visibility="collapsed",key="ph_suelo")
            
            
            with row1_col2:
        # Selector (dropdown)
                st.subheader("Textura del suelo")
                textura_suelo = st.selectbox(
                    "Elige una opción",
                    ["franco", "franco-arcilloso", "arcilloso","otro"],label_visibility="collapsed"
                )
                if textura_suelo=="otro":
                    st.write("No se seleccionó opcion valida.")
                    
                else:
                    pass

                # Input numérico
                st.subheader("Materia orgánica del suelo (%)") 
                mo_suelo = st.number_input("Ingrese M.O", min_value=0.0, max_value=None, value=2.0, step=0.01,label_visibility="collapsed",key="mo_suelo")
                
                    # Input numérico
                st.subheader("Conductividad Eléctrica del suelo (dS/m)")
                ce_suelo = st.number_input("Ingrese C.E (dS/m) ", min_value=0.0, max_value=None, value=0.4, step=0.01,label_visibility="collapsed",key="ce_suelo")
                
                # Input numérico
                st.subheader(" CIC del suelo (meq/100g)")
                cic_suelo = st.number_input("Ingrese C.I.C (meq/100g) ", min_value=0.0, max_value=None, value=15.0, step=0.01,label_visibility="collapsed",key="cic_suelo")
                
                
        st.subheader(":green[_Macronutrientes_]",divider=True)
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
        # Input numérico
            st.subheader("Nitrógeno del suelo (ppm)")
            nitrogeno_suelo = st.number_input("Ingrese Nitrogeno (mg/kg) o ppm", min_value=0.0, max_value=None, value=20.0, step=0.01,label_visibility="collapsed",key="nitrogeno_suelo")
            # Input numérico
            st.subheader("Fósforo del suelo (ppm)")
            fosforo_suelo = st.number_input("Ingrese Fosforo (mg/kg) o ppm", min_value=0.0, max_value=None, value=15.0, step=0.01,label_visibility="collapsed",key="fosforo_suelo")
            
            # Input numérico
            st.subheader("Potasio del suelo (ppm)")
            potasio_suelo = st.number_input("Ingrese Potasio (mg/kg) o ppm", min_value=0.0, max_value=None, value=150.0, step=0.01,label_visibility="collapsed",key="potasio_suelo")
            
        with row2_col2:
            # Input numérico
            st.subheader("Calcio del suelo (ppm)")
            calcio_suelo = st.number_input("Ingrese Calcio (ppm) ", min_value=0.0, max_value=None, value=1000.0, step=0.01,label_visibility="collapsed",key="calcio_suelo")
            
            # Input numérico
            st.subheader("Magnesio del suelo (ppm)")
            magnesio_suelo = st.number_input("Ingrese Magnesio (ppm) ", min_value=0.0, max_value=None, value=100.0, step=0.01,label_visibility="collapsed",key="magnesio_suelo")
            
            # Input numérico
            st.subheader("Azufre del suelo (ppm)")
            azufre_suelo = st.number_input("Ingrese Azufre (ppm) ", min_value=0.0, max_value=None, value=10.0, step=0.01,label_visibility="collapsed",key="azufre_suelo")
            
        # with row1_col2:
   
            
        st.subheader(":orange[_Micronutrientes_]",divider="orange")
        row3_col1, row3_col2 = st.columns(2)
        with row3_col1:
            # Input numérico
            st.subheader("Hierro del suelo (ppm)")
            hierro_suelo = st.number_input("Ingrese Hierro % ", min_value=0.0, max_value=None, value=5.0, step=0.01,label_visibility="collapsed",key="hierro_suelo")
            
            # Input numérico
            st.subheader("Zinc del suelo (ppm)")
            zinc_suelo = st.number_input("Ingrese Zinc  ", min_value=0.0, max_value=None, value=1.0, step=0.01,label_visibility="collapsed",key="zinc_suelo")
            
            # Input numérico
            st.subheader("Manganeso del suelo (ppm)")
            manganeso_suelo = st.number_input("Ingrese Manganeso  ", min_value=0.0, max_value=None, value=2.0, step=0.01,label_visibility="collapsed",key="manganeso_suelo")
        
        with row3_col2:
            # Input numérico
            st.subheader("Cobre del suelo (ppm)")
            cobre_suelo = st.number_input("Ingrese Cobre  ", min_value=0.0, max_value=None, value=0.5, step=0.01,label_visibility="collapsed",key="cobre_suelo")
            
            st.subheader("Boro del suelo (ppm)")
            boro_suelo = st.number_input("Ingrese Boro ", min_value=0.0, max_value=None, value=0.5, step=0.01,label_visibility="collapsed",key="boro_suelo")
            st.subheader("Aluminio del suelo (ppm)")
            aluminio_suelo = st.number_input("Ingrese Aluminio ", min_value=0.0, max_value=None, value=0.5, step=0.01,label_visibility="collapsed",key="aluminio_suelo")
            
            # st.subheader(":green[_Relacion de Bases Intercambiables_]",divider=True)
            # st.subheader("Calcio/Potasio")
            # relacion_cak_suelo = st.number_input("Ingrese relacion ", min_value=0.0, max_value=None, value=0.5, step=0.01,label_visibility="collapsed",key="relacion_cak_suelo")
            
            # st.subheader("Calcio/Magnesio")
            # relacion_camg_suelo = st.number_input("Ingrese relacion ", min_value=0.0, max_value=None, value=0.5, step=0.01,label_visibility="collapsed",key="relacion_camg_suelo")
            
            # st.subheader("Calcio+Magnesio/Potasio")
            # relacion_camgk_suelo = st.number_input("Ingrese relacion ", min_value=0.0, max_value=None, value=0.5, step=0.01,label_visibility="collapsed",key="relacion_camgk_suelo")
            
            # st.subheader("Magnesio/Potasio")
            # relacion_mgk_suelo = st.number_input("Ingrese relacion ", min_value=0.0, max_value=None, value=0.5, step=0.01,label_visibility="collapsed",key="relacion_mgk_suelo")
            
        st.subheader("",divider="blue")
    # Botón para enviar el formulario
        enviadoA = st.form_submit_button("Enviar")
        if enviadoA:

            nutri["nitrogeno_suelo"]=nitrogeno_suelo
            nutri["mo_suelo"]=mo_suelo
            nutri["ce_suelo"]=ce_suelo
            nutri["cic_suelo"]=cic_suelo
            nutri["ph_suelo"]=ph_suelo
            nutri["potasio_suelo"]=potasio_suelo
            nutri["calcio_suelo"]=calcio_suelo
            nutri["magnesio_suelo"]=magnesio_suelo
            nutri["fosforo_suelo"]=fosforo_suelo
            nutri["azufre_suelo"]=azufre_suelo
            nutri["hierro_suelo"]=hierro_suelo
            nutri["zinc_suelo"]=zinc_suelo
            nutri["manganeso_suelo"]=manganeso_suelo
            nutri["cobre_suelo"]=cobre_suelo
            nutri["boro_suelo"]=boro_suelo
            nutri["aluminio_suelo"]=aluminio_suelo
            # nutri["relacion_cak_suelo"]=relacion_cak_suelo
            # nutri["relacion_camg_suelo"]=relacion_camg_suelo
            # nutri["relacion_camgk_suelo"]=relacion_camgk_suelo
            # nutri["relacion_mgk_suelo"]=relacion_mgk_suelo

            engine = SistemaRecomendacionFertilizantesConAnalisis()
            engine.reset()  
            
            
            # Declarar hechos
            engine.declare(Cultivo(tipo=opcioncultivo, etapa=etapa_cultivo,rendimientoEsperado=rendimiento_esperado_con))
            engine.declare(Suelo(textura=textura_suelo))
            engine.declare(Nutrientes(elementos=nutri))
            
            engine.run() 


            # Mostrar el DataFrame en una tabla utilizando st.table
            st.title(f":red[Deficiencias Detectadas en {opcioncultivo}]")
            st.subheader("Recomendaciones:")
            st.table(df.assign(hack='').set_index('hack', drop=True))
            
            plan_fertilizacion(df)
    # Contenido de la segunda pestaña
with tab2:
    with st.form(key="con_suelo",border=False):
        st.header("Parametros visuales")
        st.subheader("_Indicadores físicos y estéticos de la planta_",divider="blue")
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            # Selector (dropdown)
            st.subheader("Rendimiento Esperado")
            rendimiento_esperado = st.number_input("Ingrese rendimiento", min_value=0.0, max_value=None, value=15.0, step=1.0,label_visibility="collapsed",key="rendimiento_esperado")
            
            st.subheader("Tipo de Cultivo")
            opcioncultivo_sin = st.selectbox(
                "Elige una opción",
                ["Mango", "Cacao"],label_visibility="collapsed",key="opcioncultivo_sin"
            )
            # Selector (dropdown)
            st.subheader("Textura del suelo")
            textura_suelo_sin = st.selectbox(
                "Elige una opción",
                ["franco", "franco-arcilloso", "arcilloso","otro"],label_visibility="collapsed",key="textura_suelo_sin"
            )
            if textura_suelo_sin=="otro":
                st.write("No se seleccionó opción vlida.")
                
            else:
                pass
            # Selector (dropdown)
            st.subheader("Etapa de Cultivo")
            etapa_cultivo_sin = st.selectbox(
                "Elige una opción",
                ["Crecimiento vegetativo","Desarrollo del fruto","Floración y cuajado"],key="etapa_cultivo_sin",
            help="Germinación:Mango: 1 a 3 semanas.Cacao: 1 a 4 semanas. - Plántula:Mango: 3 a 6 meses. Cacao: 4 a 6 meses. - Crecimiento vegetativo:Mango: De 1 a 4 años. Cacao: De 1 a 3 años. - Floración:Mango: Una vez al año, dependiendo de la variedad y manejo (puede durar 2-3 meses). Cacao: Floración continua durante el año, con picos estacionales. - Fructificación:Mango: 100-150 días desde la floración hasta la maduración del fruto.Cacao: 5-6 meses desde la floración hasta la maduración de las mazorcas. - Maduración del fruto:Mango: 2-3 semanas en el período de maduración.Cacao: Mazorcas maduran de manera continua según las estaciones. - Senescencia (en árboles viejos):Puede variar dependiendo del manejo del cultivo.    "
            )
            
            
            # st.subheader("Estado las hojas")
            # st.radio("**Deformaciones en la hojas?**",["No","Si"],captions=["_Estado normal_","_Deficiencias Nutricionales_"],horizontal=True,key="estado_hoja")

        with row2_col2:
            st.subheader("Hojas")
            color_hoja = st.selectbox(
                "Elige una opción",
                ["Verdes", "Amarillentas","Amarillamiento entre las nervaduras","Hojas deformadas o con manchas negras","Marrones o secas"],label_visibility="collapsed",key="color_hoja"
            )
            st.subheader("Raices")
            raices = st.selectbox(
                "Elige una opción",
                ["Raíces largas y fibrosas", "Raíces cortas y deformadas","Raíces podridas"],label_visibility="collapsed",key="raices"
            )
            st.subheader("Tallo")
            tallo = st.selectbox(
                "Elige una opción",
                ["Tallo robusto y firme", "Tallo débil y alargado","Presencia de necrosis en el tallo"],label_visibility="collapsed",key="tallo"
            )
            st.subheader("Frutos")
            frutos = st.selectbox(
                "Elige una opción",
                ["Frutos pequeños o deformes", "Pudrición apical en frutos","Frutos grandes y sanos"],label_visibility="collapsed",key="frutos"
            )
        with st.container(border=True):
            st.subheader("Malezas",help="Seleccione las malezas que tenga presente en su cultivo")
            cl1,cl2,cl3,cl4,cl5,cl6=st.columns(6)
            with cl1:
                with st.container(border=True):
                    st.image("./Urtica_Dioica.jpg",caption="Urtica Dioica")
                    
                    urtica_dioica=st.checkbox("urtica_dioica",key="urtica_dioica",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (urtica_dioica):
                        malezas_suelo.append("Urtica Dioica")
                with st.container(border=True):
                    st.image("./Acederilla.jpg",caption="Acederilla")
                
                    acederilla=st.checkbox("acederilla",key="acederilla",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (acederilla):
                        malezas_suelo.append("Acederilla")
            with cl2:
                with st.container(border=True):
                    st.image("./Chenopodium.jpg",caption="Chenopodium")
                    
                    chenopodium=st.checkbox("chenopodium",key="chenopodium",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (chenopodium):
                        malezas_suelo.append("Chenopodium")
                with st.container(border=True):
                    st.image("./Pasto_Johnson.jpg",caption="Pasto Johnson")
            
                    Pasto_Johnson=st.checkbox("Logo",key="Pasto_Johnson",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (Pasto_Johnson):
                        malezas_suelo.append("Pasto Johnson")
                        
            with cl3:
                with st.container(border=True):
                    st.image("./Trebol_Rojo.jpg",caption="Trebol Rojo")
                
                    trebol=st.checkbox("Logo",key="trebol",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (trebol):
                        malezas_suelo.append("Trebol Rojo")
        
                with st.container(border=True):
                    st.image("./Achillea_Millefolium.jpg",caption="Achillea Millefolium")
                
                    achillea_millefolium=st.checkbox("Logo",key="achillea_millefolium",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (achillea_millefolium):
                        malezas_suelo.append("Achillea Millefolium")
                       
            with cl4:
                with st.container(border=True):
                    st.image("./Equisetum_Arvense.jpg",caption="Equisetum Arvense")
                    
                    Equisetum_arvense=st.checkbox("Logo",key="Equisetum_arvense",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (Equisetum_arvense):
                        malezas_suelo.append("Equisetum Arvense")
                        
                        
                with st.container(border=True):
                    st.image("./Taraxacum_Officinale.jpg",caption="Taraxacum Officinale")
                    
                    Taraxacum_officinale=st.checkbox("Logo",key="Taraxacum_officinale",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (Taraxacum_officinale):
                        malezas_suelo.append("Taraxacum Officinale")
                        
            with cl5:
                with st.container(border=True):
                    st.image("./Hyparrhenia_Rufa.jpg",caption="Hyparrhenia Rufa")
                    
                    Hyparrhenia_rufa=st.checkbox("Logo",key="Hyparrhenia_rufa",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (Hyparrhenia_rufa):
                        malezas_suelo.append("Hyparrhenia Rufa")
                        
                
                with st.container(border=True):
                    st.image("./Medicago_Sativa.jpg",caption="Medicago Sativa")
                    
                    Medicago_sativa=st.checkbox("Logo",key="Medicago_sativa",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (Medicago_sativa):
                        malezas_suelo.append("Medicago Sativa")
                     
            with cl6:
                with st.container(border=True):
                    st.image("./Sinapis_Arvensis.jpg",caption="Sinapis Arvensis")
                
                    Sinapis_arvensis=st.checkbox("Logo",key="Sinapis_arvensis",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (Sinapis_arvensis):
                        malezas_suelo.append("Sinapis Arvensis")
                        
                
                with st.container(border=True):
                    st.image("./Plantago_Major.jpg",caption="Plantago Major")
                    
                    plantago_major=st.checkbox("Logo",key="plantago_major",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (plantago_major):
                        malezas_suelo.append("Plantago Major")
                        
                
        with st.container(border=True):
            st.subheader("Hongos",help="Seleccione los hongos en su cultivo")
            cl1,cl2,cl3,cl4,cl5,cl6=st.columns(6)
            with cl1:
                with st.container(border=True):
                    st.image("./Micorrizas.jpg",caption="Micorrizas")
                    
                    micorrizas=st.checkbox("micorrizas",key="micorrizas",label_visibility="collapsed")
                # st.subheader("Crecimiento general")
                # st.radio("**Problemas de crecimiento de la planta?**",["No","Si"],captions=["_Crecimiento correcto_","_Crecimiento lento o atrofiado_"],horizontal=True,key="crecimiento")
                    if (micorrizas):
                        hongos_suelo.append("Micorrizas")
                        
            
        st.subheader("",divider="blue")
    # Botón para enviar el formulario
        enviadoS = st.form_submit_button("Enviar")
            
        if enviadoS:

            engine = SistemaRecomendacionFertilizantesSinAnalisis()
            engine.reset()  
            # Declarar hechos
            engine.declare(Cultivo(tipo=opcioncultivo_sin, etapa=etapa_cultivo_sin,rendimientoEsperado=rendimiento_esperado))
            engine.declare(Suelo(textura=textura_suelo_sin))
            engine.declare(Malezas(malezas=malezas_suelo))
            engine.declare(Hongos(hongos=hongos_suelo))
            engine.declare(Planta(hojas=color_hoja,tallo=tallo,raices=raices,frutos=frutos))
            

            
            
            engine.run() 
            # Mostrar el DataFrame en una tabla utilizando st.table
            st.title(f":red[Deficiencias Detectadas en {opcioncultivo_sin}]")
            st.subheader("Recomendaciones:")
            st.table(df.assign(hack='').set_index('hack', drop=True))
            # sql="select * from rangos_deficiencia"
            # cursor.execute(sql)
            # datos = cursor.fetchall()
            
            # Convertir los datos en un DataFrame
            # dataf = pd.DataFrame(datos, columns=cursor.column_names)
            # print("Consulta ejecutada correctamente. Datos obtenidos:")
            # print(dataf)
            # conectar.commit()


#     hojas
# maleza
    # for fact in engine.facts.items():
    #     print(fact)  # Print the fact name and value    
    # st.write([malezas_suelo,hongos_suelo,color_hoja])
# hongo

# def init_connection():
#     return mysql.connector.connect(**st.secrets["mysql"])

# conn=init_connection()

# @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()
    
# rows=run_query("select * from rangos_deficiencia;")

# for row in rows:
#     st.write(f"{row[0]} as a : {row[1]} ppm")

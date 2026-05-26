from experta import *

# Definir hechos relacionados con los cultivos y el suelo
class Cultivo(Fact):
    """Representa un cultivo específico"""
    tipo = Field(str, mandatory=True)  # Ejemplo: "maíz", "mango", "cacao"
    etapa = Field(str)  # Ejemplo: "germinación", "floración", "maduración"
    rendimientoEsperado=Field(float, mandatory=True)

class Suelo(Fact):
    """Representa las características del suelo"""
    ph = Field(float)  # Ejemplo: pH del suelo
    textura = Field(str, mandatory=True)  # Ejemplo: "arenoso", "arcilloso", "limoso"
    
class Planta(Fact):
    """Representa las características del planta"""
    hojas = Field(str)  
    raices = Field(str) 
    tallo=Field(str)
    frutos=Field(str)

class Nutrientes(Fact):
    elementos = Field(list)

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
            factor=2.2
            calculo=(rendimientoEsperado*factor)*0.34
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="Nitrato de Amonio", dosis=f"{calculo} kg/ha"))
        else:
            factor=1.8
            calculo=(rendimientoEsperado*factor)*0.46
            self.declare(Recomendacion(nutriente="Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculo} kg/ha"))
        
       
        # if 6.0 <= ph <= 7.5:
        #     self.declare(Recomendacion(fertilizante="Urea 46%", dosis=f"100 kg/ha"))
        # else:
        #     self.declare(Recomendacion(fertilizante="Fertilizante balanceado NPK", dosis="120 kg/ha"))
    


    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(raices=MATCH.raices)
          )
    def recomendar_fosforo(self,rendimientoEsperado,malezas,etapa,raices,textura):
        factor=0
        if (not("Trebol Rojo") in malezas) and (raices!="Raíces largas y fibrosas")and (etapa!="Crecimiento vegetativo" or "Desarrollo del fruto") and (textura!="franco-arcilloso"):
            factor=1.2
            calculo=(rendimientoEsperado*factor)*0.46
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="Super Fosfato Triple", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.8
            calculo=(rendimientoEsperado*factor)*0.46
            self.declare(Recomendacion(nutriente="Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculo} kg/ha"))
        

    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_potasio(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Equisetum Arvense") in malezas) and (etapa=="Crecimiento vegetativo"  or "Desarrollo del fruto") and (hojas=="Amarillamiento entre las nervaduras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=3.5
            calculo=(rendimientoEsperado*factor)*0.5
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculo} kg/ha"))
        else:
            factor=2.5
            calculo=(rendimientoEsperado*factor)*0.46
            self.declare(Recomendacion(nutriente="Potasio",fertilizante="Nitrato de potasio", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_calcio(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Achillea Millefolium" and "Taraxacum Officinale") in malezas) and (etapa!="Floración y cuajado") and (hojas!="Hojas deformadas o con manchas negras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=2.5
            calculo=(rendimientoEsperado*factor)*0.12
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="FERPAMIX PRIME", dosis=f"{calculo} kg/ha"))
        else:
            factor=2
            calculo=(rendimientoEsperado*factor)*0.03
            self.declare(Recomendacion(nutriente="Calcio",fertilizante="FERPAMIX Todo Cultivo", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango", etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_magnesio(self,rendimientoEsperado,malezas,etapa,hojas,textura):
        factor=0
        if (not("Medicago sativa") in malezas) and (etapa!="Desarrollo del fruto") and (hojas!= "Amarillentas" or "Amarillamiento entre las nervaduras") and (textura!="franco-arcilloso"):
            factor=1
            calculo=(rendimientoEsperado*factor)*0.26
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="Kieserite – Sulfato de Magnesio", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.8
            calculo=(rendimientoEsperado*factor)*0.04
            self.declare(Recomendacion(nutriente="Magnesio",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Malezas(malezas=MATCH.malezas),
          Planta(hojas=MATCH.hojas)
          )
    def recomendar_azufre(self,rendimientoEsperado,malezas,hojas,textura):
        factor=0
        if (not("Sinapis Arvensis") in malezas) and (hojas!= "Hojas deformadas o con manchas negras") and (textura!="franco-arcilloso"):
            factor=0.6
            calculo=(rendimientoEsperado*factor)*0.24
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Sulfato de Amonio", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.4
            calculo=(rendimientoEsperado*factor)*0.18
            self.declare(Recomendacion(nutriente="Azufre",fertilizante="Sulfato de Potasio", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango",etapa=MATCH.etapa,rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos)
          )
    def recomendar_boro(self,rendimientoEsperado,hojas,textura,frutos,etapa):
        factor=0
        if (frutos!="Frutos pequeños o deformes") and (etapa!="Floración y cuajado") and (hojas!= "Hojas deformadas o con manchas negras" or "Marrones o secas") and (textura!="franco-arcilloso"):
            factor=0.02
            calculo=(rendimientoEsperado*factor)*0.1
            self.declare(Recomendacion(nutriente="Boro",fertilizante="Ferpaboro", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.01
            calculo=(rendimientoEsperado*factor)*0.01
            self.declare(Recomendacion(nutriente="Boro",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos),
          Malezas(malezas=MATCH.malezas),
          )
    def recomendar_zinc(self,rendimientoEsperado,hojas,textura,frutos,malezas):
        factor=0
        if (not("Plantago Major") in malezas) and (frutos!="Frutos grandes y sanos") and (hojas!= "Verdes") and (textura!="franco-arcilloso"):
            factor=0.03
            calculo=(rendimientoEsperado*factor)*0.335
            self.declare(Recomendacion(nutriente="Zinc",fertilizante="Sulfato de Zinc Monohidratado", dosis=f"{calculo} kg/ha"))
        else:
            factor=0.02
            calculo=(rendimientoEsperado*factor)*0.02
            self.declare(Recomendacion(nutriente="Zinc",fertilizante="Ferpagrow", dosis=f"{calculo} kg/ha"))
        
    @Rule(Cultivo(tipo="Mango",rendimientoEsperado=MATCH.rendimientoEsperado),
          Suelo(textura=MATCH.textura),
          Planta(hojas=MATCH.hojas,frutos=MATCH.frutos),
          Malezas(malezas=MATCH.malezas),
          )
    def suelo_agotado(self,rendimientoEsperado,hojas,textura,malezas):
        factor=0
        if (not("Hyparrhenia Rufa") in malezas) and (hojas!= "Amarillentas" or "Amarillamiento entre las nervaduras") and (textura!="franco-arcilloso"):
            factorN=2
            factorP=1
            factorK=3
            calculoN=(rendimientoEsperado*factorN)*0.46
            calculoP=(rendimientoEsperado*factorP)*0.46
            calculoK=(rendimientoEsperado*factorK)*0.5
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculoN} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculoP} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculoK} kg/ha"))
        else:
            factorN=2
            factorP=1
            factorK=3
            calculoN=(rendimientoEsperado*factorN)*0.46
            calculoP=(rendimientoEsperado*factorP)*0.46
            calculoK=(rendimientoEsperado*factorK)*0.5
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Nitrogeno",fertilizante="Urea 46%", dosis=f"{calculoN} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Fosforo",fertilizante="Fosfato diamónico (DAP)", dosis=f"{calculoP} kg/ha"))
            self.declare(Recomendacion(nutriente="Suelo agotado, aplicar Potasio",fertilizante="Sulfato de potasio", dosis=f"{calculoK} kg/ha"))

    
    @Rule(Recomendacion(fertilizante=MATCH.fertilizante, dosis=MATCH.dosis,nutriente=MATCH.nutriente))
    def mostrar_recomendacion(self, fertilizante, dosis, nutriente):
        print(f"Deficiencia de {nutriente}, Recomendación: Aplicar {fertilizante} en una dosis de {dosis}.")


    
# Ejecución del sistema
if __name__ == "__main__":
    engine = SistemaRecomendacionFertilizantesSinAnalisis()
    engine.reset()
    
    # Declarar hechos
    engine.declare(Cultivo(tipo="Mango", etapa="Crecimiento vegetativo",rendimientoEsperado=70.0))
    engine.declare(Suelo(textura="franco-arcilloso"))
    engine.declare(Malezas(malezas=["Urtica Dioica","Chenopodium","Trebol Rojo","Equisetum Arvense"]))
    engine.declare(Hongos(hongos=["Micorrizas"]))
    engine.declare(Planta(hojas="Verdes",tallo="Tallo robusto y firme",raices="Raíces largas y fibrosas"))
    
    
    engine.declare(Suelo(textura="franco-arcilloso"))
    engine.declare(Malezas(malezas=["Urtica Dioica","Chenopodium"]))
    engine.declare(Hongos(hongos=["Micorrizas"]))
    engine.declare(Planta(hojas="Verdes"))
    
    # engine.declare(Planta(raices="Raíces largas y fibrosas"))

    # watch('RULES', 'FACTS')
    
    # Ejecutar reglas
    engine.run()




# productos_simples = {
#     "UREA 46%": {"nitrogeno": 46, "dosis_base": 100},  # Contenido de nitrógeno (%) y dosis base en kg/ha
#     "Fosfato Diamónico (DAP)": {"fosforo": 46, "nitrogeno": 18, "dosis_base": 150},
#     "Muriato de Potasio": {"potasio": 60, "dosis_base": 120},
#     "Super Fosfato Triple": {"calcio": 20, "fosforo": 46, "dosis_base": 200},
#     "Kieserite": {"magnesio": 16, "dosis_base": 100},
#     "Sulfato de Zinc Monohidratado": {"zinc": 36, "dosis_base": 50},
#     "Ferpaboro": {"boro": 20, "dosis_base": 20}
# }

# # Definimos un hecho para describir las características del cultivo
# class Cultivo(Fact):
#     tipo = Field(str, mandatory=True)  # Tipo de cultivo (ej. Mango)
#     pH = Field(float, mandatory=True)  # pH del suelo
#     textura = Field(str, mandatory=True)  # Textura del suelo
#     etapa = Field(str, mandatory=True)  # Textura del suelo
#     materia_organica = Field(float, mandatory=True)  # Porcentaje de materia orgánica
#     nitrogeno = Field(float, mandatory=True)  # Contenido de nitrógeno en mg/kg
#     fosforo = Field(float, mandatory=True)
#     potasio = Field(float, mandatory=True)
#     calcio = Field(float, mandatory=True)
#     magnesio = Field(float, mandatory=True)
#     conductividad_electrica = Field(float, mandatory=True)
#     cation_exchange_capacity = Field(float, mandatory=True)
#     # arcilla = Field(float, mandatory=True)
#     hierro = Field(float, mandatory=True)
#     manganeso = Field(float, mandatory=True)
#     zinc = Field(float, mandatory=True)
#     cobre = Field(float, mandatory=True)
#     boro = Field(float, mandatory=True)
# # Definimos un hecho para describir las características del cultivo
# class CultivoSinAnalisisSuelo(Fact):
#     tipo = Field(str)  # Tipo de cultivo (ej. Mango)
#     # etapa = Field(str, mandatory=True)  
#     hojas = Field(str)  # Porcentaje de materia orgánica
#     raices = Field(str)  # Contenido de nitrógeno en mg/kg
#     # tallo = Field(str, mandatory=True)
#     # frutos = Field(str, mandatory=True)
#     maleza = Field(list)
#     hongo = Field(list)


# # Creamos un motor de conocimiento
# class SistemaFertilizante(KnowledgeEngine):

#     @Rule(CultivoSinAnalisisSuelo(tipo=P(lambda tipo: tipo in ["Mango","Cacao"]),
#                   hojas="Verdes",
#                   maleza=P(lambda maleza:all(m in maleza for m in ["Urtica dioica", "Chenopodium"])),
#                   hongo=P(lambda hongo:["Micorrizas"]  in hongo),
#                   ))
#     def rico_nitrogeno(self):
#         print("El suelo de su cultivo tiene una buena cantidad de nitrogeno")
#         st.success("El suelo de su cultivo tiene una buena cantidad de nitrogeno")
        
#     @Rule(CultivoSinAnalisisSuelo(tipo=P(lambda tipo: tipo in ["Mango","Cacao"]),
                  
#                   hojas="Verdes",
#                   maleza=P(lambda maleza: maleza in ["Trebol Rojo"]),
#                   raices="Raíces largas y fibrosas",
#                   ))
#     def rico_fosforo(self):
#         print("El suelo de su cultivo tiene una buena cantidad de fosforo")
#         st.success("El suelo de su cultivo tiene una buena cantidad de fosforo")
        
    
#     @Rule(CultivoSinAnalisisSuelo(tipo=P(lambda tipo: tipo in ["Mango","Cacao"]),
                  
#                   hojas="Verdes",
#                   maleza=P(lambda maleza: maleza in ["Equisetum Arvense"]),
#                   raices="Raíces largas y fibrosas",
#                   ))
#     def rico_potasio(self):
#         print("El suelo de su cultivo tiene una buena cantidad de potasio")
#         st.success("El suelo de su cultivo tiene una buena cantidad de potasio")
        
    
#     @Rule(CultivoSinAnalisisSuelo(tipo=P(lambda tipo: tipo in ["Mango","Cacao"]),
                  
#                   hojas=P(lambda hojas: hojas in ["Amarillentas","Amarillamiento entre las nervaduras","Hojas deformadas o con manchas negras"]),
#                   maleza=P(lambda maleza: maleza in ["Hyparrhenia Rufa"]),
                  
#                   ))
#     def suelo_pobre(self):
#         print("El suelo tiene bajo contenido de nutrientes")
#         st.warning("El suelo tiene bajo contenido de nutrientes")
        
    

#     # @Rule(Cultivo(textura='franco'))
#     # def suelo_franco(self):
#     #     self.pH=P(lambda pH: 5.8 <= pH <= 7.0)
#     #     print(f"rango de pH para suelo franco: {self.pH}")

#     # @Rule(Cultivo(textura='franco-arcilloso'))
#     # def suelo_franco_arcilloso(self):
#     #     self.pH=P(lambda pH: 6.0 <= pH <= 7.2)
#     #     print(f"rango de pH para suelo franco-arcilloso: {self.pH}")

#     # @Rule(Cultivo(textura='arcilloso'))
#     # def suelo_arcilloso(self):
#     #     self.pH=P(lambda pH: 6.2 <= pH <= 7.4)
#     #     print(f"rango de pH para suelo arcilloso: {self.pH}")




#     # Regla para condiciones adecuadas
#     @Rule(Cultivo(tipo="Mango",
#                   pH=P(lambda pH: 5.5 <= pH <= 7.0),
#                   textura=P(lambda textura: textura in ["franco", "franco-arcilloso", "arcilloso"]),
#                   materia_organica=P(lambda mo: 2.0 <= mo <= 4.0),
#                   nitrogeno=P(lambda n: 80.0 <= n <= 200.0),
#                   fosforo=P(lambda f: 20.0 <= f <= 40.0),
#                   potasio=P(lambda k: 150.0 <= k <= 250.0),
#                   calcio=P(lambda ca: 5.0 <= ca <= 12.0),
#                   magnesio=P(lambda mg: 2.0 <= mg <= 4.5),
#                   conductividad_electrica=P(lambda ce: 0.4 <= ce <= 1.2),
#                   cation_exchange_capacity=P(lambda cec: 12 <= cec <= 30),
                  
#                   hierro=P(lambda fe: 4.5 <= fe <= 5.0),
#                   manganeso=P(lambda mn: 2.0 <= mn <= 3.0),
#                   zinc=P(lambda zn: 1.0 <= zn <= 2.0),
#                   cobre=P(lambda cu: 0.2 <= cu <= 0.5),
#                   etapa=P(lambda etapa: etapa in ["Germinación", "Plántula","Crecimiento vegetativo","Floración","Fructificación","Maduración del fruto","Senescencia"]),
#                   boro=P(lambda b: 0.5 <= b <= 1.0)))
#     def condiciones_adecuadas(self):
#         print("Las condiciones del suelo son adecuadas para el cultivo de Mango.")
#         st.success("Las condiciones del suelo son adecuadas para el cultivo de Mango.")
#         st.write("---")
#     # Reglas para parámetros inadecuados con recomendaciones
#     # @Rule(Cultivo(tipo="Mango", pH=P(lambda pH: not (5.5 <= pH <= 7.0)),textura=P(lambda textura: textura in ["franco", "franco-arcilloso", "arcilloso"])))
#     # def ph_inadecuado(self):

#     #     print("El pH del suelo no es adecuado. Debe estar entre 5.5 y 7.0.")
#     #     print("Recomendación: Aplicar enmiendas calcáreas o azufre según sea necesario.")
#     #     df.loc[len(df)] = ['Ph',ph_suelo, 'Aplicar enmiendas calcáreas o azufre según sea necesario.']

#     @Rule(Cultivo(tipo="Mango",pH=P(lambda pH: pH < 5.8 or pH > 7.4),textura=P(lambda textura: textura in ["franco", "franco-arcilloso", "arcilloso"]),materia_organica=P(lambda mo: mo < 2.0 or mo > 4.5)))
#     def calcular_cal_con_textura_y_materia_organica(self):
#         # Parámetros iniciales
#         ph_actual = ph_suelo  # Asumimos que esta variable contiene el pH actual del suelo
#         ph_objetivo = 0  # Ajustar según el cultivo
#         pureza_cal = 85  # Pureza de la cal agrícola en porcentaje

#         # Determinar el factor de corrección según el tipo de suelo
#         if textura_suelo == "franco":
#             factor_correccion = 1.0
#             ph_objetivo=6.4
#         elif textura_suelo == "franco-arcilloso":
#             factor_correccion = 1.25
#             ph_objetivo=6.6
#         elif textura_suelo == "arcilloso":
#             factor_correccion = 1.5
#             ph_objetivo=6.8
#         else:
#             print(f"Tipo de suelo desconocido: {textura_suelo}. No se puede calcular la cal.")
#             return

#         # Calcular la cantidad de cal agrícola necesaria
#         if ph_actual < 5.8:
#             cantidad_cal = ((ph_objetivo - ph_actual) / factor_correccion) * (100 / pureza_cal)
#             recomendacion_ph = f"Aplicar {cantidad_cal:.2f} toneladas de cal agrícola por hectárea para ajustar el pH a {ph_objetivo}."
#         else:
#             recomendacion_ph = "El pH está dentro del rango adecuado, no se requiere cal agrícola."

#         # Verificar la materia orgánica
#         if mo_suelo < 2.0:
#             recomendacion_mo = "El contenido de materia orgánica es bajo. Recomendación: Aplicar compost o materia orgánica adicional."
#         elif mo_suelo > 4.5:
#             recomendacion_mo = "El contenido de materia orgánica es alto. No es necesario aplicar más materia orgánica."
#         else:
#             recomendacion_mo = "El contenido de materia orgánica está en el rango adecuado."

#         # Imprimir las recomendaciones
#         print(recomendacion_ph)
#         print(recomendacion_mo)

#         # Registrar en el DataFrame
#         df.loc[len(df)] = ['pH', ph_actual, recomendacion_ph]
#         df.loc[len(df)] = ['Materia Orgánica', mo_suelo, recomendacion_mo]

#     @Rule(Cultivo(tipo="Mango",pH=P(lambda pH: pH < 5.8 or pH > 7.4),textura=P(lambda textura: textura in ["franco", "franco-arcilloso", "arcilloso"])))
#     def calcular_cal_con_textura(self):
#         # Parámetros iniciales
#         ph_actual = ph_suelo  # Asumimos que esta variable contiene el pH actual del suelo
#         ph_objetivo = 0  # Ajustar según el cultivo
#         pureza_cal = 85  # Pureza de la cal agrícola en porcentaje

#         # Determinar el factor de corrección según el tipo de suelo
#         if textura_suelo == "franco":
#             factor_correccion = 1.0
#             ph_objetivo=6.4
#         elif textura_suelo == "franco-arcilloso":
#             factor_correccion = 1.25
#             ph_objetivo=6.6
#         elif textura_suelo == "arcilloso":
#             factor_correccion = 1.5
#             ph_objetivo=6.8
#         else:
#             print(f"Tipo de suelo desconocido: {textura_suelo}. No se puede calcular la cal.")
#             return

#         # Calcular la cantidad de cal agrícola necesaria
#         if ph_actual < 5.8:
#             cantidad_cal = ((ph_objetivo - ph_actual) / factor_correccion) * (100 / pureza_cal)
#             recomendacion_ph = f"Aplicar {cantidad_cal:.2f} toneladas de cal agrícola por hectárea para ajustar el pH a {ph_objetivo}."
#         else:
#             recomendacion_ph = "El pH está dentro del rango adecuado, no se requiere cal agrícola."

#         # Verificar la materia orgánica
#         if mo_suelo < 2.0:
#             recomendacion_mo = "El contenido de materia orgánica es bajo. Recomendación: Aplicar compost o materia orgánica adicional."
#         elif mo_suelo > 4.5:
#             recomendacion_mo = "El contenido de materia orgánica es alto. No es necesario aplicar más materia orgánica."
#         else:
#             recomendacion_mo = "El contenido de materia orgánica está en el rango adecuado."

#         # Imprimir las recomendaciones
#         print(recomendacion_ph)
#         print(recomendacion_mo)

#         # Registrar en el DataFrame
#         df.loc[len(df)] = ['pH', ph_actual, recomendacion_ph]
#         df.loc[len(df)] = ['Materia Orgánica', mo_suelo, recomendacion_mo]



#     @Rule(Cultivo(tipo="Mango", textura=P(lambda textura: textura not in ["franco", "franco-arcilloso", "arcilloso"])))
#     def textura_inadecuada(self):
#         print("La textura del suelo no es adecuada. Debe ser franco, franco-arcilloso o arcilloso.")
#         print("Recomendación: Mejorar la textura con materia orgánica o enmiendas específicas.")
        
        
#         df.loc[len(df)] = ['Textura',textura_suelo, 'Mejorar la textura con materia orgánica o enmiendas específicas.']
        


#     @Rule(Cultivo(tipo="Mango", materia_organica=P(lambda mo: not (2.0 <= mo <= 4.5))))
#     def materia_organica_inadecuada(self):
#         print("El contenido de materia orgánica no es adecuado. Debe estar entre 2.0% y 4.0%.")
#         # st.warning("El contenido de materia orgánica no es adecuado. Debe estar entre 2.0% y 4.0%.")
#         print("Recomendación: Incorporar compost o estiércol bien descompuesto.")
        
        
#         df.loc[len(df)] = ['Materia organica',format(float(mo_suelo), ".2f"), 'Incorporar compost o estiércol bien descompuesto.']
        


#     @Rule(Cultivo(tipo="Mango", nitrogeno=P(lambda n: n < 80.0),textura=P(lambda textura: textura in ["franco", "franco-arcilloso", "arcilloso"]),etapa=P(lambda etapa: etapa in ["Germinación", "Plántula","Crecimiento vegetativo","Floración","Fructificación","Maduración del fruto","Senescencia"])))
#     def deficiencia_nitrogeno_suelo(self):
#         print("Deficiencia de nitrógeno detectada.")
#         # Parámetros de conversión
#         densidad_aparente = 1.0  # g/cm³ (ajustar según el tipo de suelo)
#         profundidad = 30  # cm (profundidad del muestreo
#         print("---------",self.facts[1]["etapa"],self.facts[1]["textura"])
#         #["Germinación", "Plántula","Crecimiento vegetativo","Floración","Fructificación","Maduración del fruto","Senescencia"]
#         if(self.facts[1]["textura"]=="franco"):

#             if(self.facts[1]["etapa"]=="Germinación"):
#                 nitrogeno_requerido=100 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             if(self.facts[1]["etapa"]=="Plántula"):
#                 nitrogeno_requerido=125 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             if(self.facts[1]["etapa"]=="Crecimiento vegetativo"):
#                 nitrogeno_requerido=175 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             else:
#                 nitrogeno_requerido=215 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                

#             df.loc[len(df)] = ['Nitrogeno',format(float(nitrogeno_suelo), ".1f"), f'Aplicar {cantidad:.2f} kg/ha de UREA 46%.']
        
#               # Fórmula de cálculo
#         if(self.facts[1]["textura"]=="franco-arcilloso"):

#             if(self.facts[1]["etapa"]=="Germinación"):
#                 nitrogeno_requerido=110 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             if(self.facts[1]["etapa"]=="Plántula"):
#                 nitrogeno_requerido=145 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             if(self.facts[1]["etapa"]=="Crecimiento vegetativo"):
#                 nitrogeno_requerido=195 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             else:
#                 nitrogeno_requerido=235 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                

#             df.loc[len(df)] = ['Nitrogeno',format(float(nitrogeno_suelo), ".1f"), f'Aplicar {cantidad:.2f} kg/ha de UREA 46%.']
        
#               # Fórmula de cálculo
#         if(self.facts[1]["textura"]=="arcilloso"):

#             if(self.facts[1]["etapa"]=="Germinación"):
#                 nitrogeno_requerido=120 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             if(self.facts[1]["etapa"]=="Plántula"):
#                 nitrogeno_requerido=155 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             if(self.facts[1]["etapa"]=="Crecimiento vegetativo"):
#                 nitrogeno_requerido=205 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                
#             else:
#                 nitrogeno_requerido=255 # Cantidad ideal de nitrógeno
#                 nitrogeno_actual=(nitrogeno_suelo*densidad_aparente*profundidad*0.1)
#                 deficiencia = nitrogeno_requerido - nitrogeno_actual  # Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 producto = productos_simples["UREA 46%"]  # Urea 46%
#                 cantidad = abs((deficiencia*0.25)+deficiencia / (producto["nitrogeno"] / 100))
                

#             df.loc[len(df)] = ['Nitrogeno',format(float(nitrogeno_suelo), ".1f"), f'Aplicar {cantidad:.2f} kg/ha de UREA 46%.']
        
#               # Fórmula de cálculo

#         # df.loc[len(df)] = ['Nitrogeno',format(float(nitrogeno_suelo), ".2f"), f'Aplicar {cantidad:.2f} kg/ha de UREA 46%.']
        

#     productos_fosforo = {
#         1: {"nombre": "Fosfato Diamónico (DAP)", "p_porcentaje": 46},  # P2O5 = 46%
#         2: {"nombre": "Super Fosfato Triple", "p_porcentaje": 46},  # P2O5 = 46%
#         3: {"nombre": "Ferpamix PRIME", "p_porcentaje": 20},  # P2O5 = 20%
#     }

#     @Rule(Cultivo(tipo="Mango",etapa=P(lambda etapa: etapa in ["Germinación", "Plántula","Crecimiento vegetativo","Floración","Fructificación","Maduración del fruto","Senescencia"]) ,textura=P(lambda textura: textura in ["franco", "franco-arcilloso", "arcilloso"]),fosforo=P(lambda f: not (15.0 <= f <= 70.0))))
#     def deficiencia_fosforo_suelo(self):
#         print("Deficiencia de fósforo detectada.")
        
#         # Parámetros de conversión
#         densidad_aparente = 1  # g/cm³ (ajustar según el tipo de suelo)
#         profundidad = 30  # cm (profundidad del muestreo)

#         if(self.facts[1]["textura"]=="franco"):

#             if(self.facts[1]["etapa"]=="Germinación"):
#                 fosforo_actual = ((fosforo_suelo*2.2914) * densidad_aparente * profundidad * 0.1)

#                 fosforo_requerido=7.05 # Cantidad ideal de fosforo requeriddo para 15ton
#                 deficiencia = (fosforo_requerido - fosforo_actual )*2# Deficiencia calculada
#                 # Selección del fertilizante (Urea por defecto)
#                 mejor_producto = max(self.productos_fosforo.values(), key=lambda x: x["p_porcentaje"])
#                 cantidad = deficiencia / (mejor_producto["p_porcentaje"] / 100)   # Fórmula de cálculo
            
#             df.loc[len(df)] = ['Fosforo',format(float(fosforo_suelo), ".2f"), f'Aplicar {cantidad:.2f} kg/ha de {mejor_producto['nombre']}.']


        

        
#     @Rule(Cultivo(tipo="Mango", potasio=P(lambda k: k < 150.0)))
#     def deficiencia_potasio(self):
#         print("Deficiencia de potasio detectada.")
#         # st.warning("Deficiencia de potasio detectada.")

#         print("Recomendación: Aplicar 120 kg/ha de Muriato de Potasio.")
#         # st.write("Recomendación: Aplicar 120 kg/ha de Muriato de Potasio.")
#         # st.write("---")
        
#         df.loc[len(df)] = ['Potasio',format(float(potasio_suelo), ".2f"), 'Aplicar 120 kg/ha de Muriato de Potasio.']


#     @Rule(Cultivo(tipo="Mango", calcio=P(lambda ca: ca < 5.0)))
#     def deficiencia_calcio(self):
#         print("Deficiencia de calcio detectada.")
#         st.warning("Deficiencia de calcio detectada.")
        
#         print("Recomendación: Aplicar 200 kg/ha de Super Fosfato Triple.")
#         df.loc[len(df)] = ['Calcio',format(float(calcio_suelo), ".2f"), 'Aplicar 120 kg/ha de Muriato de Potasio.']


#     @Rule(Cultivo(tipo="Mango", magnesio=P(lambda mg: mg < 2.0)))
#     def deficiencia_magnesio(self):
#         print("Deficiencia de magnesio detectada.")
#         st.warning("Deficiencia de magnesio detectada.")
        
#         print("Recomendación: Aplicar 100 kg/ha de Kieserite.")
#         df.loc[len(df)] = ['Magnesio',format(float(magnesio_suelo), ".2f"), 'Aplicar 120 kg/ha de Muriato de Potasio.']
        

#     @Rule(Cultivo(tipo="Mango", zinc=P(lambda zn: zn < 1.0)))
#     def deficiencia_zinc(self):
#         print("Deficiencia de zinc detectada.")
#         st.warning("Deficiencia de zinc detectada.")
        
#         print("Recomendación: Aplicar 50 kg/ha de Sulfato de Zinc Monohidratado.")
#         df.loc[len(df)] = ['Zinc',format(float(zinc_suelo), ".2f"), 'Aplicar 120 kg/ha de Muriato de Potasio.']
        

#     @Rule(Cultivo(tipo="Mango", boro=P(lambda b: b < 0.5)))
#     def deficiencia_boro(self):
#         print("Deficiencia de boro detectada.")
#         st.warning("Deficiencia de boro detectada.")
        
#         print("Recomendación: Aplicar 20 kg/ha de Ferpaboro.")
        

#     @Rule(Cultivo(tipo="Mango", conductividad_electrica=P(lambda ce: ce > 1.2)))
#     def conductividad_electrica_alta(self):
#         print("La conductividad eléctrica es alta, lo que puede afectar la absorción de nutrientes.")
#         st.warning("La conductividad eléctrica es alta, lo que puede afectar la absorción de nutrientes.")

#         print("Recomendación: Realizar un lavado del suelo con agua para reducir la salinidad.")
#         st.write("Recomendación: Realizar un lavado del suelo con agua para reducir la salinidad.")
#         st.write("---")
        

#     @Rule(Cultivo(tipo="Mango", cation_exchange_capacity=P(lambda cec: cec < 12)))
#     def baja_capacidad_intercambio_cationes(self):
#         print("La capacidad de intercambio catiónico es baja.")
#         st.warning("La capacidad de intercambio catiónico es baja.")
        
#         print("Recomendación: Incorporar materia orgánica para mejorar la retención de nutrientes.")
#         st.write("Recomendación: Incorporar materia orgánica para mejorar la retención de nutrientes.")
#         st.write("---")

#     # Regla compuesta para deficiencia de nitrógeno, fósforo y potasio
#     @Rule(Cultivo(tipo="Mango",
#                   nitrogeno=P(lambda n: n < 80.0),
#                   fosforo=P(lambda f: f < 40.0),
#                   potasio=P(lambda k: k < 150.0)))
#     def deficiencia_npk(self):
#         print("Deficiencia de nitrógeno, fósforo y potasio detectada.")
#         dosis_urea = 100 * (80.0 - self.facts[1]["nitrogeno"]) / 46
#         dosis_dap = 150 * (40.0 - self.facts[1]["fosforo"]) / 46
#         dosis_muriato = 120 * (150.0 - self.facts[1]["potasio"]) / 60
#         st.warning("Deficiencia de nitrógeno, fósforo y potasio detectada.")
        
#         df.loc[len(df)] = [
#             "Nitrógeno, Fósforo y Potasio",
#             f"N: {self.facts[1]['nitrogeno']:.2f}, P: {self.facts[1]['fosforo']:.2f}, K: {self.facts[1]['potasio']:.2f}",
#             f"Aplicar {dosis_urea:.2f} kg/ha de UREA, {dosis_dap:.2f} kg/ha de DAP y {dosis_muriato:.2f} kg/ha de Muriato de Potasio."
#         ]

#     # Regla compuesta para deficiencia de calcio y magnesio
#     @Rule(Cultivo(tipo="Mango",
#                   calcio=P(lambda ca: ca < 3.0),
#                   magnesio=P(lambda mg: mg < 2.0)))
#     def deficiencia_calcio_magnesio(self):
#         print("Deficiencia de calcio y magnesio detectada.")
#         dosis_superfosfato = 200 * (3.0 - self.facts[1]["calcio"]) / 20
#         dosis_kieserite = 100 * (2.0 - self.facts[1]["magnesio"]) / 16
#         st.warning("Deficiencia de calcio y magnesio detectada.")
        
#         df.loc[len(df)] = [
#             "Calcio y Magnesio",
#             f"Ca: {self.facts[1]['calcio']:.2f}, Mg: {self.facts[1]['magnesio']:.2f}",
#             f"Aplicar {dosis_superfosfato:.2f} kg/ha de Super Fosfato Triple y {dosis_kieserite:.2f} kg/ha de Kieserite."
#         ]

#     # Regla compuesta para deficiencia de todos los micronutrientes
#     @Rule(Cultivo(tipo="Mango",
#                   zinc=P(lambda zn: zn < 1.0),
#                   boro=P(lambda b: b < 0.5),
#                   magnesio=P(lambda mg: mg < 2.0)))
#     def deficiencia_micronutrientes(self):
#         print("Deficiencia de zinc, boro y magnesio detectada.")
#         dosis_zinc = 50 * (1.0 - self.facts[1]["zinc"]) / 36
#         dosis_boro = 20 * (0.5 - self.facts[1]["boro"]) / 20
#         dosis_kieserite = 100 * (2.0 - self.facts[1]["magnesio"]) / 16
#         st.warning("Deficiencia de zinc, boro y magnesio detectada.")
        
#         df.loc[len(df)] = [
#             "Zinc, Boro y Magnesio",
#             f"Zn: {self.facts[1]['zinc']:.2f}, B: {self.facts[1]['boro']:.2f}, Mg: {self.facts[1]['magnesio']:.2f}",
#             f"Aplicar {dosis_zinc:.2f} kg/ha de Sulfato de Zinc, {dosis_boro:.2f} kg/ha de Ferpaboro y {dosis_kieserite:.2f} kg/ha de Kieserite."
#         ]

#     # Regla compuesta para deficiencia severa en todos los nutrientes
#     @Rule(Cultivo(tipo="Mango",
#                   nitrogeno=P(lambda n: n < 60.0),
#                   fosforo=P(lambda f: f < 30.0),
#                   potasio=P(lambda k: k < 100.0),
#                   calcio=P(lambda ca: ca < 2.0),
#                   magnesio=P(lambda mg: mg < 1.5),
#                   zinc=P(lambda zn: zn < 0.5),
#                   boro=P(lambda b: b < 0.2)))
#     def deficiencia_severa_general(self):
#         print("Deficiencia severa en todos los nutrientes detectada.")
#         dosis_urea = 100 * (60.0 - self.facts[1]["nitrogeno"]) / 46
#         dosis_dap = 150 * (30.0 - self.facts[1]["fosforo"]) / 46
#         dosis_muriato = 120 * (100.0 - self.facts[1]["potasio"]) / 60
#         dosis_superfosfato = 200 * (2.0 - self.facts[1]["calcio"]) / 20
#         dosis_kieserite = 100 * (1.5 - self.facts[1]["magnesio"]) / 16
#         dosis_zinc = 50 * (0.5 - self.facts[1]["zinc"]) / 36
#         dosis_boro = 20 * (0.2 - self.facts[1]["boro"]) / 20
#         st.error("Deficiencia severa en todos los nutrientes detectada.")
#         st.write(f"Recomendación: Aplicar {dosis_urea:.2f} kg/ha de UREA 46%, {dosis_dap:.2f} kg/ha de Fosfato Diamónico (DAP), {dosis_muriato:.2f} kg/ha de Muriato de Potasio, {dosis_superfosfato:.2f} kg/ha de Super Fosfato Triple, {dosis_kieserite:.2f} kg/ha de Kieserite, {dosis_zinc:.2f} kg/ha de Sulfato de Zinc y {dosis_boro:.2f} kg/ha de Ferpaboro.")
#         st.write("---")
        
#         df.loc[len(df)] = [
#             "Deficiencia severa",
#             f"N: {self.facts[1]['nitrogeno']:.2f}, P: {self.facts[1]['fosforo']:.2f}, K: {self.facts[1]['potasio']:.2f}, Ca: {self.facts[1]['calcio']:.2f}, Mg: {self.facts[1]['magnesio']:.2f}, Zn: {self.facts[1]['zinc']:.2f}, B: {self.facts[1]['boro']:.2f}",
#             f"Aplicar {dosis_urea:.2f} kg/ha de UREA, {dosis_dap:.2f} kg/ha de DAP, {dosis_muriato:.2f} kg/ha de Muriato de Potasio, {dosis_superfosfato:.2f} kg/ha de Super Fosfato Triple, {dosis_kieserite:.2f} kg/ha de Kieserite, {dosis_zinc:.2f} kg/ha de Sulfato de Zinc y {dosis_boro:.2f} kg/ha de Ferpaboro."
#         ]

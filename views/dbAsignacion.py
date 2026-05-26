#se importa la libreria pymongo para realiar la conexion con la base de datos en mongoDB
import pymongo
#se usa datatime para convertir la fecha ingresada en un formato aceptable para mongoDb
from  datetime import datetime,date
from views.dbPlanificacion import cerrar_planificacion
import streamlit as st
from collections import Counter
#datos para la conexion
MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_ESPERA=1000
MONGO_BASE_DATOS="PIS"
MONGO_COLECCION="SinAnalisis"
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO
#se inicia la conexion con mongo por medio del cliente
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_ESPERA)
base_datos=cliente[MONGO_BASE_DATOS]
coleccion=base_datos[MONGO_COLECCION]
coleccion_estado=base_datos["Camion"]
#aqui se almacena los id que se encuentran en la base de datos
idEntrega=[]
#muestra los datos de la coleccion
def mostrardatos():
    try:
        for documento in coleccion.find():
            print(documento)
            #print(documento["matricula"])
        print("se ha detectado correctamente el mongo local")
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Eror, tiempo excedido"+errortiempo)

#insertar en la coleccion
def insertarAsignacion(datos):
    try:
        for documento in coleccion.find():
            idEntrega.append(documento["_id"])

        documento_nuevo={"_id":max(idEntrega)+1, #max(idEntrega)+
                   "camion":datos['camion'], 
                   "carga":datos['carga'], 
                   "fecha_hora":datetime.combine(datos['fecha_hora'][0], datos['fecha_hora'][1]), 
                   "planificacion_id":datos['planificacion_id'],
                   "estado":datos['estado']
                   
                   }
        print(documento_nuevo)
        coleccion.insert_one(documento_nuevo)
        print("se ha insertado correctamente")
        
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)

def cambio_disp_en_uso(camion):
    try:
        filtro = {'_id':int(camion)}
        print(camion)
# Actualización que se aplicará
        # actualizacion = {'$set': {'edad': 30}}

# Ejecuta la actualización
        documento_nuevo={ #max(idEntrega)+
                    '$set':{
                   "estado":"En uso"
                    }
                   
                   }
        print(documento_nuevo) 
        coleccion_estado.update_one(filtro,documento_nuevo)
        print("Se ha actualizado correctamente ✅")
        st.toast("Se ha actualizado correctamente ✅")
        #cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)

def cambio_disp_disponible(camion):
    try:
        filtro = {'_id':int(camion)}
        print(camion)
# Actualización que se aplicará
        # actualizacion = {'$set': {'edad': 30}}

# Ejecuta la actualización
        documento_nuevo={ #max(idEntrega)+
                    '$set':{
                   "estado":"disponible"
                    }
                   
                   }
        print(documento_nuevo) 
        coleccion_estado.update_one(filtro,documento_nuevo)
        print("Se ha actualizado correctamente ✅")
        st.toast("Se ha actualizado correctamente ✅")
        #cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)

def contar_recomendaciones_sin():
    try:
        recomendaciones = coleccion.count_documents({})
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Error, tiempo excedido: " + str(errortiempo))
    return recomendaciones


def consultar_asignaciones_pendientes(camion):
    try:
        for documento in coleccion.find():
             #or documento['camion']==str(camion)
            if documento['camion']==camion:
                return documento
                print(documento)
            #print(documento["matricula"])
        print("se ha detectado correctamente el mongo local")
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Eror, tiempo excedido"+errortiempo)


def actualizar_asignacion(datos):
    try:
        filtro = {'_id':datos['_id']}
        
# Actualización que se aplicará
        # actualizacion = {'$set': {'edad': 30}}

# Ejecuta la actualización
        documento_nuevo={ #max(idEntrega)+
                    '$set':{"estado":"completado",
                            "conductor":datos['conductor'],
                            "peso_saca":datos['peso_saca'],
                            "precio_saca":datos['precio_saca']
                   }}
        
        print(datos['_id']) 
        coleccion.update_one(filtro,documento_nuevo, upsert=True)
        cerrar_planificacion(datos['_id'])
        print("Se ha completado la asignación ✅")
        st.toast("Se ha completado la asignación 🎉")
        #cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)


def promedio():
    total_carga=[]
    try:
        for documento in coleccion.find():
            if documento['estado']=='completado':
                total_carga.append(documento['carga'])
            print(total_carga)
        promedio=sum(total_carga)/len(total_carga)
            #print(documento["matricula"])
        print("se ha detectado correctamente el mongo local")
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Eror, tiempo excedido"+errortiempo)
    return promedio




def obtener_carga_por_mes():
    camiones_ids=[]
    for documento in coleccion_estado.find():
        camiones_ids.append(documento['_id'])
    # Crear el pipeline de agregación
    pipeline = [
        {
            "$match": {
                "camion": {"$in": camiones_ids}
            }
        },
        {
            "$group": {
                "_id": {
                    "camion": "$camion",
                    "mes": {"$month": "$fecha_hora"},
                    "anio": {"$year": "$fecha_hora"}
                },
                "carga_total": {"$sum": "$carga"}
            }
        },
        {
            "$sort": {"_id.camion": 1, "_id.anio": 1, "_id.mes": 1}
        }
    ]

    # Ejecutar el pipeline de agregación
    resultado = coleccion.aggregate(pipeline)

    # Almacenar los resultados en un diccionario
    cargas_por_camion = {}
    for entry in resultado:
        camion = entry["_id"]["camion"]
        mes = entry["_id"]["mes"]
        anio = entry["_id"]["anio"]
        carga_total = entry["carga_total"]

        # Inicializar el diccionario para el camión si no existe
        if camion not in cargas_por_camion:
            cargas_por_camion[camion] = {}

        # # Almacenar la carga total por mes y año
        # if anio not in cargas_por_camion[camion]:
        #     cargas_por_camion[camion][anio] = {}
        
        cargas_por_camion[camion] = carga_total

    return cargas_por_camion



def maleza_mas_frecuente():
    try:
        # Conectar a la base de datos
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cliente["PIS"]
        coleccion = db["SinAnalisis"]

        # Recopilar todas las malezas
        todas_malezas = []
        for documento in coleccion.find():
            if 'malezas' in documento:
                todas_malezas.extend(documento['malezas'])

        # Contar la frecuencia de cada maleza
        conteo_malezas = Counter(todas_malezas)

        # Encontrar la maleza que más se repite
        maleza_comun = conteo_malezas.most_common(1)
        if maleza_comun:
            nombre_maleza, frecuencia = maleza_comun[0]
            print(f"La maleza más frecuente es '{nombre_maleza}' con {frecuencia} apariciones.")
        else:
            print("No se encontraron malezas en los documentos.")

    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Error, tiempo excedido: " + str(errortiempo))

    return nombre_maleza
# Llamar a la función y mostrar el resultado

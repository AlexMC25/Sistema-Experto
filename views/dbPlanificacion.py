#se importa la libreria pymongo para realiar la conexion con la base de datos en mongoDB
import pymongo
#se usa datatime para convertir la fecha ingresada en un formato aceptable para mongoDb
from  datetime import datetime,date
import streamlit as st
#datos para la conexion
MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_ESPERA=1000
MONGO_BASE_DATOS="PIS"
MONGO_COLECCION="ConAnalisis"
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO
#se inicia la conexion con mongo por medio del cliente
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_ESPERA)
base_datos=cliente[MONGO_BASE_DATOS]
coleccion=base_datos[MONGO_COLECCION]
coleccion_asignacion=base_datos['Asignacion']
#aqui se almacena los id que se encuentran en la base de datos
idPlanificacion=[]
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


if 'id_planificacion' not in st.session_state:
    st.session_state.id_planificacion =0

#insertar en la coleccion
def insertarPlanificacion(datos):
    try:
        for documento in coleccion.find():
            idPlanificacion.append(documento["_id"])
        id=max(idPlanificacion)+1
        documento_nuevo={"_id":id, #max(idEntrega)+
                   "fecha":datetime.combine(datos['fecha'],datetime.min.time()),
                   "cantidad_entregar":datos['cantidad_entregar'], 
                   "destino":datos['destino'], 
                   "estado":datos['estado'],
                   }
        st.session_state.id_planificacion=id
        print(documento_nuevo)
        coleccion.insert_one(documento_nuevo)
        print("se ha insertado correctamente")
        #cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)

def eliminar_ultima_planificacion(id):
    try:
        
        filtro = {'_id': id}

# Actualización que se aplicará
        # actualizacion = {'$set': {'edad': 30}}
        #print(documento_nuevo) 
        coleccion.delete_one(filtro)
        print("Se ha actualizado correctamente ✅")
        st.toast("Se ha eliminado correctamente ✅")
        #cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)


def cerrar_planificacion(id_asignacion):
    
    try:
        for documento in coleccion_asignacion.find():
            if documento['_id']==id_asignacion and documento['estado']=='completado':
                for documento_planificado in coleccion.find():
                    if documento['planificacion_id']==documento_planificado['_id']:
                        filtro = {'_id':documento['planificacion_id']}
                        documento_nuevo={'$set':{"estado":"completado",}}

                        coleccion.update_one(filtro,documento_nuevo, upsert=True)
                        print('planificado '+documento_planificado['estado'])
                        # documento_planificado['estado']='completado'

                print(documento)
            #print(documento["matricula"])
        print("se ha detectado correctamente el mongo local")
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Eror, tiempo excedido"+errortiempo)

def cliente_mas_frecuente():
    cliente_frecuente = []
    try:
        for documento in coleccion.find():
            if documento['propietario'] is not None:
                cliente_frecuente.append(documento['propietario'])
        
        # Encontrar propietarios repetidos
        repetidos = encontrar_repetidos(cliente_frecuente)
        print("Propietarios repetidos:", repetidos)
        
        print("se ha detectado correctamente el mongo local")
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Error, tiempo excedido: " + str(errortiempo))

    return cliente_frecuente[0]



def encontrar_repetidos(lista):
    # Crear un diccionario para contar las ocurrencias
    conteo = {}
    for elemento in lista:
        if elemento in conteo:
            conteo[elemento] += 1
        else:
            conteo[elemento] = 1
    
    # Encontrar elementos repetidos
    repetidos = [elemento for elemento, cuenta in conteo.items() if cuenta > 1]
    
    return repetidos

def contar_recomendaciones():
    try:
        recomendaciones = coleccion.count_documents({})
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Error, tiempo excedido: " + str(errortiempo))
    return recomendaciones

def consultar_ciudad_asignaciones():
        # Consulta para obtener todos los documentos con estado "completado"
    resultados = coleccion.find({"estado": {"$in": ["completado", "pendiente"]}})

    # Crear un diccionario para contar las repeticiones de cada ciudad
    ciudades_contador = {}

    for resultado in resultados:
        ciudad = resultado["destino"]
        if ciudad in ciudades_contador:
            ciudades_contador[ciudad] += 1
        else:
            ciudades_contador[ciudad] = 1


    return ciudades_contador


cliente_mas_frecuente()
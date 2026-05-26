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
MONGO_COLECCION="Cosechadora"
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO
#se inicia la conexion con mongo por medio del cliente
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_ESPERA)
base_datos=cliente[MONGO_BASE_DATOS]
coleccion=base_datos[MONGO_COLECCION]
#aqui se almacena los id que se encuentran en la base de datos
idCosechadora=[]
#muestra los datos de la coleccion
def mostrarCosechadoras():
    try:
        for documento in coleccion.find():
            print(documento)
            #print(documento["matricula"])
        print("se ha detectado correctamente el mongo local")
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Eror, tiempo excedido"+errortiempo)

#insertar en la coleccion
def insertarCosechadora(datos):
    try:
        for documento in coleccion.find():
            idCosechadora.append(documento["_id"])

        documento_nuevo={"_id":max(idCosechadora)+1, #max(idEntrega)+
                   "conductor":datos['conductor'],
                   "capacidad_tolva":datos['capacidad_tolva'], 
                   "estado":'disponible', 
                   "observacion":'',
                   
                   
                   }
        print(documento_nuevo)
        coleccion.insert_one(documento_nuevo)
        st.toast('Se ha insertado correctamente ✅')
        print("se ha insertado correctamente")
        #cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)

#actualizar en la coleccion
def actualizarCosechadora(datos):
    try:
        for documento in coleccion.find():
            idCosechadora.append(documento["_id"])

        filtro = {'_id': datos['_id']}

# Actualización que se aplicará
        # actualizacion = {'$set': {'edad': 30}}

# Ejecuta la actualización
        documento_nuevo={ #max(idEntrega)+
                    '$set':{
                   "conductor":datos['conductor'],
                   "capacidad_tolva":datos['capacidad_tolva'], 
                   "estado":datos['estado'], 
                   "observacion":datos['observacion'],
                    }
                   
                   }
        print(documento_nuevo) 
        coleccion.update_one(filtro,documento_nuevo)
        print("Se ha actualizado correctamente ✅")
        st.toast("Se ha actualizado correctamente ✅")
        #cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)

def eliminarCosechadora(datos):
    try:
        for documento in coleccion.find():
            idCosechadora.append(documento["_id"])

        filtro = {'_id': datos['_id']}

# Actualización que se aplicará
        # actualizacion = {'$set': {'edad': 30}}
        #print(documento_nuevo) 
        coleccion.delete_one(filtro)
        print("Se ha actualizado correctamente ✅")
        st.toast("Se ha eliminado correctamente ✅")
        #cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)

def disponibilidadCosechadora():
    disponibles={}
    try:
        for documento in coleccion.find():
            if documento['estado']=='disponible':
                disponibles={'_id':documento['_id'],
                            'estado':documento['estado']
                            }
            #print(disponibles)
            #print(documento["matricula"])
        print("se ha detectado correctamente el mongo local")
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Eror, tiempo excedido"+errortiempo)
    return disponibles


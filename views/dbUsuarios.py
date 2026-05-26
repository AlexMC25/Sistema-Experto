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
MONGO_COLECCION="Usuarios"
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO
#se inicia la conexion con mongo por medio del cliente
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_ESPERA)
base_datos=cliente[MONGO_BASE_DATOS]
coleccion=base_datos[MONGO_COLECCION]
#aqui se almacena los id que se encuentran en la base de datos
idEntrega=[]
#muestra los datos de la coleccion
usuario={}

def mostrardatos():
    try:
        for documento in coleccion.find():
            usuario['_id']=documento['_id']
            usuario['email']=documento['email']
            usuario['failed_login_attempts']=documento['failed_login_attempts']
            usuario['logged_in']=documento['logged_in']
            usuario['name']=documento['name']
            usuario['password']=documento['password']

            print(usuario)
            #print(documento["matricula"])
        print("se ha detectado correctamente el mongo local")
    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        print("Eror, tiempo excedido"+errortiempo)

    return usuario

#cliente.close()

mostrardatos()

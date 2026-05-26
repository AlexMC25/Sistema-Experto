#se importa la libreria pymongo para realiar la conexion con la base de datos en mongoDB
import pymongo
#se usa datatime para convertir la fecha ingresada en un formato aceptable para mongoDb
from  datetime import datetime,date

#datos para la conexion
MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_ESPERA=1000
MONGO_BASE_DATOS="PIS"
MONGO_COLECCION="Traslado"
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO
#se inicia la conexion con mongo por medio del cliente
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_ESPERA)
base_datos=cliente[MONGO_BASE_DATOS]
coleccion=base_datos[MONGO_COLECCION]
#aqui se almacena los id que se encuentran en la base de datos
idTranslado=[]
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
def insertarTraslado(datos):
    try:
        for documento in coleccion.find():
            idTranslado.append(documento["_id"])

        documento_nuevo={"_id":max(idTranslado)+1, #max(idEntrega)+
                   "chofer":datos['chofer'], 
                   "matricula":datos['matricula'], 
                   "destino":datos['destino'],
                   "n_cargas":datos['n_cargas'],
                   "tasa":datos['tasa'],
                   "fechaHora": datetime.combine(datos['fecha'], datetime.min.time())
                   #"fechaHora":datetime.date(datos['fecha'])
                   }
        print(datos['fecha'])
        coleccion.insert_one(documento_nuevo)
        print("se ha insertado correctamente")
        cliente.close()
    except pymongo.errors.OperationFailure as errorinsertar:
        print("Error, al insertar"+errorinsertar)

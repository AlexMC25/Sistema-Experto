import pymongo
import streamlit as st
import streamlit.components.v1 as components
import os

def obtener_productos():
    try:
        # Conectar a la base de datos
        cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        db = cliente["PIS"]
        coleccion = db["Productos"]

        # Recuperar el documento que contiene la información de los productos
        documento = coleccion.find_one({"_id": 1})

        if documento:
            productos_simples = documento.get("productos_simples", {})
            productos_ferpamix = documento.get("productos_ferpamix", {})
            productos_ferpamix_LC = documento.get("productos_ferpamix_LC", {})
            productos_especializados = documento.get("productos_especializados", {})

            return {
                "productos_simples": productos_simples,
                "productos_ferpamix": productos_ferpamix,
                "productos_ferpamix_LC": productos_ferpamix_LC,
                "productos_especializados": productos_especializados
            }
        else:
            st.error("No se encontró el documento con _id 1.")
            return {}

    except pymongo.errors.ServerSelectionTimeoutError as errortiempo:
        st.error("Error, tiempo excedido: " + str(errortiempo))
        return {}

def mostrar_productos_en_cards(productos, titulo, subcarpeta):
    st.write(f"### {titulo}")
    for key, producto in productos.items():
        # Ruta de la imagen del producto
        nombre_imagen = producto['nombre'].replace(" ", "_").replace("%", "").replace("(", "").replace(")", "") + ".jpg"
        ruta_imagen = os.path.join("productos\\fertilizantes", subcarpeta, nombre_imagen)
        # HTML de la tarjeta con la imagen
        card_html = f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin: 10px 0;">
            
            <h4>{producto['nombre']}</h4>
            {st.image(f"{ruta_imagen}",width=200)}
            <p><strong>Fórmula:</strong> {producto['Formula']}</p>
            <p><strong>Presentación:</strong> {producto['Presentacion kg']} kg</p>
            <p><strong>Características:</strong> {producto['Características']}</p>
            <div style="display: flex; justify-content: space-between;">
                <button onclick="window.location.href='/editar?producto={key}'">Editar</button>
                <button onclick="window.location.href='/eliminar?producto={key}'">Eliminar</button>
            </div>
        </div>
        """
        components.html(card_html, height=400)

# Llamar a la función y mostrar los productos
productos = obtener_productos()

if productos:
    mostrar_productos_en_cards(productos["productos_simples"], "Productos Simples", "productos_simples")
    mostrar_productos_en_cards(productos["productos_ferpamix"], "Productos FERPAMIX", "productos_ferpamix")
    mostrar_productos_en_cards(productos["productos_ferpamix_LC"], "Productos FERPAMIX LC", "productos_ferpamix_LC")
    mostrar_productos_en_cards(productos["productos_especializados"], "Productos Especializados", "productos_especializados")
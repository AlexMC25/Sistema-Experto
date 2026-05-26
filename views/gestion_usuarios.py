import streamlit as st
import pandas as pd

# Crear un diccionario de usuarios
usuarios = {
    "jcox": {
        "email": "dbaldwin@gmail.com",
        "estado": False,
        "name": "David Baldwin",
        "password": "def321"
    },
    "acox": {
        "email": "jsmith@gmail.com",
        "estado": True,
        "name": "Alex Magallanes",
        "password": "abc123",
        "rol": "administrador"
    },
    "luisz": {
        "email": "rbriggs@gmail.com",
        "estado": True,
        "name": "Luis Zambrano",
        "password": "def123",
        "rol": "conductor"
    },
    "klevers": {
        "email": "rcouper@gmail.com",
        "estado": False,
        "name": "Klever Sarmiento",
        "password": "qwe123"
    },
    "marcelos": {
        "email": "wedw@ew.com",
        "estado": False,
        "name": "Marcelo San Lucas",
        "password": "ewq123"
    }
}

# Convertir el diccionario a un DataFrame de Pandas
df = pd.DataFrame(usuarios).T

# Cambiar los títulos de las columnas
df = df.rename(columns={
    "email": "Correo Electrónico",
    "estado": "Estado Activo",
    "name": "Nombre",
    "password": "Contraseña",
    "rol": "Rol"
})

# Restablecer el índice del DataFrame para no mostrar el índice original
df.reset_index(drop=True, inplace=True)

# Mostrar la tabla con st.dataframe
st.title("Gestión de usuarios")
st.subheader("Lista de Usuarios")

# Mostrar el DataFrame sin el índice
st.markdown(df.to_html(index=False), unsafe_allow_html=True)

# Crear un selectbox para elegir un usuario
usuario_seleccionado = st.selectbox("Selecciona un usuario:", df['Nombre'])

# Obtener los datos del usuario seleccionado
usuario_data = df[df['Nombre'] == usuario_seleccionado].iloc[0]

# Mostrar inputs para modificar los valores del usuario seleccionado
with st.form(key='modificar_usuario'):
    email = st.text_input("Correo Electrónico", value=usuario_data['Correo Electrónico'])
    estado = st.selectbox("Estado Activo", options=[True, False], index=int(usuario_data['Estado Activo']))
    contraseña = st.text_input("Contraseña", value=usuario_data['Contraseña'], type="password")
    rol = st.text_input("Rol", value=usuario_data['Rol'] if 'Rol' in usuario_data else '')

    # Botón para enviar cambios
    submit_button = st.form_submit_button("Modificar Usuario")

# Botón para eliminar el usuario seleccionado
if st.button("Eliminar Usuario"):
    # Eliminar del diccionario usando el nombre del usuario seleccionado
    usuario_clave = df[df['Nombre'] == usuario_seleccionado].index[0]  # Obtener la clave del diccionario
    del usuarios[usuario_clave]

    # Volver a crear el DataFrame con los datos actualizados
    df = pd.DataFrame(usuarios).T
    df = df.rename(columns={
        "email": "Correo Electrónico",
        "estado": "Estado Activo",
        "name": "Nombre",
        "password": "Contraseña",
        "rol": "Rol"
    })
    df.reset_index(drop=True, inplace=True)

    # Mostrar el DataFrame actualizado
    st.markdown(df.to_html(index=False), unsafe_allow_html=True)
    st.success(f"Usuario {usuario_seleccionado} eliminado con éxito.")

if submit_button:
    # Actualizar el diccionario de usuarios
    clave_usuario = df[df['Nombre'] == usuario_seleccionado].index[0]  # Obtener la clave del diccionario
    usuarios[clave_usuario]['email'] = email
    usuarios[clave_usuario]['estado'] = estado
    usuarios[clave_usuario]['password'] = contraseña
    if 'Rol' in usuarios[clave_usuario]:
        usuarios[clave_usuario]['rol'] = rol

    # Volver a crear el DataFrame con los datos actualizados
    df = pd.DataFrame(usuarios).T
    df = df.rename(columns={
        "email": "Correo Electrónico",
        "estado": "Estado Activo",
        "name": "Nombre",
        "password": "Contraseña",
        "rol": "Rol"
    })
    df.reset
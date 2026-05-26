import streamlit as st
import streamlit_authenticator as stauth
from Menu_camion import menu_camion
import base64
from Menu import menu


#configuracion de la pagina
#st.set_page_config(page_title="Sistema Web",page_icon="🌾",layout="centered")

usuarios={
    "cookie": {
        "expiry_days": 1,
        "key": "some_signature_key",
        "name": "some_cookie_name"
    },
    "credentials": {
        "usernames": {
            "jcox": {
                "email": "dbaldwin@gmail.com",
                "failed_login_attempts": 0,
                "logged_in": False,
                "name": "David Baldwin",
                "password": "def321"
            },
            "acox": {
                "email": "jsmith@gmail.com",
                "failed_login_attempts": 0,
                "logged_in": True,
                "name": "Alex Magallanes",
                "password": "abc123",
                "rol":"administrador"
            },
            "luisz": {
                "email": "rbriggs@gmail.com",
                "failed_login_attempts": 0,
                "logged_in": True,
                "name": "Luis Zambrano",
                "password": "def123",
                "rol":"conductor"
            },
            "klevers": {
                "email": "rcouper@gmail.com",
                "failed_login_attempts": 0,
                "logged_in": False,
                "name": "Klever Sarmiento",
                "password": "qwe123"
            },
            "marcelos": {
                "email": "wedw@ew.com",
                "failed_login_attempts": 0,
                "logged_in": False,
                "name": "Marcelo San Lucas",
                "password": "ewq123"
            }
        }
    },
    "pre-authorized": {
        "emails": ["melsby@gmail.com"]
    }
}
# Crear el objeto Authenticator
authenticator = stauth.Authenticate(
    usuarios['credentials'],
    usuarios['cookie']['name'],
    usuarios['cookie']['key'],
    usuarios['cookie']['expiry_days'],
    usuarios['pre-authorized']
)



#variable que cambia el texto de boton
texto_boton_olvide="Olvide mi contraseña"
texto_boton_nuevo="Registrarse"

#restablecer clave
# Inicializar una variable de estado para controlar la visibilidad del widget
if 'olvide_clave' not in st.session_state:
    st.session_state.olvide_clave = False

if 'btn_olvide_clave' not in st.session_state:
    st.session_state.btn_olvide_clave = False

if 'btn_nuevo_usuario' not in st.session_state:
    st.session_state.btn_nuevo_usuario = False

# Inicializar el estado de la sesión para controlar si el botón está deshabilitado
if 'btn_nuevo_usuario_des' not in st.session_state:
    st.session_state.btn_nuevo_usuario_des = False

# Inicializar el estado de la sesión para controlar si el botón está deshabilitado
if 'btn_olvide_clave_des' not in st.session_state:
    st.session_state.btn_olvide_clave_des = False

# Inicializar el estado de la sesión para controlar la visibilidad del contenedor
if 'mostrar_contenedor_botones' not in st.session_state:
    st.session_state.mostrar_contenedor_botones = False


#regstrar nuevo usuario
# Inicializar una variable de estado para controlar la visibilidad del widget
if 'nuevo_usuario' not in st.session_state:
    st.session_state.nuevo_usuario = False

# Función para alternar la visibilidad del widget
def  mostrar_olvide_contraseña():
    st.session_state.olvide_clave = not st.session_state.olvide_clave
    st.session_state.btn_nuevo_usuario_des = not st.session_state.btn_nuevo_usuario_des

# Función para alternar la visibilidad del widget
def  mostrar_nuevo_usuario():
    st.session_state.nuevo_usuario = not st.session_state.nuevo_usuario
    st.session_state.btn_olvide_clave_des = not st.session_state.btn_olvide_clave_des


#funcion para restablecer clave
def restablecer_clave():
    try:
        username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(fields={'Form name':'Olvide contraseña', 'Username':'Nombre de usuario', 'Submit':'Enviar'})
        if username_of_forgotten_password:
            st.success('Nueva clave generada con exito!')
            print(new_random_password )
            # The developer should securely transfer the new password to the user.
        elif username_of_forgotten_password == False:
            st.error('Nombre de usuario no existe')
    except Exception as e:
        st.error(e)

if 'titulo_hacienda' not in st.session_state:
    st.session_state.titulo_hacienda = False

def mostrar_titulo():
    
            #st.image("./logofer.png",use_column_width=True)
    
    st.session_state.titulo_hacienda = not st.session_state.titulo_hacienda
#funcion que genera el inicio de sesion
def get_img_as_base64(file):
    with open(file,"rb") as f:
        data=f.read()
    return base64.b64encode(data).decode()

img=get_img_as_base64("logofer.png")
def inicio_sesion():
    st.session_state.mostrar_contenedor_botones=True
    with st.container():
        col1,col2,col3=st.columns([3,6,1],vertical_alignment="center",gap="large")
        with col2:
            st.title("  :blue[Ferpacific] 🍫🥭")
                  
    name,authentication_status,username=authenticator.login(location="main",fields={'Form name':'Inicio de sesión', 'Username':'Usuario 👤', 'Password':'Contraseña #️⃣', 'Login':'Ingresar'},clear_on_submit=True)
    #variable para msotrar o ocultar contenedor de botones
    
    if st.session_state["authentication_status"]:
        if username!='acox':
            menu_camion()
        else:
            menu()
        with st.sidebar:
            st.write(f'Bienvenido *{st.session_state["name"]}*')
            
            
            authenticator.logout(button_name="Salir")
            
            
    elif st.session_state["authentication_status"] is False:
        st.error('usuario/contraseña incorrecto')
    elif st.session_state["authentication_status"] is None:
        
        st.warning('Por favor ingrese usuario y contraseña')
    
    


#funcion para registrar un nuevo usuario
def registrar_nuevo():
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False,fields={'Form name':'Registrar Usuario', 'Name':'Nombre 👤','Username':'Usuario 👤', 'Password':'Contraseña #️⃣', 'Email':'Correo','Repeat password':'Repetir Contraseña #️⃣','Register':'Registrar'},clear_on_submit=True)
        if email_of_registered_user:
            st.success('Usuario registrado con exito!')
    except Exception as e:
        st.error(e)

# Condicional para mostrar u ocultar el widget
if st.session_state.olvide_clave:
    restablecer_clave()
    texto_boton_olvide="Ir a inicio de sesión"
# Condicional para mostrar u ocultar el widget
elif st.session_state.nuevo_usuario:
    registrar_nuevo()
    texto_boton_nuevo="Ir a inicio de sesión"
else:
    inicio_sesion()
    texto_boton_olvide="Olvide mi contraseña"



#contenedores de los botones

izquierda,centro,derecha=st.columns(3,gap="small")
contenedor_botones = st.container(height=300,border=False)

if st.session_state.mostrar_contenedor_botones:
    with contenedor_botones:
        with izquierda:
            # Botón para alternar la visibilidad
            st.button(texto_boton_olvide, on_click=mostrar_olvide_contraseña,key='btn_olvide_clave',use_container_width=True,help="Quieres un nueva clave?",disabled=st.session_state.btn_olvide_clave_des)
        

        with derecha:
            # Botón para alternar la visibilidad
            
            st.button(texto_boton_nuevo, on_click=mostrar_nuevo_usuario,key='btn_nuevo_usuario',use_container_width=True,help="Tienes cuenta?",disabled=st.session_state.btn_nuevo_usuario_des)





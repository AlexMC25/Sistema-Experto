import google.generativeai as genai
import streamlit as st
#clave para conectarse con gemini
genai.configure(api_key="AIzaSyA2Q6W-c3MGxACZKk_XOi-5oSlxKs6CRSg")
model = genai.GenerativeModel('gemini-1.5-flash')
business_context = """
Eres un asistente virtual para un sistema web de registro de distribución de arroz que se encarga de planificar diferentes entregas de arroz en cascara recien cosechado por toneladas, que son transportadas en camiones. 
El sistema se especializa en crear una planificación de distribución para diferentes destinos.
El sistema posee varios modulos: un modulo de dashboard, un modulo de reporte, modulo de planificacion, un modulo de asignacion, y modulo denominado camiones , un modulo denominado cosechadoras, un modulo de chatbot.
El modulo dasboard muestra indicadores kpi y grafico con los valores de la cosecha y los camiones.
El modulo de reporte es donde se visualizan diferentes tablas que contienen informacion como:las planificaciones realizadas y su estado de completado o incompleto, los camiones disponibles y ocupados y sus demas datos,las cosechadoras disponibles y ocupadas y sus demas datos, las asignaciones de camiones creadas a partir de la planificacion a la que esten referenciada sus demas datos.
El modulo de planificacion es donde se ingresan datos como la fecha, la cantidad planificada a entregar y el destino a donde se debe llevar la carga y la cantidad de toneladas a entregar.
Dentro del modulo de planificacion esta el modulo de asignacion de camiones que distribuyen el arroz por toneladas, aqui se escoge a los camiones disponibles y se le asigna una carga a transportar no mayor a su capacidad de carga y la cantidad planificada anteriormente, al darc click en asignar se crea una asignacion para los camiones.
Dentro del modulo camiones se puede añadir un nuevo camion o editar los datos de un camion ya registrado.
Dentro del modulo cosechadoras se puede añadir una nueva cosechadora o actualizar una ya existente.
El modulo chatbot da respuestas referentes a la cosecha de arroz y el sistema web.
Los camiones poseen un modulo adicional donde solo interactuan ellos, en ese modulo ellos pueden visualizar los datos de la asignacion que poseen ellos y marcarla como terminada, y esto modifica la informacion de la planificacion y la marca como completada.
Para ingresar al sistema se necesita inicar sesión con clave y usuario.

Algunas preguntas frecuentes que podrías recibir son:
1. ¿Cuantos modulos posee el sistema?
2. ¿Qué datos se pueden ingresar por cada modulo?
3. ¿Que informacion posee el dashboard?
4. ¿Como funciona la planificacion y la asignacion?


Responde siempre en base a la información anterior y asegúrate de dar respuestas que sean precisas y alineadas con la filosofía del negocio.
"""

# Función para crear el chatbot/vista
def chat():
    st.title('Asistente Virtual 🤖')

    # Inicializa la sesión si no está ya inicializada
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "first_message" not in st.session_state:
        st.session_state.first_message = True

    # Muestra los mensajes almacenados
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Envía el primer mensaje del asistente si es la primera vez
    if st.session_state.first_message:
        assistant_message = "Hola, ¿Cómo puedo ayudarte?"
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        st.session_state.first_message = False

    # Captura el input del usuario
    if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

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

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        


# chat()
# #para imprimir por consola
#     # while(True):
#     #     pregunta=input("Usuario: ")
#     #     if(pregunta=="-1"):
#     #         exit()
#     #     else:
            
#     #         response = model.generate_content(pregunta)
#     #         print(f'Gemini: {response.text}')
        
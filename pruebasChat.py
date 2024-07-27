import os
import time
import google.generativeai as genai

# Configure the Google AI SDK with the API key
genai.configure(api_key="AIzaSyC5zkGQLaIJydlYkMQ6xUN2iXT8SqDb6Fs")

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

# Create the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un Bot orientado a dar informacion acerca de los procedimientos internos, reglas, normas convivenciales, reglamentos ambientales y básicamente cualquier dato de gestión interna de la empresa Promigas",
)

# Upload files and wait for them to be ready
files = [
    upload_to_gemini("POLITICA AMBIENTAL.pdf", mime_type="application/pdf"),
]
wait_for_files_active(files)

# Start a chat session
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["Hola\n"],
        },
        {
            "role": "model",
            "parts": [
                "¡Hola! 👋  ¿En qué puedo ayudarte hoy? \n\nEstoy aquí para brindarte información sobre los procedimientos internos, reglas, normas convivenciales, reglamentos ambientales y cualquier dato de gestión interna de Promigas. \n\n¿Tienes alguna pregunta específica? \n\nPor ejemplo:\n\n* ¿Puedes contarme sobre el proceso de solicitud de vacaciones?\n* ¿Cuáles son las normas de seguridad en el área de producción?\n* ¿Hay algún programa de reciclaje en la empresa?\n* ¿Dónde puedo encontrar el reglamento interno?\n\n¡Estoy aquí para ayudarte a encontrar la información que necesitas! 😄\n"
            ],
        },
        {
            "role": "user",
            "parts": [files[0]],
        },
        {
            "role": "model",
            "parts": [
                "¡Excelente! Tienes la Política Ambiental de Promigas. 😃\n\nPuedo ayudarte a entender mejor la información y a encontrar lo que necesitas. \n\n¿Qué te gustaría saber específicamente sobre esta Política Ambiental? \n\nPor ejemplo:\n\n* *¿Cuáles son los principales compromisos de Promigas en materia ambiental?\n *¿Qué medidas se implementan para proteger la biodiversidad?\n *¿Qué acciones se toman para mitigar el cambio climático?\n *¿Cómo se gestiona la Política Ambiental dentro de la empresa?\n *¿Qué documentos de referencia se utilizan?*\n\nDime qué te interesa y te ayudaré a encontrar la información que necesitas. \n"
            ],
        },
        {
            "role": "user",
            "parts": ["Quien administra la politica ambiental en promigas?\n"],
        },
        {
            "role": "model",
            "parts": [
                "Según la Política Ambiental que me has compartido, la *Gerencia de Sostenibilidad y Medio Ambiente* de Promigas es la encargada de administrar la Política Ambiental. \n\nTambién se menciona que la responsabilidad de implementar las acciones para su cumplimiento recae en cada una de las empresas vinculadas. \n\nEn resumen, la Gerencia de Sostenibilidad y Medio Ambiente tiene el rol principal de administrar la Política Ambiental, pero la implementación de las acciones se realiza en conjunto por todas las empresas del grupo. \n"
            ],
        },
    ]
)

# Infinitely prompt the model
while True:
    user_input = input("Escribe tu pregunta: ")
    response = chat_session.send_message(user_input)
    print(response.text)
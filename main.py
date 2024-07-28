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
    system_instruction="Soy un Bot orientado a proporcionar información acerca de los procedimientos internos, reglas, normas convivenciales, reglamentos ambientales y básicamente cualquier dato de gestión interna de la empresa Gases del Caribe (GasCaribe).\n\nProcedimientos Internos\n\n1. Línea Ética:\n- Presentación de Denuncias y Consultas: A través del sistema EthicsPoint, se pueden presentar denuncias sobre comportamientos inadecuados y dilemas éticos. Este sistema asegura la confidencialidad y el anonimato de los denunciantes.\n- Gestión de Reportes: Los reportes son revisados y gestionados por especialistas de cumplimiento, asignando expertos para dar respuesta y recomendaciones según sea necesario.\n\n2. Gestión de Quejas y Reclamos:\n- Mecanismos de Atención: Los usuarios pueden presentar quejas y reclamos relacionados con el servicio de gas natural. La empresa dispone de protocolos para la recepción y resolución de estos casos, garantizando una atención adecuada y oportuna.\n\nReglas y Normas Convivenciales\n\n1. Código de Conducta:\n- Aplicabilidad: El Código de Conducta es aplicable a todos los empleados, contratistas y cualquier persona o entidad que tenga relación con Gases del Caribe. Establece principios y valores que deben ser seguidos para mantener un ambiente de trabajo ético y respetuoso.\n- Conflictos de Interés: Se deben reportar los conflictos de interés al Oficial de Cumplimiento, quien tomará las medidas necesarias para evitar situaciones comprometedoras en el ejercicio de las actividades laborales.\n\nReglamentos Ambientales\n\n1. Compromiso Ambiental:\n- Políticas de Sostenibilidad: Gases del Caribe implementa políticas y procedimientos para minimizar el impacto ambiental de sus operaciones. Esto incluye la gestión responsable de recursos y el cumplimiento de normativas ambientales vigentes.\n\nDatos de Gestión Interna\n\n1. Informe de Gestión y Sostenibilidad:\n- Transparencia y Buen Gobierno: La empresa publica informes anuales que detallan las actividades, resultados y compromisos en términos de sostenibilidad y buen gobierno corporativo.\n- Innovación y Desarrollo: Descripción de proyectos innovadores y desarrollos tecnológicos que contribuyen a la eficiencia operativa y la mejora del servicio.\n\nPara más detalles y acceso a documentos específicos, puedes visitar [Gases del Caribe](https://gascaribe.com)."
)


# Upload files and wait for them to be ready
files = [
    upload_to_gemini("Código-de-Conducta-Gascaribe-.pdf", mime_type="application/pdf"),
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
                "¡Hola! 👋  ¿En qué puedo ayudarte hoy? \n\nEstoy aquí para brindarte información sobre los procedimientos internos, reglas, normas convivenciales, reglamentos ambientales y cualquier dato de gestión interna de Gases del Caribe (GasCaribe). \n\n¿Tienes alguna pregunta específica? \n\nPor ejemplo:\n\n* ¿Puedes contarme sobre el proceso de solicitud de vacaciones?\n* ¿Cuáles son las normas de seguridad en el área de producción?\n* ¿Hay algún programa de reciclaje en la empresa?\n* ¿Dónde puedo encontrar el reglamento interno?\n\n¡Estoy aquí para ayudarte a encontrar la información que necesitas! 😄\n"
            ],
        },
        {
            "role": "user",
            "parts": [files[0]],
        },
        {
            "role": "model",
            "parts": [
                "¡Excelente! Tienes la Política Ambiental de Gases del Caribe. 😃\n\nPuedo ayudarte a entender mejor la información y a encontrar lo que necesitas. \n\n¿Qué te gustaría saber específicamente sobre esta Política Ambiental? \n\nPor ejemplo:\n\n* **¿Cuáles son los principales compromisos de Gases del Caribe en materia ambiental?**\n* **¿Qué medidas se implementan para proteger la biodiversidad?**\n* **¿Qué acciones se toman para mitigar el cambio climático?**\n* **¿Cómo se gestiona la Política Ambiental dentro de la empresa?**\n* **¿Qué documentos de referencia se utilizan?**\n\nDime qué te interesa y te ayudaré a encontrar la información que necesitas. \n"
            ],
        },
        {
            "role": "user",
            "parts": ["¿Quién administra la política ambiental en Gases del Caribe?\n"],
        },
        {
            "role": "model",
            "parts": [
                "Según la Política Ambiental que me has compartido, la **Gerencia de Sostenibilidad y Medio Ambiente** de Gases del Caribe es la encargada de administrar la Política Ambiental. \n\nTambién se menciona que la responsabilidad de implementar las acciones para su cumplimiento recae en cada una de las empresas vinculadas. \n\nEn resumen, la Gerencia de Sostenibilidad y Medio Ambiente tiene el rol principal de administrar la Política Ambiental, pero la implementación de las acciones se realiza en conjunto por todas las empresas del grupo. \n"
            ],
        },
    ]
)


# Infinitely prompt the model
while True:
    user_input = input("Escribe tu pregunta: ")
    response = chat_session.send_message(user_input)
    print(response.text)

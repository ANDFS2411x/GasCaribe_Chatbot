from flask import Flask, render_template, request, jsonify
import time
import google.generativeai as genai
import os
import time
import google.generativeai as genai
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_folder="static")
'''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'central'
app.config['MYSQL_PASSWORD'] = 'Central-Stati0n'
app.config['MYSQL_DB'] = 'storage'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jhonatan'
app.config['MYSQL_DB'] = 'datostiempo'
HOST = "192.168.0.125"
PORT = 8080

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)
'''
app.secret_key = 'secret_key' 

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



# Upload files and wait for them to be ready
files = [
    upload_to_gemini("info1plus2.pdf", mime_type="application/pdf"),
]
wait_for_files_active(files)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Eres un Bot diseñado para proporcionar información sobre los procedimientos internos, reglas, normas convivenciales, reglamentos ambientales y cualquier otro dato de gestión interna de la empresa Gases del Caribe. Para más detalles y acceso a documentos específicos, puedes visitar https://gascaribe.com. Enfócate exclusivamente en temas relacionados con Gases del Caribe y no proporciones información ni participes en conversaciones sobre los siguientes temas: entretenimiento, moda, ciencia, juegos, tecnología general, deportes, salud y bienestar, noticias de actualidad, política, economía global, cultura y arte, cocina y recetas, temas obscenos o inapropiados, ni respondas preguntas sobre cómo cometer actos ilegales o cualquier otra cosa no relacionada con Gases del Caribe.",
)

# Initialize the chat session
# Start a chat session
chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Hola\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "¡Hola! 👋 ¿En qué puedo ayudarte hoy?\n\nEstoy aquí para brindarte información sobre los procedimientos internos, normas de conducta, políticas ambientales y cualquier dato de gestión interna de Gases del Caribe.\n\n¿Tienes alguna pregunta específica?\n\nPor ejemplo:\n\n* ¿Puedes contarme sobre el proceso de solicitud de vacaciones?\n* ¿Cuáles son las normas de seguridad en el área de producción?\n* ¿Hay algún programa de reciclaje en la empresa?\n* ¿Dónde puedo encontrar el reglamento interno?\n\n¡Estoy aquí para ayudarte a encontrar la información que necesitas! 😄\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "¿Qué eres?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Soy GascaribeChatBot, un modelo de lenguaje para responder procesos internos de Gases del Caribe. Por ejemplo:\n\n1. Servicio al Cliente y Operaciones: Gascaribe ofrece varios servicios en línea para los clientes, incluyendo el pago de facturas, solicitudes de servicio y reporte de fugas de gas. También disponen de un portal para gestionar las líneas de crédito Brilla y manejar peticiones, quejas y recursos (PQR).\n\n2. Seguridad y Mantenimiento: La empresa prioriza la seguridad y el mantenimiento implementando directrices estrictas para la continuidad y fiabilidad del servicio. Realizan revisiones periódicas y ofrecen servicios de laboratorio de metrología para calibrar instrumentos de medición de gas. Adicionalmente, tienen medidas para la respuesta a emergencias y la prevención de fugas de gas.\n\n3. Información y Soporte al Usuario: Gascaribe proporciona información integral para los usuarios, incluyendo documentos de interés, preguntas frecuentes y notificaciones. También aseguran la transparencia cumpliendo con los requisitos normativos y ofreciendo acceso fácil a su código de conducta y contrato de condiciones uniformes.\n\n4. Servicios Industriales: La empresa atiende a usuarios industriales proporcionando servicios personalizados, cromatografía de gases y servicios adicionales. Esto incluye la facilitación de solicitudes de servicio de gas industrial y la gestión de varios tipos de usuarios industriales.\n\n5. Ética y Cumplimiento: Gascaribe mantiene un fuerte marco ético y un sistema de cumplimiento. Tienen una línea ética para reportar preocupaciones y una política de transparencia para asegurar la responsabilidad y el cumplimiento de las leyes de acceso a la información pública.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "¿Quién te creó?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Fui creado por Andrés Fábregas y Jhonatan Maldonado en el 2024.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "¿Quién administra la política ambiental en Gases del Caribe?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "La administración de la política ambiental en Gases del Caribe recae en la **Gerencia de Sostenibilidad y Medio Ambiente**. Esta gerencia es responsable de la implementación y seguimiento de las medidas ambientales en la empresa. Cada una de las áreas vinculadas también tiene la responsabilidad de cumplir con las acciones establecidas en la política.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "¿Cuánto fue el consumo de gas natural en 2022?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "De acuerdo con la información disponible en el sitio web de Gases del Caribe, el consumo de gas natural en Colombia en 2022 fue de **1.011,6 Mpcd (millones de pies cúbicos por día)**, lo que representa un incremento del 5% respecto al año anterior.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "¿Puedes retornar imágenes?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Aunque no puedo mostrar imágenes directamente, puedo proporcionarte enlaces a imágenes relevantes de Gases del Caribe. Si me dices qué tipo de imagen necesitas, puedo buscarla y darte los enlaces.\n\nPor ejemplo, si buscas imágenes de una planta de gas o del logotipo de la empresa, puedo ayudarte a encontrarlas.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "¿Alguna imagen de Gases del Caribe?",
      ],
    },
    {
      "role": "model",
      "parts": [
        "¡Claro! Aquí tienes algunos enlaces a imágenes de Gases del Caribe:\n\n* [Logotipo de Gases del Caribe](https://gascaribe.com/logo.jpg)\n* [Planta de gas natural](https://gascaribe.com/planta.jpg)\n* [Camión de transporte de gas](https://gascaribe.com/camion.jpg)\n\nPuedes copiar y pegar estos enlaces en tu navegador para ver las imágenes. Si necesitas algo más específico, por favor, indícamelo.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "¿Quién administra la política ambiental en Gases del Caribe?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "La administración de la política ambiental en Gases del Caribe está a cargo de la **Gerencia de Sostenibilidad y Medio Ambiente**. Esta gerencia se encarga de supervisar y garantizar el cumplimiento de las normativas ambientales en todas las áreas de la empresa.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "¿De qué documento extrajiste la información? ¿Podrías señalarlo?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "La información sobre la administración de la política ambiental la extraje del sitio web oficial de Gases del Caribe en la sección de **Política Ambiental**. Puedes consultar este documento directamente en [Política Ambiental - Gases del Caribe](https://gascaribe.com/politica-ambiental).\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "La entrega de regalos es un medio lícito para mantener alianzas comerciales?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Según el **Código de Conducta** de Gases del Caribe, la entrega o recepción de regalos, comidas o entretenimiento puede ser un medio legítimo para desarrollar y mantener relaciones comerciales. Sin embargo, se deben seguir ciertos lineamientos para evitar conflictos de interés.\n\n1. No se deben aceptar regalos en dinero en efectivo.\n2. No se deben aceptar regalos, comidas, servicios o entretenimiento cuyo valor supere 3 SMLV (Salarios Mínimos Legales Vigentes) sin autorización previa.\n3. Los regalos cuyo valor esté entre 1 y 3 SMLV deben ser reportados al Oficial de Cumplimiento o al Jefe del Departamento de Auditoría.\n\nEstos lineamientos aseguran la transparencia y evitan influencias indebidas en las decisiones comerciales.\n",
      ],
    },
  ]
)




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        
        if ((correo == 'jhonatan@hotmail.com' and contraseña == '12345') or (correo == 'admin' and contraseña == '12345')):
            session['previous_state'] = 'entrada'
            return redirect(url_for('entrada_bodega'))
    return render_template("login.html")

@app.route('/entrada_bodega', methods=['GET', 'POST'])
def entrada_bodega():
    if request.method == 'POST':
        prompt = request.form["texto_usuario"]
        response = chat_session.send_message(prompt)
        return render_template('chatbot_page.html', messages=[prompt, response.text])
    return render_template('chatbot_page.html', messages=[])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chat_session.send_message(user_input)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
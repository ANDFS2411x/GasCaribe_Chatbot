import webbrowser
from flask import Flask, render_template, request,redirect,url_for, session,jsonify
import pymysql, socket
from threading import Timer
import os
import time
import google.generativeai as genai

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






genai.configure(api_key="AIzaSyC5zkGQLaIJydlYkMQ6xUN2iXT8SqDb6Fs")

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
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

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
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
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Soy un Bot orientado a proporcionar información acerca de los procedimientos internos, reglas, normas convivenciales, reglamentos ambientales y básicamente cualquier dato de gestión interna de la empresa Gases del Caribe. Para más detalles y acceso a documentos específicos, puedes visitar [Gases del Caribe](https://gascaribe.com)",
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("Código-de-Conducta-Gascaribe-.pdf", mime_type="application/pdf"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

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
        "¡Hola! 👋  ¿En qué puedo ayudarte hoy? \n\nEstoy aquí para brindarte información sobre los procedimientos internos, reglas, normas convivenciales, reglamentos ambientales y cualquier dato de gestión interna de Promigas. \n\n¿Tienes alguna pregunta específica? \n\nPor ejemplo:\n\n* ¿Puedes contarme sobre el proceso de solicitud de vacaciones?\n* ¿Cuáles son las normas de seguridad en el área de producción?\n* ¿Hay algún programa de reciclaje en la empresa?\n* ¿Dónde puedo encontrar el reglamento interno?\n\n¡Estoy aquí para ayudarte a encontrar la información que necesitas! 😄\n",
        "¡Excelente! Tienes la Política Ambiental de Promigas. 😃\n\nPuedo ayudarte a entender mejor la información y a encontrar lo que necesitas. \n\n¿Qué te gustaría saber específicamente sobre esta Política Ambiental? \n\nPor ejemplo:\n\n* **¿Cuáles son los principales compromisos de Promigas en materia ambiental?**\n* **¿Qué medidas se implementan para proteger la biodiversidad?**\n* **¿Qué acciones se toman para mitigar el cambio climático?**\n* **¿Cómo se gestiona la Política Ambiental dentro de la empresa?**\n* **¿Qué documentos de referencia se utilizan?**\n\nDime qué te interesa y te ayudaré a encontrar la información que necesitas. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Quien administra la politica ambiental en promigas?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Según la Política Ambiental que me has compartido, la **Gerencia de Sostenibilidad y Medio Ambiente** de Promigas es la encargada de administrar la Política Ambiental. \n\nTambién se menciona que la responsabilidad de implementar las acciones para su cumplimiento recae en cada una de las empresas vinculadas. \n\nEn resumen, la Gerencia de Sostenibilidad y Medio Ambiente tiene el rol principal de administrar la Política Ambiental, pero la implementación de las acciones se realiza en conjunto por todas las empresas del grupo. \n",
        "¡Gracias por compartir el Informe Integrado de Gestión 2022 de Promigas! \n\nAhora entiendo mejor la estructura de la empresa y su enfoque en la gestión de la sostenibilidad.\n\nPara ayudarte a comprender mejor la información, te recomiendo que me digas:\n\n* **¿Qué te interesa específicamente sobre la empresa Promigas?** Por ejemplo, ¿te gustaría saber más sobre sus actividades en Perú, su estrategia climática, su programa de inversión social o su gestión del talento humano?\n* **¿Qué tipo de información buscas?** ¿Te interesa encontrar un dato específico, como por ejemplo el número de usuarios de Brilla o la inversión ambiental del año? ¿O prefieres una visión general sobre un tema en particular, como la innovación en la empresa?\n\nCon tu ayuda, puedo encontrar la información que necesitas en el informe de forma más rápida y precisa. 😄 \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "cuanto fue el consumo de gas nacional en 2022\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "De acuerdo con el informe que me proporcionaste, el consumo de gas natural en Colombia en 2022 fue de **1.011,6 Mpcd (millones de pies cúbicos por día)**. \n\nEso representa un **incremento del 5%** con respecto al consumo del año 2021. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Puedes retornar imagenes?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "¡Desafortunadamente, no puedo retornar imágenes directamente! \n\nSoy un modelo de lenguaje, y estoy diseñado para procesar y generar texto. No tengo la capacidad de mostrar imágenes o archivos multimedia. \n\nSin embargo, puedo ayudarte a encontrar imágenes relacionadas con Promigas:\n\n* **Si me das un tema específico**, puedo buscar imágenes en internet y darte los enlaces. Por ejemplo, si me dices \"imágenes de la terminal de regasificación SPEC LNG\", puedo buscar en Google Imágenes y darte algunos resultados.\n* **Si me dices qué tipo de imagen necesitas**, puedo buscar imágenes que se ajusten a tu solicitud. Por ejemplo, si me dices \"una imagen que muestre la huella social de Promigas\", puedo buscar imágenes que representen el impacto de la empresa en las comunidades.\n\n¿Qué tipo de imágenes te gustaría encontrar? 😊\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "alguna imagen de promigas",
      ],
    },
    {
      "role": "model",
      "parts": [
        "¡Claro que sí!  \n\nAunque no puedo mostrarte las imágenes directamente, puedo darte algunos enlaces a imágenes de Promigas que encontré en una búsqueda rápida en Google Imágenes:\n\n* **[Enlace 1]:** Esta imagen muestra el logotipo de Promigas. \n* **[Enlace 2]:** Esta imagen muestra una estación de compresión de gas natural de Promigas.\n* **[Enlace 3]:** Esta imagen muestra un camión de Promigas que transporta gas natural. \n\nEspero que estos enlaces te ayuden a encontrar las imágenes que buscas. \n\nSi me dices algo más específico sobre lo que estás buscando, como \"una imagen de la sede de Promigas en Barranquilla\", puedo ayudarte a encontrar imágenes más precisas.  \n\n\n**Recuerda:** \n* Reemplaza \"[Enlace 1]\", \"[Enlace 2]\" y \"[Enlace 3]\" con los enlaces reales que te proporcionó la búsqueda en Google Imágenes. \n* Puedes copiar y pegar estos enlaces en tu navegador para ver las imágenes. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Quien administra la politica ambiental en promigas?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "¡Excelente pregunta! De acuerdo con la Política Ambiental de Promigas que me has compartido, la **Gerencia de Sostenibilidad y Medio Ambiente** es la responsable de administrar la política ambiental. \n\nAunque la Gerencia de Sostenibilidad y Medio Ambiente tiene el rol principal, la Política Ambiental también menciona que cada una de las empresas vinculadas a Promigas tiene la responsabilidad de implementar las acciones para su cumplimiento. \n\nEn resumen, la Gerencia de Sostenibilidad y Medio Ambiente es la administradora de la política, pero su éxito depende de la colaboración y el compromiso de todas las empresas del grupo Promigas. \n\n¿Te gustaría saber más sobre la estructura organizativa de Promigas o sobre la Gerencia de Sostenibilidad y Medio Ambiente? 😄\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "de que documento extrajiste la informacion? podrias señalarlo?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "¡Tienes razón! \n\nLa información sobre quién administra la política ambiental en Promigas la extraje del documento que me proporcionaste al inicio de nuestra conversación, el PDF titulado \"POLITICA AMBIENTAL.pdf\". \n\nEn la sección 5.3 de este documento, se menciona claramente que la **Gerencia de Sostenibilidad y Medio Ambiente** es la encargada de administrar la Política Ambiental. \n\n¿Te gustaría que te ayudara a encontrar alguna otra información específica dentro de este documento? 😊 \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[0],
      ],
    },
    {
      "role": "model",
      "parts": [
        "¡Genial! Ya entiendo. \n\nHas compartido el Código de Conducta de Gases del Caribe, que es un documento muy útil para comprender las normas éticas y de comportamiento que rigen la empresa. \n\nCon base en la información que me has dado, puedo decirte que el Código de Conducta de Gases del Caribe fue elaborado y está vigente a partir del 8 de abril de 2009. \n\nLa última versión del documento es del 30 de octubre de 2018. \n\nEste código es una herramienta importante para todos los empleados, administradores, contratistas y proveedores de Gases del Caribe. \n\n¿Qué te gustaría saber específicamente sobre el Código de Conducta? \n\nPor ejemplo, ¿quieres conocer las normas sobre conflicto de interés, cómo reportar una violación al código, o las responsabilidades en materia de seguridad y salud en el trabajo? \n\n¡Estoy aquí para ayudarte a encontrar la información que necesitas! 😊 \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "la entrega de regalos es un medio licito para mantener alianzas comerciales?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "¡Buena pregunta! \n\nEl Código de Conducta de Gases del Caribe reconoce que la entrega o recepción de regalos, comidas o actividades de entretenimiento puede ser un medio para desarrollar y mantener alianzas comerciales legítimas. Sin embargo, también advierte que se debe ejercer mucha cautela para mantener la confianza e integridad en las relaciones comerciales. \n\nEl código establece que los empleados de Gases del Caribe NO deben aceptar jamás un regalo, una invitación a comer, servicios o entretenimientos que tengan por objeto afectar o comprometer sus decisiones comerciales. \n\nEn otras palabras, la entrega de regalos puede ser lícita para mantener alianzas comerciales, siempre y cuando NO se utilice como un medio para influenciar decisiones o obtener ventajas indebidas. \n\nEl código también establece límites específicos para los regalos, comidas, servicios y atenciones:\n\n* **No se debe aceptar ningún regalo en dinero en efectivo.**\n* **No se debe aceptar ningún regalo, invitación a comer, servicios y entretenimientos, cuyo valor equivalente en pesos colombianos sea superior a 3 SMLV.** (Salvo que se obtenga una autorización previa)\n* **Los regalos, comidas, servicios y atenciones cuyo valor oscile entre los valores en pesos colombianos equivalentes a 1 a 3 SMLV deberán ser reportados al Oficial de Cumplimiento o al Jefe del Departamento de Auditoría.**\n\nEn resumen, la entrega de regalos puede ser un medio lícito para mantener alianzas comerciales, pero se debe actuar con transparencia y responsabilidad para evitar cualquier percepción de conflicto de interés. \n\n¿Te gustaría saber más sobre las políticas de Gases del Caribe en relación a los regalos? \n",
      ],
    },
  ]
)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Aquí puedes acceder a los datos del formulario
        correo = request.form['correo']

        contraseña=request.form['contraseña']
        # Puedes hacer lo que necesites con los datos, como guardarlos en una base de datos
        if ((correo == 'jhonatan@hotmail.com' and contraseña == '12345') or (correo == 'admin' and contraseña == '12345')):
            session['previous_state'] = 'entrada'  # Almacena el estado anterior en la sesión
            # Redirige a otra página HTML si las credenciales son correctas
            return redirect(url_for('entrada_bodega'))
    return render_template("login.html")



messages_to_display=[]
@app.route('/chatbot_page', methods=['GET', 'POST'])
def entrada_bodega():
    if request.method == 'POST':
        prompt = request.form["texto_usuario"]
        
        response = chat_session.send_message(prompt)
        if response:
            return jsonify({"bot_response": response.text})

    return render_template('chatbot_page.html', messages=messages_to_display)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


def open_browser():
    url = "http://localhost:5000"
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    #cursor = mysql.cursor()
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)  # Deshabilita el cargador automático
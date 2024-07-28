from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import google.generativeai as genai
import PyPDF2
import webbrowser
from threading import Timer
app = Flask(__name__, static_folder="static")
app.secret_key = 'secret_key'

# Configurar la API key de Google
genai.configure(api_key="AIzaSyBeOhFkN0L_mdq30gSk6cilc4oT9Azds54")

def leer_pdf(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        texto = ""
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def chatbot(prompt, contexto):
    modelo = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            "Eres un Bot diseñado para proporcionar información sobre los procedimientos internos, "
            "reglas, normas convivenciales, reglamentos ambientales y cualquier otro dato de gestión interna "
            "de la empresa Gases del Caribe. Para más detalles y acceso a documentos específicos, puedes visitar "
            "https://gascaribe.com. Enfócate exclusivamente en temas relacionados con Gases del Caribe y no proporciones "
            "información ni participes en conversaciones sobre los siguientes temas: entretenimiento, moda, ciencia, juegos, "
            "tecnología general, deportes, salud y bienestar, noticias de actualidad, política, economía global, cultura y arte, "
            "cocina y recetas, temas obscenos o inapropiados, ni respondas preguntas sobre cómo cometer actos ilegales o cualquier "
            "otra cosa no relacionada con Gases del Caribe."
        ),
    )
    chat = modelo.start_chat(history=[])
    respuesta = chat.send_message(f"Basándote en el siguiente contexto, responde a la pregunta: \n\nContexto: {contexto}\n\nPregunta: {prompt}")
    return respuesta.text

# Ruta del archivo PDF
ruta_pdf = "info.pdf"

# Leer el contenido del PDF
contenido_pdf = leer_pdf(ruta_pdf)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        
        if ((correo == 'jhonatan@hotmail.com' and contraseña == '12345') or (correo == 'admin' and contraseña == '12345')):
            session['previous_state'] = 'entrada'
            return redirect(url_for('entrada_bodega'))
    return render_template("login.html")

@app.route('/chatbot_page', methods=['GET', 'POST'])
def entrada_bodega():
    if request.method == 'POST':
        pregunta = request.form["texto_usuario"]
        response = chatbot(pregunta, contenido_pdf)
        return render_template('chatbot_page.html', messages=[pregunta, response])
    return render_template('chatbot_page.html', messages=[])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chatbot(user_input, contenido_pdf)
    return jsonify({'response': response})

def open_browser():
    url = "http://localhost:5000"
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)  # Deshabilita el cargador automático
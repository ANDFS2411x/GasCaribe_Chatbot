import webbrowser
from flask import Flask, render_template, request,redirect,url_for, session,jsonify
import pymysql, socket
from threading import Timer
import os
import time
import google.generativeai as genai
import logging

app = Flask(__name__, static_folder="static")

app.secret_key = 'secret_key'  




genai.configure(api_key="AIzaSyCn2MW0BUTIVRLRajBGw_Zn7sLVWj3utoY")


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
  system_instruction="Soy un Bot orientado a proporcionar información acerca de los procedimientos internos, reglas, normas convivenciales, reglamentos ambientales y básicamente cualquier dato de gestión interna de la empresa Gases del Caribe.",
)

# TODO Make these files available on the local file system
# You may need to update the file paths


# Some files have a processing delay. Wait for them to be ready.

chat_session = model.start_chat()






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


logging.basicConfig(level=logging.INFO)

@app.route('/log', methods=['POST'])
def log():
    text = request.json['text']
    return '', 204



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
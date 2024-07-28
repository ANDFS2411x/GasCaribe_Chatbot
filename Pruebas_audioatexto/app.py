from flask import Flask, render_template, request
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log():
    text = request.json['text']
    logging.info(f"Texto reconocido: {text}")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
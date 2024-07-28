import PIL.Image
import google.generativeai as genai
from google.api_core.exceptions import NotFound

# Configura la API con tu clave
genai.configure(api_key="AIzaSyC5zkGQLaIJydlYkMQ6xUN2iXT8SqDb6Fs")

# Carga la imagen
img = PIL.Image.open('foto1.jpg')

# Cambia al nuevo modelo
model = genai.GenerativeModel('gemini-1.5-flash')

# Genera el contenido con el nuevo modelo
try:
    response = model.generate_content(img)
    print(response.text)
except NotFound as e:
    print("Modelo no encontrado:", e)
except Exception as e:
    print("Ocurrió un error:", e)

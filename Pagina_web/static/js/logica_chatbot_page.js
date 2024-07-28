const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

//si no ha iniciado sesion y altera la url, de igual se redirige a la pagina de login
if (!isAuthenticated) {
  window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', function() {
  var conversationZone = document.getElementById('conversation');
  conversationZone.scrollTop = conversationZone.scrollHeight;
});

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('formulario_ingreso');
  const conversationDiv = document.getElementById('conversation');
  const userInput = document.getElementById('texto_usuario');

  form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const userMessage = userInput.value;
      
      // Añadir inmediatamente el mensaje del usuario a la conversación
      appendMessage(userMessage, 'user');
      
      // Limpiar el input
      userInput.value = '';

      // Enviar el mensaje al servidor
      fetch('/chatbot_page', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
              'texto_usuario': userMessage
          })
      })
      .then(response => response.json())
      .then(data => {
          // Añadir la respuesta del bot a la conversación
          appendMessage(data.bot_response, 'bot');
      });
  });

  function appendMessage(message, sender) {
      const messageDiv = document.createElement('div');
      messageDiv.className = `message-container ${sender}-container`;
      messageDiv.innerHTML = `<div class="${sender}-message">${message}</div>`;
      conversationDiv.appendChild(messageDiv);
      
      // Hacer scroll hasta el final de la conversación
      conversationDiv.scrollTop = conversationDiv.scrollHeight;
  }
});


const checkbox = document.getElementById('listenCheckbox');
const textInput = document.getElementById('texto_usuario');
let recognition;

if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';

    recognition.onresult = function(event) {
        let interimTranscript = '';
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            let transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
                console.log(transcript);  // Imprime en la consola del navegador
                fetch('/log', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({text: transcript}),
                });
            } else {
                interimTranscript += transcript;
            }
        }
        textInput.value = finalTranscript || interimTranscript;
    };

    checkbox.addEventListener('change', function() {
        if (this.checked) {
            recognition.start();
            textInput.value = '';  // Limpiar el input al comenzar
        } else {
            recognition.stop();
        }
    });
} else {
    alert('Tu navegador no soporta reconocimiento de voz.');
}

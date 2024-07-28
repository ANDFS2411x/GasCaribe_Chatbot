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
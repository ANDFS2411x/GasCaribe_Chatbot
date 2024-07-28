const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

//si no ha iniciado sesion y altera la url, de igual se redirige a la pagina de login
if (!isAuthenticated) {
  window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', function() {
  var conversationZone = document.getElementById('conversation');
  conversationZone.scrollTop = conversationZone.scrollHeight;
});
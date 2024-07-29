var boton=document.getElementById("boton_envio")
var correo=document.getElementById("correo")
var contraseña=document.getElementById("contraseña")

function aut(){
    if((correo.value=="jhonatan@hotmail.com" && contraseña.value=="12345") || (correo.value=='admin' && contraseña.value=='12345')){
        localStorage.setItem('isAuthenticated', 'true');
    }else{
        alert("credenciales incorrectas")
        localStorage.setItem('isAuthenticated', 'false');

    }

}
boton.addEventListener("click",aut)


var boton_qr=document.getElementById("btn_redirigir")
var contenedor_correo=document.getElementById("contenedor_correo")
var contenedor_contraseña=document.getElementById("contenedor_contraseña")
var contenedor_envio=document.getElementById("boton_envio")
var parrafo_volver=document.getElementById("parrafo_volver")
var parrafo_qr=document.getElementById("parrafo_qr")
var contenedor_camara=document.querySelector(".contenedor_camara")
boton_qr.addEventListener("click",function(){
    contenedor_correo.classList.add("hidden");
    contenedor_contraseña.classList.add("hidden");
    contenedor_envio.classList.add("hidden");
    parrafo_volver.classList.remove("pvolv")
    parrafo_qr.classList.add("hidden")
    parrafo_volver.classList.add("estilo_retornar")
    contenedor_camara.classList.remove("loco")
})


parrafo_volver.addEventListener("click",function(){
    contenedor_correo.classList.remove("hidden");
    contenedor_contraseña.classList.remove("hidden");
    contenedor_envio.classList.remove("hidden");
    parrafo_volver.classList.add("pvolv")
    parrafo_qr.classList.remove("hidden")
    contenedor_camara.classList.add("loco")

})



var myqr=document.getElementById("your-qr-result")
var lastResult,countResults=0;
var contenedor=document.getElementById("contenedor")



//ocultar el boton de pausa
document.addEventListener('DOMContentLoaded', function() {
    var pausa=document.getElementById("my-qr-reader__dashboard_section")
    //pausa.style.display="none"
    const videostr=document.getElementById("my-qr-reader__scan_region")
    videostr.style.transform="scaleX(-1)"
    //videostr.style.opacity=0
    const elements = document.querySelectorAll('*');
    elements.forEach(element => {
      element.style.borderColor = 'transparent';
    });
  });
  




  validador_reset=false      

  function onScanSuccess(decodeText,decodeResult){ 
    console.log(decodeText)
    if(decodeText=="work" || decodeText=="end"){
        correo.value="jhonatan@hotmail.com"
        contraseña.value="12345"
        boton.click()
    }else{
        alert("Credenciales incorrectas")
    }
  
  }
  
  var htmlscanner=new Html5QrcodeScanner(
      "my-qr-reader", {fps:1,qrbox:170})
  
      htmlscanner.render(onScanSuccess)
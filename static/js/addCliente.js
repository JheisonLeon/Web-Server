(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
          form.classList.add('was-validated')
  
        }, false)
      })
  })()
  

  function validar(){
    aux = document.getElementById('nombreUsuario')
    sitio = aux.value
    if (sitio.includes(' ')){
      aux.value = '';
      Swal.fire('No debe existir espacios en blanco', '', 'error');
      
    } if (sitio.includes(',') || sitio.includes('.')){
      aux.value = '';
      Swal.fire('No debe existir comas ni puntos', '', 'error');
      
    }
  }
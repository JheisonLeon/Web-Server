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
  
  /*$(function(){
      $('ul.tabs li:first').addClass('active');
      $('.secciones article').hide();
      $('.secciones article:first').show();
  });
  $('ul.tabs li').click(function(){
      $('ul.tabs li').removeClass('active');
      $(this).addClass('active');
      $('.secciones article').hide();
      var activeTab = $(this.firstElementChild).attr('href');
      if(activeTab == '#Tab5'){
        $('body').addClass('fondoTab5');
        $('body').removeClass('fondoTab4');
        $('body').removeClass('fondoTab3');
        $('body').removeClass('fondoTab2');
        $('body').removeClass('fondoTab1');
      }else if( activeTab == '#Tab4'){
        $('body').addClass('fondoTab4');
        $('body').removeClass('fondoTab5');
        $('body').removeClass('fondoTab3');
        $('body').removeClass('fondoTab2');
        $('body').removeClass('fondoTab1');
      }else if( activeTab == '#Tab3'){
        $('body').addClass('fondoTab3');
        $('body').removeClass('fondoTab5');
        $('body').removeClass('fondoTab4');
        $('body').removeClass('fondoTab2');
        $('body').removeClass('fondoTab1');
      }else if( activeTab == '#Tab2'){
        $('body').addClass('fondoTab2');
        $('body').removeClass('fondoTab5');
        $('body').removeClass('fondoTab4');
        $('body').removeClass('fondoTab3');
        $('body').removeClass('fondoTab1');
      }else if( activeTab == '#Tab1'){
        $('body').addClass('fondoTab1');
        $('body').removeClass('fondoTab5');
        $('body').removeClass('fondoTab4');
        $('body').removeClass('fondoTab3');
        $('body').removeClass('fondoTab2');
      }
     
      $(activeTab).show();
      return false;
  });*/
  
  $('.burger').click(function () {
  
    let x = $('#side_nav').width();
    if (x <= 55) {
      $('#side_nav').addClass('menu-expanded');
      $('#side_nav').removeClass('menu-collapsed');
    } else {
      $('#side_nav').addClass('menu-collapsed');
      $('#side_nav').removeClass('menu-expanded');
    }
  
    return false;
  });
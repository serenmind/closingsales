(function() {
  'use strict';
  $(function() {
    function toggleError(con, remove) {
      if (!remove) {
        con.parents('.input-wrap').addClass('.has-error');
      } else {
        con.parents('.input-wrap').removeClass('.has-error');
      }
    }
    var email = $('#email'),
        phone = $('#phone'),
        full_name = $('#full_name'),
        message = $('#message');

     $('#submit').on('click', function(evt) {
      var name = full_name.val();
      if (name.trim() === '') {
        
        full_name.parents('.input-wrap').addClass('has-error');
        return false;
      } else {
        full_name.parents('.input-wrap').removeClass('has-error');
      }
      var phone_no = phone.val()
      if (phone_no.trim() === '') {
        phone.parents('.input-wrap').addClass('has-error'); 
        return false;
      } else {
        phone.parents('.input-wrap').removeClass('has-error');
      }

      var messageText = message.val()
      if (messageText.trim() === '') {
        message.parents('.input-wrap').addClass('has-error');
        return false
      }
     });
   });
}())
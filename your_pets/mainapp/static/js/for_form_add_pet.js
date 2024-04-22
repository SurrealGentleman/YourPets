$(document).ready(function() {
  const radioButtons = document.querySelectorAll('input[type="radio"]');
  for (let i = 0; i < radioButtons.length; i++) {
    radioButtons[i].addEventListener('change', function() {
      const petId = this.id;
      alert(petId)
      if (petId == 'add-pet_button') {
        $.ajax({
          url: '/add_pet/',
          type: 'GET',
          data: {},
          success: function(response) {
            $('#form-container').html(response.form_html);
          },
          error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
          }
        });
      }
      else {
        $.ajax({
          url: '/change_pet/',
          type: 'GET',
          data: {'pet_id': petId},
          success: function(response) {
            $('#form-container2').html(response.form_html);
          },
          error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
          }
        });
      }
    });
  }
});
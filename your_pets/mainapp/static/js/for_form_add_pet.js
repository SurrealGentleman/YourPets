    $(document).ready(function() {
        $('#id_pets').on('change', function() {
            var petId = $(this).val();
            if (petId == 'add-pet_button') {
                $.ajax({
                    url: '/add_pet/',  // URL, по которому обрабатывается асинхронный запрос на получение пород
                    type: 'GET',
                    success: function(response) {
                        $('#form-container').html(response.form_html);
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            }
            else if (petId == ''){
                $('#form-container').html('');
            }
        });
    });
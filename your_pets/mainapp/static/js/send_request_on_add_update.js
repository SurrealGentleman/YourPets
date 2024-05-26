$(document).ready(function() {
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    for (let i = 0; i < radioButtons.length; i++) {
        radioButtons[i].addEventListener('change', function() {
            const petId = this.id;
            if (petId == 'add-pet_button') {
                $.ajax({
                    url: '/get_form/',
                    type: 'GET',
                    data: {
                        'add_pet': true
                    },
                    success: function(response) {
                        $('#form-container-add_update_pet').html(response.form_html);
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            }
            else {
                $.ajax({
                    url: '/get_form/',
                    type: 'GET',
                    data: {
                        'update_pet': true,
                        'pet_id': petId
                    },
                    success: function(response) {
                        $('#form-container-add_update_pet').html(response.form_html);
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            }
        });
    }

    $('input[type="radio"]').each(function() {
        if ($(this).is(':checked')) {
            var petId = this.id;
            if (petId == 'add-pet_button') {
                $.ajax({
                    url: '/get_form/',
                    type: 'GET',
                    data: {
                        'add_pet': true
                    },
                    success: function(response) {
                        $('#form-container-add_update_pet').html(response.form_html);
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            }
            else {
                $.ajax({
                    url: '/get_form/',
                    type: 'GET',
                    data: {
                        'update_pet': true,
                        'pet_id': petId
                    },
                    success: function(response) {
                        $('#form-container-add_update_pet').html(response.form_html);
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            }
        }
    });
});
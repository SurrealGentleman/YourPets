$(document).ready(function() {
    $('#change_password').click(function() {
        $.ajax({
            url: '/change_password/',
            type: 'GET',
            data: {
                'change_password': true
            },
            success: function(response) {
                $('#form-container-change_password').html(response.form_html);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});
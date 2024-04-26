$(document).ready(function() {
    $('#id_kind').on('change', function() {
        var kindId = $(this).val();
        if (kindId) {
            $.ajax({
                url: '/get_breeds/',
                type: 'GET',
                data: {
                    'kind_id': kindId
                },
                success: function(data) {
                    $('#id_breed').empty();
                    if (data.length > 0) {
                        $.each(data, function(index, breed) {
                            $('#id_breed').append('<option value="' + breed.id + '">' + breed.name + '</option>');
                        });
                    } else {
                        $('#id_breed').append('<option value="">Нет доступных пород</option>');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при получении пород');
                }
            });
        }
        else {
            $('#id_breed').empty();
        }
    });
});
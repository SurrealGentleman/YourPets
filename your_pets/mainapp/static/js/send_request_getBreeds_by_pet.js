$(document).ready(function() {
    $('input[name="pet"]').each(function() {
        if ($(this).is(':checked')) {
            var petId = $(this).val();
            if (petId) {
                $.ajax({
                    url: '/get_breeds/',
                    type: 'GET',
                    data: {
                        'pet_id': petId
                    },
                    success: function(data) {
                        $('#id_breed').empty();
                        if (data.length > 0) {
                            $.each(data, function(index, breed) {
                                $('#id_breed')
                                .append('<div><input type="checkbox" name="breed" id="' + breed.id + '" value="'
                            + breed.id + '">' + '<label for="' + breed.id + '">' + breed.name + '</label></div>');
                            });

                            $('input[name="breed"]').each(function() {
                                var optionId = $(this).val();
                                if (selectedBreedIds != null) {
                                    if (selectedBreedIds.includes(optionId)) {
                                        $(this).prop('checked', true);
                                    }
                                }
                            });
                        } else {
                            $('#id_breed').append('<option value="">Нет доступных пород</option>');
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка при получении пород');
                    }
                });
            } else {
                $('#id_breed').empty();
            }
        }
    });

    $('input[name="pet"]').on('change', function() {
        var petId = $(this).val();
        if (petId) {
            $.ajax({
                url: '/get_breeds/',
                type: 'GET',
                data: {
                    'pet_id': petId
                },
                success: function(data) {
                    $('#id_breed').empty();
                    if (data.length > 0) {
                        $.each(data, function(index, breed) {
                            $('#id_breed')
                                .append('<div><input type="checkbox" name="breed" id="' + breed.id + '" value="'
                            + breed.id + '">' + '<label for="' + breed.id + '">' + breed.name + '</label></div>');
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

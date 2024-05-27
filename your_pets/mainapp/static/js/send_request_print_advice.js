$(document).ready(function() {
    $('input[name="pet"]').each(function() {
        if ($(this).is(':checked')) {
            var petId = $(this).val();
            if (petId) {
                $.ajax({
                    url: '/get_cards_advice/',
                    type: 'GET',
                    data: {
                        'pet_id': petId,
                    },
                    success: function(response) {
                        $('#card_advice').html(response.cards_html);
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка при получении карточек советов');
                    }
                });
            } else {
                $('#card_advice').empty();
            }
        }
    });

    $('input[name="pet"]').on('change', function() {
        var petId = $(this).val();
        if (petId) {
            $.ajax({
                url: '/get_cards_advice/',
                type: 'GET',
                data: {
                    'pet_id': petId,
                },
                success: function(response) {
                    $('#card_advice').html(response.cards_html);
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при получении карточек советов');
                }
            });
        }
        else {
            $('#card_advice').empty();
        }
    });
});
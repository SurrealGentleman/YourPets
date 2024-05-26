$(document).ready(function() {
    $('input[name="pet"]').each(function() {
        if ($(this).is(':checked')) {
            var petId = $(this).val();
            var mutual_likes = $('#id_mutual_likes').prop('checked');
            if (petId) {
                $.ajax({
                    url: '/get_cards_likes/',
                    type: 'GET',
                    data: {
                        'pet_id': petId,
                        'mutual_likes': mutual_likes
                    },
                    success: function(response) {
                        $('#card_likes').html(response.cards_html);
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка при получении карточек животных');
                    }
                });
            } else {
                $('#card_likes').empty();
            }
        }
    });

    $('input[name="pet"]').on('change', function() {
        var petId = $(this).val();
        var mutual_likes = $('#id_mutual_likes').prop('checked');
        if (petId) {
            $.ajax({
                url: '/get_cards_likes/',
                type: 'GET',
                data: {
                    'pet_id': petId,
                    'mutual_likes': mutual_likes
                },
                success: function(response) {
                    $('#card_likes').html(response.cards_html);
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при получении карточек животных');
                }
            });
        }
        else {
            $('#card_likes').empty();
        }
    });

    $('#id_mutual_likes').on('change', function() {
        var mutual_likes = $('#id_mutual_likes').prop('checked');
        var petId = $('input[name="pet"]:checked').val();
        if (petId) {
            $.ajax({
                url: '/get_cards_likes/',
                type: 'GET',
                data: {
                    'pet_id': petId,
                    'mutual_likes': mutual_likes
                },
                success: function(response) {
                    $('#card_likes').html(response.cards_html);
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при получении карточек животных');
                }
            });
        }
        else {
            $('#card_likes').empty();
        }
    });
});
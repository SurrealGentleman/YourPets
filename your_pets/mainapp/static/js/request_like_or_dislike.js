function request_like_or_dislike(name, card_id){
    $('input[name="pet"]').each(function() {
        if ($(this).is(':checked')) {
            var petId = $(this).val();
            var mutual_likes = $('#id_mutual_likes').prop('checked');
            if (name == 'dislike_btn'){
                $.ajax({
                    url: '/dislike/',
                    type: 'GET',
                    data: {
                        'petId': petId,
                        'card_id': card_id,
                    },
                    success: function(data) {
                        $('#card_likes').empty();
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
                                console.error('Ошибка при отправке запроса');
                            }
                        });
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка при отправке запроса');
                    }
                });
            }
            else if (name == 'like_btn'){
                $.ajax({
                    url: '/like/',
                    type: 'GET',
                    data: {
                        'petId': petId,
                        'card_id': card_id,
                    },
                    success: function(data) {
                        $('#card_likes').empty();
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
                                console.error('Ошибка при отправке запроса');
                            }
                        });
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка при отправке запроса');
                    }
                });
            }
        }
    });
}
function favorite_advice_card(advice_card_id){
    $('input[name="pet"]').each(function() {
        if ($(this).is(':checked')) {
            var petId = $(this).val();
            if ($('#'+advice_card_id).attr('class') == 'card_not_favorite'){
                $.ajax({
                    url: '/favorite_advice_card/',
                    type: 'GET',
                    data: {
                        'petId': petId,
                        'advice_card_id': advice_card_id,
                    },
                    success: function(data) {
                        add_favorite_class(advice_card_id)
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка при отправке запроса');
                    }
                });
            }
            else if ($('#'+advice_card_id).attr('class') == 'card_favorite'){
                $.ajax({
                    url: '/not_favorite_advice_card/',
                    type: 'GET',
                    data: {
                        'petId': petId,
                        'advice_card_id': advice_card_id,
                    },
                    success: function(data) {
                        remove_favorite_class(advice_card_id)
                    },
                    error: function(xhr, status, error) {
                        console.error('Ошибка при отправке запроса');
                    }
                });
            }

        }
    });
}

function add_favorite_class(card_id){
    $('#'+card_id).removeClass('card_not_favorite');
    $('#'+card_id).addClass('card_favorite');
}

function remove_favorite_class(card_id){
    $('#'+card_id).removeClass('card_favorite');
    $('#'+card_id).addClass('card_not_favorite');
}
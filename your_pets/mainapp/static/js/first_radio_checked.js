$(document).ready(function() {
    var $petInputs = $('input[name="id_pets"]');
    var $petLabels = $petInputs.next('label');

    // Устанавливаем последний input как выбранный по умолчанию
    $petInputs.last().prop('checked', true);

    // Добавляем класс darkening всем label, кроме последнего
    $petLabels.not(':last').addClass('darkening');

    // Обработчик события change для input[name=id_pets]
    $petInputs.on('change', function() {
        var $currentInput = $(this);
        var $currentLabel = $currentInput.next('label');

        // Если текущий input является последним
        if ($currentInput.is($petInputs.last())) {
            // Убираем класс darkening у текущего label
            $currentLabel.removeClass('darkening');

            // Добавляем класс darkening всем другим label
            $petLabels.not($currentLabel).addClass('darkening');
        } else {
            // Убираем класс darkening у текущего label
            $currentLabel.removeClass('darkening');

            // Добавляем класс darkening всем другим label, кроме последнего
            $petLabels.not($currentLabel).not(':last').addClass('darkening');
        }
    });
});
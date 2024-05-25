document.addEventListener('DOMContentLoaded', function() {
    var radioButtons = document.querySelectorAll('input[type="radio"]');
    console.log(radioButtons)
    if (radioButtons.length > 0) {
        radioButtons[0].checked = true;
        console.log(radioButtons[0].checked)
    }
    radioButtons.forEach(function(radioButton) {
        radioButton.addEventListener('change', function() {
            radioButtons.forEach(function(rb, i) {
                var label = rb.nextElementSibling;
                if (rb.checked) {
                    label.classList.remove('darkening');
                } else if (i !== radioButtons.length - 1) {
                    label.classList.add('darkening');
                }
            });
        });
    });
});

$(document).ready(function(){
    $('.open_popup').click(function(e) {
        e.preventDefault();
        $('html').addClass('no-scroll');
        $('.popUp-bg').fadeIn(500);

    });
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.popUp').length && !$(event.target).closest('.open_popup').length) {
            $('.popUp-bg').fadeOut(400);
            $('html').removeClass('no-scroll');
        }
    });
});

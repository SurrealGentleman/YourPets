$(document).ready(function(){
    $('.open_popup').click(function(e) {
        e.preventDefault();
        $('.popUp-bg').fadeIn(800);
        $('html').addClass('no-scroll');
    });
//    $('.close-popup').click(function() {
//        $('.popup-bg').fadeOut(800);
//        $('html').removeClass('no-scroll');
//    });
});

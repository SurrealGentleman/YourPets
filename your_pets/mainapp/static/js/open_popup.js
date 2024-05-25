$(document).ready(function() {

  // Получаем ссылки на формы
  var $form_register = $('#form_register');
  var $form_login = $('#form_login');
  var $form_change_password = $('#form_change_password')

  // Функция для открытия попапа и подсветки активной кнопки
  function openPopup(activeButton) {
    console.log(activeButton);
    $('html').addClass('no-scroll');
    $('.popUp-bg').fadeIn(500);
    $('.active').removeClass('active');
    if (activeButton=='register'){
      $form_register.show();
      $form_login.hide();
      $('.register').addClass('active');
    }
    else if(activeButton=='login'){
      $form_login.show();
      $form_register.hide();
      $('.login').addClass('active');
    } else if (activeButton=='changePassword'){
      $form_change_password.show();
    }
  }

  // Обработчик клика по кнопке открытия попапа
  $('.open_popup').click(function(e) {
    e.preventDefault();
    var $href =window.location.href.split('/');
    var $page = $href[$href.length - 2]
    if ($page == 'profile'){
      openPopup('changePassword');
    } else{
      openPopup('login'); // По умолчанию открываем форму "Вход"
      $('.login').addClass('active')
    }
  });

  // Обработчик клика по всему документу для закрытия попапа
  $(document).on('click', function(event) {
    if (!$(event.target).closest('.popUp').length && !$(event.target).closest('.open_popup').length) {
      $('.popUp-bg').fadeOut(400);
      $('html').removeClass('no-scroll');
    }
  });

  // Обработчик клика по кнопкам "Вход" и "Регистрация"
  $('.login, .register').click(function() {
    // Удаляем нижний бордюр у всех заголовков
    $('.active').removeClass('active');
    // Добавляем нижний бордюр к нажатой кнопке
    $(this).addClass('active');

    // Переключаем видимость форм
    if ($(this).hasClass('login')) {
      $form_login.show();
      $form_register.hide();
    } else if ($(this).hasClass('register')) {
      $form_register.show();
      $form_login.hide();
    }
  });

  // Проверяем наличие ошибок в формах при загрузке страницы
  console.log($('.errors li').length)
  if ($('.errors li').length) {
    if ($('#form_register .errors li').length) {
      openPopup('register'); // Открываем форму "Регистрация" при ошибках в ней
    } else if ($('#form_login .errors li').length) {
      openPopup('login'); // Открываем форму "Вход" при ошибках в ней
    } else if ($('#form_change_password .errors li').length){
      openPopup('changePassword');
    }
  }
});
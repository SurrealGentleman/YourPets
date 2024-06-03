$(document).ready(function(){
    // Включаем или отключаем отображение модального окна.
    const confirmModal = document.getElementById('confirmModal');
    const overlay = document.getElementById('overlay');
    const yesBtn = document.getElementById('yesBtn');
    const noBtn = document.getElementById('noBtn');

    // Устанавливаем обработчики на кнопки.
    yesBtn.addEventListener('click', () => {hideModal();});
    noBtn.addEventListener('click', () => { hideModal(); /* Код для "Нет" */ });
})

function showModal() {
    confirmModal.style.display = 'flex';
    $('html').addClass('no-scroll');
    $('.overlay').fadeIn(500);
}
function hideModal() { overlay.style.display = 'none'; }


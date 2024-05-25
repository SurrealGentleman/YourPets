$(document).ready(function(){
  $(document).on('click', '.photo-wrapper', function() {
    const photoInput = document.getElementById('id_photo');
    const photoPreview = document.getElementById('photo-preview');

    if (photoInput) {
      photoInput.click();
    }
  });

  $(document).on('change', '#id_photo', function() {
    const photoInput = document.getElementById('id_photo');
    const photoPreview = document.getElementById('photo-preview');

    const file = photoInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function() {
        if (photoPreview) {
          photoPreview.src = reader.result;
        }
      };
      reader.readAsDataURL(file);
    }
  });

  //Вывод фотографии при выборе в форме добавления питомца
  $(document).on('change', '#id_photo', function() {
    var photoInput = document.getElementById('id_photo');
    var previewImage = document.getElementById('preview-image');

    var file = photoInput.files[0];
    console.log(file)
    if (file) {
      var reader = new FileReader();
        reader.onload = function(e) {
          previewImage.src = e.target.result; // Устанавливаем src для изображения
          previewImage.style.display = 'block'; // Показываем изображение
          $('.plus-icon').hide(); // Скрываем иконку "плюс"
        }
      reader.readAsDataURL(file);
    }
  });
});
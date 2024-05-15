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
        photoPreview.src = reader.result;
      };
      reader.readAsDataURL(file);
    }
  });
});
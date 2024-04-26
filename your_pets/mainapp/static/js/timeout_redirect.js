$(document).ready(function() {
  if ($('.success').text()) {
    setTimeout(function() {
      window.location.href = "/profile/";
    }, 1000);
  }
});
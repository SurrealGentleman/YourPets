$(document).ready(function(){
    var checkbox = document.getElementById('id_search');
    var mission = document.getElementById('mission');

    if (checkbox.checked){
        mission.style.display = 'block';
    }
    else{
        mission.style.display = 'none';
    }

    checkbox.addEventListener('change', function(){
        if (checkbox.checked){
            mission.style.display = 'block';
        }
        else{
            mission.style.display = 'none';
        }
    });

});
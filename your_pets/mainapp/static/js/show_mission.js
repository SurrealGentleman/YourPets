$(document).ready(function(){
    var checkbox = $('#id_search');
    var mission = $('#mission');
    var mission_form_add = $('#mission_form_add');

    checkbox.change(function() {
        if (checkbox.is(':checked')) {
            mission.show();
            mission_form_add.show();
        } else {
            mission.hide();
            mission_form_add.hide();
        }
    });

    if (checkbox.is(':checked')) {
        mission.show();
        mission_form_add.show();
    } else {
        mission.hide();
        mission_form_add.hide();
    }
});
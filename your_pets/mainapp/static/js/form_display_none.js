$(document).ready(function(){
    var form_register_classes = document.getElementById("form_register").classList
    var form_login_classes = document.getElementById("form_login").classList
    $('.login').click(function(e){
        if(form_login_classes.contains("display_none")){
            form_login_classes.remove("display_none")
            form_register_classes.add("display_none")
        }
    });
    $('.register').click(function(e){
        if(form_register_classes.contains("display_none")){
            form_register_classes.remove("display_none")
            form_login_classes.add("display_none")
        }
    });
});

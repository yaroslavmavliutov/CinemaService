$(document).ready(function() {

    if (window.localStorage.getItem('isAdmin') == 'true') {
        $('#add_film_button').show();
    }

   $('#log_jwt').on('click', function(){
       console.log('gg');
       var auth = $('#auth_form');
       $('#menu-main').hide();
       auth.trigger('reset');
       auth.show();
   });


   $('#log_out').on('click', function(){
       window.localStorage.removeItem('token');
       window.localStorage.removeItem('username');
       window.localStorage.removeItem('isAdmin');
       $('#log_jwt').show();
       $('#log_out').hide();
       $('#reg_user').show();
       $('#add_film_button').hide();
   });

   $('#reg_user').on('click', function(){
           $('#main-page').hide();
           $('#reg_cont').show();
   });

   $('#add_film_button').on('click', function(){
           $('#main-page').hide();
           $('#post_cont').show();
   });

   $('#reg_form').on('submit', function(e){
       e.preventDefault();
       var data = {};
       data.username = $('#username_reg').val();
       data.password = $('#pass_reg').val();
       data.email = $('#email_reg').val();
              $.ajax({
             url: '/reg_form/',
             type: 'POST',
             data: data,
             cache: true,
             success: function (response) {
                 console.log("OK");
                 console.log(response);
                 var reg_form = $('#reg_form');
                 reg_form.trigger('reset');
                 reg_form.hide();
                 $('#main-page').show();
                 alert('Successfully registered');
             },
             error: function() {
                 console.log("Error! Try again");
             }
             });
   });

    $.ajax({
        url: '/users/',
             type: 'GET',
             cache: true,
             beforeSend: function(xhr) {
             xhr.setRequestHeader("Authorization", "JWT " + window.localStorage.getItem('token'));
             },
             success: function (response) {
                 console.log("OK");
                 console.log(response);
             },
             error: function() {
                 console.log("ERROR");
             }
    });
   $('#auth_form').on('submit', function (e) {
       e.preventDefault();
       var data = {};
       data.username = $('#username_form').val();
       data.password = $('#password_form').val();
       $.ajax({
             url: '/api/v1/auth/login/',
             type: 'POST',
             data: data,
             cache: true,
             success: function (response) {
                 console.log("OK");
                 console.log(response.token);
                 window.localStorage.setItem('token', response.token);
                 window.localStorage.setItem('log_user', data.username);
                 $('#menu-main').show();
                 $('#auth_form').hide();
                 $('#log_jwt').hide();
                 $('#log_out').show();
                 $('#reg_user').hide();
                 adminCheck();
             },
             error: function() {
                 console.log("ERROR");
                 $('#auth_form').trigger('reset');
                 alert('Wrong username or password');
             }
             });
   });

});
function adminCheck(){
    $.ajax({
       url: '/admin_check/',
       type: 'GET',
       cache: true,
       beforeSend: function(xhr) {
             xhr.setRequestHeader("Authorization", "JWT " + window.localStorage.getItem('token'));
             },
       success: function(response){
           window.localStorage.setItem('isAdmin', true);
           $('#add_film_button').show();
       },
       error: function() {
           window.localStorage.setItem('isAdmin', true);
           console.log('not adm');
       }
    });
}

$(function(){
var data = {};
       data.token = window.localStorage.getItem('token');
       $.ajax({
             url: '/api-token-verify/',
             type: 'POST',
             data: data,
             cache: true,
             success: function (response) {
                 console.log("OK");
                 console.log(response);
                 $('#log_out').show();
             },
             error: function() {
                 console.log("ERROR");
                 $('#log_jwt').show();
                 $('#reg_user').show();
             }
             });
});

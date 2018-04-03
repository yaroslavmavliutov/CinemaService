var bookings = [];
var pathname = window.location.pathname;
$(function(){

$('#btnSeating').on('click', createseating);
$('#bookPlace').on('click', function(e){
   e.preventDefault();
   var data = {};
   var path = pathname.replace('/', '');
   console.log(bookings);
   path = path.replace('/', '');
   data.film = path;
   data.customer = window.localStorage.getItem('log_user');
   for (var i = 0; i < bookings.length; i++){
       var place = bookings[i].split(" ");
       data.row = place[1];
       data.place = place[0];
       $.ajax({
             url: '/user_bookings/',
             type: 'POST',
             data: data,
             cache: true,
             beforeSend: function(xhr) {
             xhr.setRequestHeader("Authorization", "JWT " + window.localStorage.getItem('token'));
             },
             success: function (response) {
                 console.log("OK");
                 console.log(response);
                 alert('Booked!');
             },
             error: function() {
                 console.log("ERROR");

             }
             });
   }

});

});

function createseating(){
var k = 1;
 var seatingValue = [];
 for ( var i = 0; i < 10; i++){

    for (var j=0; j<5; j++){

        var seatingStyle = "<div class='seat available' id="+i+">" + k + "</div>";
        seatingValue.push(seatingStyle);
        k = k + 1;

         if ( j === 4){
        console.log("hi");
         var seatingStyle = "<div class='clearfix'></div>";
         k = 1;
        seatingValue.push(seatingStyle);



     }
  }

}

$('#messagePanel').html(seatingValue);
       $(function(){
            $('.seat').on('click',function(){
              if($(this).hasClass( "selected" )){
                $( this ).removeClass( "selected" );
                var k = bookings.indexOf($(this).text() + ' ' + $(this).attr('id'));
                bookings.splice(k, 1);
              }else{
                $( this ).addClass( "selected" );
                bookings.push($(this).text() + ' ' + $(this).attr('id'));
              }
              update_orders(bookings);
            });


            $('.seat').mouseenter(function(){
                $( this ).addClass( "hovering" );

                   $('.seat').mouseleave(function(){
                   $( this ).removeClass( "hovering" );

                   });
            });


       });

}

function update_orders(data){
    var field = $('#rowtickets');
    field.text('');
    for (var i = 0; i < data.length; i++){
        var place = data[i].split(" ");
        field.append('<p>' + "Place: "+ place[0] + '  Row: ' + place[1] + '</p>');
    }
}


$(function() {
   $.ajax({
       url: '/film_list/',
       type: 'GET',
       cache: true,
       success: function(response){
           console.log(response);
           listFiller(response);
       },
       error: function() {
           console.log('error');
       }
    });
   function listFiller(resp){
        for (var i = 0; i < resp.length; i++){
            $('#main-page .row').append(
                '        <div class="col-lg-3 col-md-4 col-sm-6 portfolio-item">\n' +
                '          <div class="card h-100">\n' +
                '            <a href="#"><img class="card-img-top" src="media/' + resp[i]['poster'] + '" alt=""></a>\n' +
                '            <div class="card-body">\n' +
                '              <h4 class="card-title">\n' +
                '                <a class="link_film" href="/' + resp[i]['id'] + '/">' + resp[i]['title'] + '</a>\n' +
                '              </h4>\n' +
                '              <p class="card-text">' +
                '<p> Genre: ' + resp[i]['genre'] + '</p>'+
                '<p> Premiere date: ' + resp[i]['premiere_date'] + '</p>'+
                '<p> Session time: ' + resp[i]['session_time'] + '</p>'+
                '<p> Price: ' + resp[i]['price'] + '</p>'+
                '</p>\n' +
                '            </div>\n' +
                '          </div>\n'

            )
        }
   }
   $('.link_film').on('click', function (e) {
       e.preventDefault();
       $('#main-page').empty();
       $('#main-page').append('<h1 class="my-4">'+ 1 +'</h1>');

   });
});
$(function() {
  var slider = $('#duration-range');
    slider.on('change', function(){
        var mnt = slider.val();
        var hours = Math.floor(mnt / 60);
        var minutes = mnt - (hours * 60);
        $('#duration-text').html(hours + '.' + minutes + ' hours');
        console.log(hours + '.' + minutes);
    });

    $('#submit_post').on('click', function(e){
        e.preventDefault();
        textForm();
        setTimeout(function(){
            myDropzone.processQueue();
            myDropzone.removeItem();
        }, 2000);

    });
    $('#price_field').inputmask("numeric", {
    radixPoint: ".",
    groupSeparator: ",",
    digits: 2,
    autoGroup: true,
    prefix: '$', //No Space, this will truncate the first character
    rightAlign: false,
    oncleared: function () { self.Value(''); }
});

});
function textForm(){
        var data = {};
        data.title = $('input[name=title]').val();
        data.description = $('textarea[name=description]').val();
        data.genre = $('input[name=genre]').val();
        data.premiere_date = $('input[name=premiere_date]').val();
        data.session_time = $('input[name=session_time]').val();
        data.film_duration = $('input[name=film_duration]').val();
        data.price = $('input[name=price]').val();
        var csrf_token = $('#post_form [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
             url: '/film/',
             type: 'POST',
             data: data,
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
}
Dropzone.autoDiscover = false;

        var myDropzone = new Dropzone('#post_img', {
          url: "/poster/",
          autoProcessQueue: false,
          addRemoveLinks: true,
          init: function() {
              this.on("sending", function (file, xhr, formData) {
                  formData.append("title", $('input[name=title]').val());
              });
              this.on("complete", function(file){
                  myDropzone.removeFile(file);

              })
          }
        });




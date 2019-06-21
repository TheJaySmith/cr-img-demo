$(document).ready(function(){

  $('#imgresult').hide();
  $('#imgup').hide();

  var authtoken = '';
  var jwtoken = '';
  var base_url = 'https://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience=';
  var backend_url = 'https://vision-ml-api-x5npa2r4oa-uc.a.run.app';
  var token_url = base_url + backend_url;


  /*$.get('tk.txt', function(data) {
    authtoken = $(data);
  });*/
  $('#imgshow').on('change', function(ev){
        $('#imgup').show();
        if ( $('td').length ) {
          $('td').remove();
        }

        var f = ev.target.files[0];
        var fr = new FileReader();

        fr.onload = function(ev2) {
                console.dir(ev2);
                $('#myimg1').attr('src', ev2.target.result);
        };

        fr.readAsDataURL(f);
  });


  $('#pressme').click(function(ev){
    var fd = $('#upload-image')[0];
    var form_data = new FormData(fd);
    $('#imgresult').show();


    $.ajax({
      type: 'post',
      url: "/ml",
      data: form_data,
      contentType: false,
      processData: false,
      crossDomain: true,
      enctype: 'multipart/form-data',
      success: function( response ){
        console.log(response);

        var json_obj = $.parseJSON(response);//parse JSON
        $(function(){
          $.each(json_obj, function(i, item){
            tbl= $('<tr><td>'+i+'</td><td>'+item+'</td></tr>')
            $('#mlresults').append(tbl);
          })
        });

      }
    })

  });

});

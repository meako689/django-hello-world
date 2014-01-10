$(document).ready(function() { 
$('#photo-clear_id').removeAttr('checked');
//callback handler for form submit
    $(".ajaxform").submit(function(e)
    {
        var form = $(this);
        var btn = form.find('.ajaxsubmit');
        if (btn.hasClass('enabled')){
            btn.removeClass('enabled');
            btn.html('Working');

            var postData = $(this).serializeArray();
            var formURL = $(this).attr("action");
            
            var options = {
                success:function(data, textStatus, jqXHR){
                    if (data.photo){
                        img = $('.photopreview');
                        img.show();
                        img.attr('src', data.photo)
                    }else{
                        $('.photopreview').hide()
                    }

                    btn.addClass('enabled');
                    btn.html('Submit');
                    $('#photo-clear_id').removeAttr('checked');
                    $('#id_photo').val("");
                    $('.error').remove();
                },
                error: function(jqXHR, textStatus, errorThrown){
                    data = JSON.parse(jqXHR.responseText);
                    for (var key in data) {
                        if (data.hasOwnProperty(key)) {
                            var matchdiv = $('#id_'+key);
                            var errordiv = '<div class="error">'+data[key]+'</div>';
                            $(errordiv).insertBefore(matchdiv);
                            btn.addClass('enabled');
                            btn.html('Submit');
                        }
                    }
                    $('#photo-clear_id').removeAttr('checked');
                }
            };
            $(this).ajaxSubmit(options);
        }
        e.preventDefault(); //STOP default action
    });
}); 

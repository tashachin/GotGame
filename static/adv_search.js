// CREDIT: http://jsfiddle.net/heera/Gyaue/

$(function(){
    $('#platform-options').on('change', function(){
        var val = $(this).val();
        var sub = $('#sub-options');
        if(val == 'Search by platform') {
            $('#sub-options').find('option').show();
        }
        else {
            sub.find('option').not(':first').hide();
            $('option', sub).filter(function(){
                if($(this).attr('data-group') == val){
                    $(this).show();
                }
            });
        }
        sub.val(0);
    });
});
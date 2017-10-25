$('#loginID, #password, #appID').bind('keyup', function() {
    if(allFilled())
        $('#create_user').removeAttr('disabled');
    else
        $('#create_user').prop("disabled", true);
});

function allFilled() {
    var filled = true;
    $('body input').each(function() {
        if($(this).val() == '') filled = false;
    });
    return filled;
}
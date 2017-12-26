$('#password').bind('keyup', function() {
    if(allFilled())
        $('#change_pass').removeAttr('disabled');
    else
        $('#change_pass').prop("disabled", true);
});

function allFilled() {
    var filled = true;
    $('#password').each(function() {
        if($(this).val().length < 8) filled = false;
    });
    return filled;
}
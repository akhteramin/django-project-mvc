$('#appID, #serviceID, #serviceCategory, #description').bind('keyup', function() {
    if(allFilled())
        $('#create_service').removeAttr('disabled');
    else
        $('#create_service').prop("disabled", true);
});

function allFilled() {
    var filled = true;
    $('body input').each(function() {
        if($(this).val() == '') filled = false;
    });
    return filled;
}
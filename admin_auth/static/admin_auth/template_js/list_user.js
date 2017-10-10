$('#postUserForm').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        $.ajax({
        url : "/admin_auth/change_password/", // the endpoint
        type : "POST", // http method
        data :  $(this).serialize() , // data sent with the post request
        dataType: 'json',

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $('#ChangePasswordModal').modal('hide');
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            // " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }

    })
});


function setData(loginID,appID){
    $("#loginHeader").html("<b>Login ID:  "+loginID+"</b>");
    $("#loginID").val(loginID);
    $("#appID").val(appID);
}
function changeStatus(loginID,appID,activate=1,userID){


    if(activate==0)
    {
        $("#deactivate_"+userID).prop('disabled', true);
        console.log(activate);
        $.ajax({
                url : "/admin_auth/deactivate_user/", // the endpoint
                type : "POST", // http method
                data :  {'loginID':loginID,'appID':appID} , // data sent with the post request
                dataType: 'json',
                "beforeSend": function(xhr, settings) {
                    console.log("Before Send");
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success : function(json) {
                    console.log(json); // log the returned json to the console
                    console.log("success"); // another sanity check

                    $("#deactivate_"+userID).remove();
                    $('#actionUser_'+userID).append(
                        "<a id='activate_"+userID+"' onclick="+"changeStatus('"+loginID+"','"+appID+"','1','"+userID+"')"+" href='#' class='btn button-activate'>Activate</a>"
                    );
                },
                error : function(xhr,errmsg,err) {

                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console

                }

            });
    }

     else{
      $("#activate_"+userID).prop('disabled', true);
        console.log(activate);
        $.ajax({
                url : "/admin_auth/activate_user/", // the endpoint
                type : "POST", // http method
                data :  {'loginID':loginID,'appID':appID} , // data sent with the post request
                dataType: 'json',
                "beforeSend": function(xhr, settings) {
                    console.log("Before Send");
                    $.ajaxSettings.beforeSend(xhr, settings);
                },

                success : function(json) {
                    console.log(json); // log the returned json to the console
                    console.log("success"); // another sanity check
                    $("#activate_"+userID).remove();
                    $('#actionUser_'+userID).append(
                        "<a id='deactivate_"+userID+"' onclick="+"changeStatus('"+loginID+"','"+appID+"','0','"+userID+"')"+" href='#' class='btn button-deactivate'>Dectivate</a>"

                    );


                },

                error : function(xhr,errmsg,err) {

                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console

                }

            });
     }
};
$("#login_id").change(function(){
    console.log($("#login_id").val());

    $("#prev_login_id").val($("#login_id").val());
    $("#next_login_id").val($("#login_id").val());

});

$("#app_id").change(function(){
console.log($("#app_id").val());

    $("#prev_app_id").val($("#app_id").val());
    $("#next_app_id").val($("#app_id").val());

})


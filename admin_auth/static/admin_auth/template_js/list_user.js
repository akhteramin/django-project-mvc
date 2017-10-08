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

$('#activateForm').on('submit', function(event){
        event.preventDefault();
        var formdata = $(this).serializeArray();
        var data = {};
        $(formdata).each(function(index, obj){
            data[obj.name] = obj.value;
        });
        console.log(data.activate);
        if(data.activate==0)
        {
            $.ajax({
                url : "/admin_auth/deactivate_user/", // the endpoint
                type : "POST", // http method
                data :  $(this).serialize() , // data sent with the post request
                dataType: 'json',

                // handle a successful response
                success : function(json) {
                    console.log(json); // log the returned json to the console
                    console.log("success"); // another sanity check
//                    $("#activate").style.visibility='visible';
//                    $("#deactivate").style.visibility='hidden';

                },

                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    // " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console

                }

            });
        }
        else
        {
            $.ajax({
                url : "/admin_auth/activate_user/", // the endpoint
                type : "POST", // http method
                data :  $(this).serialize() , // data sent with the post request
                dataType: 'json',

                // handle a successful response
                success : function(json) {
                    console.log(json); // log the returned json to the console
                    console.log("success"); // another sanity check
//                    $("#activate").style.visibility='hidden';
//                    $("#deactivate").style.visibility='visible';
                },

                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    // " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }

            });
        }

    });


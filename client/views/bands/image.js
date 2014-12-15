$('#image_form').submit(function (e) {
    e.preventDefault();

    upload(this, new FormData(this),
        function (result) {
            console.log("result", result);
            $("#image").html(result['image']);
            addMessage('info', 'Bandfoto erfolgreich hochgeladen');
        },
        function (errors) {
            console.log("errors", errors);
            createErrorMessages(errors);
        }
    );

});
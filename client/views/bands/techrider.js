$('#techrider_form').submit(function (e) {
    e.preventDefault();

    upload(this, new FormData(this),
        function (result) {
            console.log("result", result);
            $("#techrider").html(result['techrider']);
            addMessage('info', 'Techrider erfolgreich hochgeladen');
        },
        function (errors) {
            console.log("errors", errors);
            createErrorMessages(errors);

        }
    );

});
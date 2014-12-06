$('#band_form').submit(function (e) {
    e.preventDefault();

    submit(this,
        function (result) {
            addMessage('info', 'Profil erfolgreich geändert');
            console.log("ok");
        },
        function (errors) {
            createErrorMessages(errors);
            console.log("errors", errors);
        }
    );

});
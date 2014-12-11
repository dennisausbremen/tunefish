var onTrackDeleteClick = linkAjaxPostHandler(function (target) {
    target.parent().fadeOut(500);
});


$('#track_form').submit(function (e) {
    e.preventDefault();

    upload(this,
        function (result) {
            $("#track_list ul").append(result['track']).click(onTrackDeleteClick);
             addMessage('info', 'Track erfolgreich hochgeladen');
        },
        function (errors) {
            console.log("errors", errors);
            createErrorMessages(errors);
        }
    );

});

$('#track_list a').click(onTrackDeleteClick);
var onTrackDeleteClick = linkAjaxPostHandler(function (target) {
    target.parent().fadeOut(500);
});


$('#track_form').submit(function (e) {
    e.preventDefault();

    upload(this,
        function (result) {
            $("#track_list").html(result['track']);
             addMessage('info', 'Track erfolgreich hochgeladen');
        },
        function (errors) {
            console.log("errors", errors);
            createErrorMessages(errors);
        }
    );

});

$(document).on('click', '#track_list a', onTrackDeleteClick);
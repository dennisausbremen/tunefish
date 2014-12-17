var updateSelectedTracksList = function(field, spinner) {
    var selectedTracksList = $('#selected-tracks');

    // clear the list of selected files
    selectedTracksList.html('');

    var files = $(field).get(0).files;
    for (var i = 0, len = files.length; i < len; ++i) {
        var filename = files[i].name;
        if (spinner) {
            selectedTracksList.append('<li><span class="spinner"></span>' + filename + '</li>');
        } else {
            selectedTracksList.append('<li>' + filename + '</li>');
        }

        setEqualHeightCards();
    }
};

var removeTrackElement = function removeTrackElement(el){
    $('audio', el).remove();
    el.remove();
}

function updateSelectedTracksStatus(done) {
    var selectedTracksList = $('span', '#selected-tracks');

    selectedTracksList.removeClass('spinner');
    if (done) {
        selectedTracksList.html('<i class="i-done"></i>');
    } else {
        selectedTracksList.html('<i class="i-close"></i>');
    }
}

var onTrackDeleteClick = linkAjaxPostHandler(function (target) {
    var el = target.parent();
    el.fadeOut(500, removeTrackElement);
});

$('#track_form').submit(function (e) {
    e.preventDefault();

    var formdata = new FormData(this);
    var audio = $('#audioFile', this);

    // get file list from audioFiles-input
    var files = audio.get(0).files;

    // assign the selected files to the formdata
    for (var i = 0, len = files.length; i < len; ++i) {
        var file = files[i];
        formdata.append('audioFile', file);
    }

    updateSelectedTracksList(audio, true);

    $("input[type=submit]", this).attr('disabled', 'disabled').css('opacity', '0.55');


    upload(this, formdata,
        function (result) {
            updateSelectedTracksStatus(true);
            $("#track_list").html(result['track']);
             addMessage('info', 'Track erfolgreich hochgeladen');
            $("input[type=submit]").removeAttr('disabled').css('opacity', '1.0');
        },
        function (errors) {
            updateSelectedTracksStatus(false);
            console.log("errors", errors);
            $("input[type=submit]").removeAttr('disabled').css('opacity', '1.0');
            createErrorMessages(errors);
        }
    );

});

$("#audioFile", '#track_form').change(function() {
    updateSelectedTracksList(this, false);
});

$(document).on('click', '#track_list a', onTrackDeleteClick);

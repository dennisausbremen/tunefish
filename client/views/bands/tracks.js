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

function updateSelectedTracksStatus(data) {
    var selectedTracksList = $('#selected-tracks');
    var selectedTracksListInfo = $('span', selectedTracksList);

    selectedTracksListInfo.removeClass('spinner');

    data.success.forEach(function(filename) {
        var track = $( "li:contains('" + filename + "')", selectedTracksList);
        $("span", track).html('<i class="i-done"></i>');
        track.delay(5000)
            .velocity('transition.slideDownOut', 250), function() {
            setEqualHeightCards();
        };
    });

    data.fail.forEach(function(filename) {
        var track = $( "li:contains('" + filename + "')", selectedTracksList);
        $("span", track).html('<i class="i-close"></i>');
    });
}

var onTrackDeleteClick = linkAjaxPostHandler(function (target) {
    var el = target.parents('li');
    el
        .velocity({'opacity': 0}, 250)
        .velocity({'height': 0}, 250, function() {
            el.remove();
            checkStepState('#step-music','i-audio','Keine Musik hochgeladen');
        });

    setTimeout(function() {
        setEqualHeightCards();
    }, 500);

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
            $("#track_list").html(result['track']);
            addMessage('info', 'Track erfolgreich hochgeladen');
            updateSelectedTracksStatus(result);
            $("input[type=submit]").removeAttr('disabled').css('opacity', '1.0');

            setEqualHeightCards();
        },
        function (errors) {
            updateSelectedTracksStatus(errors);
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

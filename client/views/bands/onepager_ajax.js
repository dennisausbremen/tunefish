$(document).ready(function() {
    var upload = function (form, onSuccess, onFailure) {
        clearMessages();
        $.ajax({
            url: form.action,
            type: 'POST',
            data: new FormData(form),
            mimeType: 'multipart/form-data',
            contentType: false,
            cache: false,
            dataType: 'json',
            processData: false,
            success: function(data) {
                updateCheckTab(data);
                onSuccess(data);
            }
        }).fail(function (data) {
            console.log(data);
            if ( typeof data.responseJSON !== 'undefined' ) {
                onFailure(data.responseJSON.errors);
            } else {
                onFailure([]);
            }
            });
    };

    var submit = function (form, onSuccess, onFailure) {
        clearMessages();
        $.post(form.action, $(form).serialize(), function(data) {
            updateCheckTab(data);
            onSuccess(data);
        }).fail(function (data) {
            onFailure(data.responseJSON.errors);
        });
    };

    var linkAjaxPostHandler = function(onSuccess) {
        return function (e) {
            clearMessages();
            e.preventDefault();
            var target = $(e.target);
            $.post(e.target.href, function(data) {
                updateCheckTab(data);
                onSuccess(target, data);
            });
        };
    };

    var addMessage = function(type, message) {
        $("#messages").append('<div class="' + type + '">' + message + '</div>');
    };

    var clearMessages = function() {
        $("#messages").html('');
    };

    var createErrorMessages = function(errors) {
        for (field in errors) {
            errors[field].forEach(function (error) {
                addMessage('error', 'Fehler im Feld ' + field + ': ' + error);
            });
        }
    };

    {% include "profile.js" %}
    {% include "tracks.js" %}
    {% include "image.js" %}
    {% include "techrider.js" %}


    function updateCheckTab(data) {
        if (data['check_tab'] !== 'undefined')
            $('#summary').html(data['check_tab']);
    }

    $('.tabs>div').hide();
    $('.tabs>div:nth-child(1)').show().addClass('active');

    $('.tabctrl a').click(function(e) {
        e.preventDefault();

        $('.tabs>div').hide();
        $('.tabctrl a').removeClass('active');
        $('.tabs>div:nth-child('+ $(this).data("index") + ')').show().addClass('active');
        $(this).addClass('active');

    });
});

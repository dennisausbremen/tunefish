$(document).ready(function() {
    var upload = function (form, onSuccess, onFailure) {
        $.ajax({
            url: form.action,
            type: 'POST',
            data: new FormData(form),
            mimeType: 'multipart/form-data',
            contentType: false,
            cache: false,
            dataType: 'json',
            processData: false,
            'success': onSuccess
        }).fail(function (data) {
                onFailure(data.responseJSON.errors);
            });
    };

    var submit = function (form, onSuccess, onFailure) {
        $.post(form.action, $(form).serialize(), onSuccess).fail(function (data) {
            onFailure(data.responseJSON.errors);
        });
    };

    var linkAjaxPostHandler = function(onSuccess) {
        return function (e) {
            e.preventDefault();
            var target = $(e.target);
            $.post(e.target.href, function(data) {
                onSuccess(target, data);
            });
        };
    };

    {% include "profile.js" %}
    {% include "tracks.js" %}
});

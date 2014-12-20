$(document).ready(function() {
    var upload = function (form, formData, onSuccess, onFailure) {
        clearMessages();

        $.ajax({
            url: form.action,
            type: 'POST',
            data: formData,
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
            var target = $(e.currentTarget);
            $.post(target.context.href, function(data) {
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

    var setEqualHeightCards = function setEqualHeightCards() {
        $('.slick-slide').css('height','auto').setAllToMaxHeight();
    };

    var checkStepState = function checkStepState(step,icon,msg) {

        var el = $(''+step),
            list = $('li', el),
            files = $('.uploaded-files', el);

        console.log('check ', el, ' list ', list, ' length ', list.length);

        if (!list.length) {
            var html = '<div class="missing-files"><i class="' + icon + '"></i><h3>' + msg + '</h3></div>';
            files.css({'display': 'none'});
            $('h2',el).append(html);
        }
    };

    {% include "profile.js" %}
    {% include "tracks.js" %}
    {% include "image.js" %}
    {% include "techrider.js" %}


    function updateCheckTab(data) {
        if (data['check_tab'] !== 'undefined')
            $('#step-summary').html(data['check_tab']);
    }

});

$.fn.setAllToMaxHeight = function(){
    return this.height( Math.max.apply(this, $.map( this , function(e){ return $(e).height() }) ) );
}

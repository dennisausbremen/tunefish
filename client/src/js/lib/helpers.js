var helper = (function ($) {
    'use strict';

    /*
     PRIVATE FUNCTIONS
     */

    /**
     * Login Page
     */
    var setActivePanel = function setActiveTab(target) {
        var tabs = $('.tabs'),
            children = tabs.children().length,
            steps = 100/children,
            tab = tabs.find('a'),
            idx = target.parent().index(),
            content = $('.form-action-wrapper');

        tab.removeClass('active');
        tab.eq(idx).addClass('active');

        content.css('transform','translate3d(-'+ (steps * idx) +'%,0,0)');
    };

    var setLoginContainerHeight = function setLoginContainerHeight() {
        var i = $('.tabs a.active').parent().index();
        var th = $('.tabs').outerHeight();
        var h = $('.form-action-wrapper .form-action').eq(i).outerHeight();
        $('.login-container').height(th+h);
    };

    var checkInvalidLogin = function checkInvalidLogin() {
        var target = $('.fail').parents('.form-action').attr('id');


        if (target) {
            setActivePanel($('[href=#'+target+']'));
        }
        setLoginContainerHeight();
    };

    var initTabs = function initTabs() {
        $(document).on('click','.tabs a:not(.active)',function(){
            var el = $(this),
                target = el.attr('href');

            setActivePanel($('[href='+target+']'));
            setLoginContainerHeight();
            return false;
        });
    };


    /**
     * Profile Page
     */

    //FORM FUNCTIONS
    var upload = function upload (form, formData, onSuccess, onFailure) {
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
            //console.log(data);
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

    var linkAjaxPostHandler = function linkAjaxPostHandler(onSuccess) {
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

    var addMessage = function addMessage(type, message) {
        $('#messages').append('<div class="' + type + '">' + message + '</div>');
    };

    var addErrorMessage = function addErrorMessage (field,error) {
        addMessage('error', 'Fehler im Feld ' + field + ': ' + error);
    };

    var clearMessages = function() {
        $('#messages').html('');
    };

    var createErrorMessages = function(errors) {
        for (var field in errors) {
            addErrorMessage(field, errors[field]);
        }
    };

    function updateCheckTab(data) {
        if (data.check_tab !== 'undefined') {
            $('#step-summary').html(data.check_tab);
            updateStepState();
        }
    }

    var checkStepState = function checkStepState(step,icon,msg) {

        var el = $(''+step),
            files = $('.uploaded-files', el);

        if (!$('li',el).length) {
            var missing = $('.missing-files', el);
            var html = '<i class="' + icon + '"></i><h3>' + msg + '</h3>';
            files.addClass('animated').removeAttr('style');
            missing.html(html).removeAttr('style');

            missing.delay(250).velocity('transition.slideDownIn',500);
        }
    };


    var setEqualHeightCards = function setEqualHeightCards() {
        $('.slick-slide').css('height','auto').setAllToMaxHeight();
    };

    var setAppBg = function setAppBg() {
        var bg = $('.main'),
            active = $('.slick-center').attr('id'),
            bgClasses = [];

        bg.addClass(active);
        bgClasses = bg.attr('class').split(' ');

        if (/step/i.test(bg.attr('class')) && (bgClasses.length-1) > 2) {
            bg.removeClass(bgClasses[2]);
        }
    };

    var setArrows = function setArrows() {
        var next = $('.slick-center').next().next();
        var prev = $('.slick-center').prev().prev();

        var nextLabel = $('.slick-next .arrow-label');
        var prevLabel = $('.slick-prev .arrow-label');

        if (next) {
            nextLabel
                .velocity('transition.slideRightOut', 250, function(){
                    $('.slick-next').removeClass('slick-disabled');
                });
        }

        if (prev) {
            prevLabel
                .velocity('transition.slideLeftOut', 250, function(){
                    $('.slick-prev').removeClass('slick-disabled');
                });
        }
    };

    var setArrowTexts = function setArrowTexts() {
        var next = $('.slick-center').next().find('h2').text();
        var prev = $('.slick-center').prev().find('h2').text();

        var nextLabel = $('.slick-next .arrow-label');
        var prevLabel = $('.slick-prev .arrow-label');

        if (next) {
            nextLabel
                .text(next)
                .velocity('transition.slideLeftIn', 250);
        }  else {
            nextLabel
                .velocity('transition.slideRightOut', 250, function(){
                    $('.slick-next').addClass('slick-disabled');
                });
        }

        if (prev) {
            prevLabel
                .text(prev)
                .velocity('transition.slideRightIn', 250);
        }  else {
            prevLabel
                .velocity('transition.slideLeftOut', 250, function(){
                    $('.slick-prev').addClass('slick-disabled');
                });
        }
    };

    var triggerFileUploadDialogue = function triggerFileUploadDialogue(e) {
        var el = $(e.target);
        el.next('input[type=file]').trigger('click');
    };

    var initCards = function initCards() {
        var sliderWrap = $('.profile-form-wrapper'),
            elms = null;

        sliderWrap.slick({
            infinite: false,
            speed: 250,
            slidesToShow: 1,
            centerMode: true,
            centerPadding: 0,
            arrows: true,
            prevArrow: '<button type="button" class="slick-prev"><span class="arrow-label"></span></button>',
            nextArrow: '<button type="button" class="slick-next"><span class="arrow-label">Musik</span></button>',
            dots: false,
            responsive: [
                {
                    breakpoint: 737,
                    settings: {
                        arrows: false
                    }
                },
                {
                    breakpoint: 736,
                    settings: {
                        arrows: false,
                        centerMode: true,
                        centerPadding: 0,
                        slidesToShow: 1,
                        adaptiveHeight: true
                    }
                }
            ],
            onInit: function(){
                setAppBg();
            },
            onBeforeChange: function(){
                setArrows();
            },
            onAfterChange: function(){
                setArrowTexts();
                setAppBg();
            }
        });

        setEqualHeightCards();
        updateStepState();


        $(document).on('click','.fg-upload',triggerFileUploadDialogue);

        $(window).on('resize',setEqualHeightCards);
    };

    var updateStepState = function updateStepState() {
        var items = $('#check-overview li');

        for (var i = 0, len = items.length; i < len; ++i) {
            var item = $(items.get(i)),
                itemID = item.attr('id').split('check-')[1],
                itemState = $('i', item).attr('class'),
                stepStateEl = $('#'+itemID+' i');

            if (stepStateEl.attr('class')) {
                stepStateEl.removeAttr('class').addClass(itemState);
            } else {
                stepStateEl.addClass(itemState);
            }


        }
    };

    var updateSelectedFilesList = function(field, spinner) {
        var form = $(field).parents('form'),
            selectedTracksList = $('.uploads--list', form),
            uploads = $(field).get(0).files;

        selectedTracksList.html('');
        for (var i = 0, len = uploads.length; i < len; ++i) {
            var filename = uploads[i].name;
            if (spinner) {
                selectedTracksList.append('<li><span class="spinner"></span>' + filename + '</li>');
            } else {
                selectedTracksList.append('<li>' + filename + '</li>');
            }
        }

        selectedTracksList.css({'display':'block','opacity': 1});
        setEqualHeightCards();
    };

    /*
     forEach Update from Git. -Nonsense, b/c called once same time-
     */
    function updateSelectedListStatus(data, form) {
        var selectedTracksList = $('.uploads--list', form);
        var selectedTracksListInfo = $('span', selectedTracksList);

        console.log(data);

        selectedTracksListInfo.removeClass('spinner');

        if (data.success || data.fail) {

            data.success.forEach(function (filename) {
                var track = $('li:contains("' + filename + '")', selectedTracksList);
                $('span', track).html('<i class="i-done"></i>');
                track
                    .delay(1000)
                    .velocity('transition.slideDownOut', 250, function () {
                        setEqualHeightCards();
                    });
            });

            data.fail.forEach(function (filename) {
                var track = $('li:contains("' + filename + '")', selectedTracksList);
                $('span', track).html('<i class="i-close"></i>');
            });

        } else if (data.general) {

            selectedTracksListInfo.html('<i class="i-close"></i>');

        } else {
            selectedTracksListInfo.html('<i class="i-done"></i>');
            selectedTracksList
                .delay(1000)
                .velocity('transition.slideDownOut', 250, function() {
                    setEqualHeightCards();
                });
        }
    }

    var loadDataURL = function loadDataURL(file, elem) {
        return function(e) {
            var image = e.target.result,
                replaceImages = $('.account-image img, #image img');

            replaceImages.velocity({opacity: 0},250,function(){
                replaceImages.attr('src',image);
            }).delay(250).velocity({opacity: 1}, 250);
        };
    };

    var handleFileSelect = function handleFileSelect(e){
        if(typeof FileReader === 'undefined') {
            return true;
        }

        var elem = $(e);
        var files = e.files;

        for (var i=0, l = files.length; i<l; i++) {
            var file = files[i];
            if (file.type.match('image.*') && elem.parents('form').is('#image_form')) {
                var reader = new FileReader();
                reader.onload = (loadDataURL(file, elem, 'image'));
                reader.readAsDataURL(file);
            }
            //else if (file.type.match('application.pdf') && elem.parents('form').is('#techrider_form')) {
            //    //console.log('pdf');
            //} else if (file.type.match('audio.mp3') && elem.parents('form').is('#track_form')) {
            //    //console.log('mp3');
            //}
        }
    };

    var initFileUploads = function initFileUploads() {
        //FileReader API Call
        $('input[type=file]').on('change', function(){
            handleFileSelect(this);
            updateSelectedFilesList(this, false);
        });
    };

    var initFormSubmits = function initFormSubmits() {

        /*
        PROFILE
         */

        $('#band_form').submit(function (e) {
            e.preventDefault();

            submit(this,
                function (result) {
                    addMessage('info', 'Profil erfolgreich geändert');
                    //console.log('ok');
                },
                function (errors) {
                    createErrorMessages(errors);
                    //console.log('errors', errors);
                }
            );

        });


        /*
        TRACKS
         */

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

        $(document).on('click', '#track_list a', onTrackDeleteClick);

        //SUBMIT
        $('#track_form').submit(function (e) {
            e.preventDefault();

            var self = $(this),
                slide = $(this).parent(),
                formdata = new FormData(this),
                fileInput = $('#audioFile', this);

            // get file list from audioFiles-input
            var files = fileInput.get(0).files;

            // assign the selected files to the formdata
            for (var i = 0, len = files.length; i < len; ++i) {
                var file = files[i];
                formdata.append('audioFile', file);
            }

            updateSelectedFilesList(fileInput, true);

            $('input[type=submit]', this).attr('disabled', 'disabled').css('opacity', '0.55');


            upload(this, formdata,
                function (result) {

                    updateSelectedListStatus(result, self);
                    $('#track_list').html(result.track);
                    addMessage('info', 'Track erfolgreich hochgeladen');
                    $('input[type=submit]').removeAttr('disabled').css('opacity', '1.0');

                    $('.missing-files', slide)
                        .delay(1000)
                        .velocity('transition.slideUpOut',250, function(){
                            if ($('.uploaded-files', self).is(':hidden')) {
                                $('.uploaded-files', slide)
                                    .velocity('transition.slideDownIn',250, function() {
                                        setEqualHeightCards();
                                    });
                            }
                        });

                },
                function (errors) {
                    updateSelectedListStatus(errors, self);
                    $('input[type=submit]').removeAttr('disabled').css('opacity', '1.0');
                    createErrorMessages(errors);
                }
            );

        });


        /*
        IMAGE
         */

        $('#image_form').submit(function (e) {
            e.preventDefault();

            var self = $(this),
                fileInput = $('#image_file');

            updateSelectedFilesList(fileInput, true);

            upload(this, new FormData(this),
                function (result) {
                    updateSelectedListStatus(result, self);
                    $('#image').html(result.image);
                    addMessage('info', 'Bandfoto erfolgreich hochgeladen');
                },
                function (errors) {
                    updateSelectedListStatus(errors, self);
                    createErrorMessages(errors);
                }
            );

        });


        /*
        TECHRIDER
         */

        $('#techrider_form').submit(function (e) {
            e.preventDefault();

            var self = $(this),
                fileInput = $('#techrider_file');

            updateSelectedFilesList(fileInput, true);

            upload(this, new FormData(this),
                function (result) {
                    console.log(result);
                    updateSelectedListStatus(result, self);
                    $('#techrider').html(result.techrider);
                    addMessage('info', 'Techrider erfolgreich hochgeladen');
                },
                function (errors) {
                    updateSelectedListStatus(errors, self);
                    createErrorMessages(errors);

                }
            );

        });




    };

    /*
     PAGE SPECIFIC PRIVATE FUNCTIONS
     */
    var App = {
        init: function initGlobalFuncs() {
            $(document).on('ajaxComplete messageChange', Messages.init);
            initFileUploads();
            initFormSubmits();

            if ($('#messages div').length) {
                $(document).trigger('messageChange');
            }
        }
    };

    var Login = {
        init: function initLoginPage() {
            checkInvalidLogin();
            initTabs();
        }
    };

    var Profile = {
        init: function initProfilePage() {
            initCards();
        }
    };

    var Messages = {
        init: function initMessages(){
            var messageContainer = $('#messages'),
                messages = $('div', messageContainer);

            messages
                .velocity('transition.slideDownIn',{stagger:250})
                .delay(5000)
                .velocity('transition.slideUpOut',{stagger: 250, backwards:true});

        }
    };


    /*
     PUBLIC FUNCTION EXPORTS
     */
    return {
        /*
         PUBLIC FUNCTIONS HERE
         */
        App: App,
        Login: Login,
        Profile: Profile,
        Messages: Messages
    };

})(jQuery, window);


$.fn.setAllToMaxHeight = function(){
    'use strict';
    var h = $(window).height()+5;
    if ($(window).width() > 767) {
        var max = Math.max.apply(this, $.map( this , function(e){ return $(e).outerHeight(); }) );

        if (h>max) {
            return this.height(h);
        } else {
            return this.height(max);
        }
    }
};

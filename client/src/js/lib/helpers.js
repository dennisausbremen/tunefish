var helper = (function ($) {
    "use strict";

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
    var setEqualHeightCards = function setEqualHeightCards() {
        $('.slick-slide').css('height','auto').setAllToMaxHeight();
    };

    var setArrowTexts = function setArrowTexts() {
        var next = $('.slick-center').next().find('h2').text();
        var prev = $('.slick-center').prev().find('h2').text();

        var nextLabel = $('.slick-next .arrow-label');
        var prevLabel = $('.slick-prev .arrow-label');

        if (next) {
            nextLabel.text(next);
            $('.slick-next').removeClass('slick-disabled');
        } else {
            $('.slick-next').addClass('slick-disabled');
        }

        if (prev) {
            prevLabel.text(prev);
        }

    };

    var triggerFileUploadDialogue = function triggerFileUploadDialogue(e) {
        var el = $(e.target);
        el.next('input[type=file]').trigger('click');
    };

    var initCards = function initCards() {
        $('.profile-form-wrapper').slick({
            infinite: false,
            slidesToShow: 1,
            centerMode: true,
            arrows: true,
            prevArrow: '<button type="button" class="slick-prev"><span class="arrow-label">Zurück</span></button>',
            nextArrow: '<button type="button" class="slick-next"><span class="arrow-label">Vor</span></button>',
            dots: true,
            responsive: [
                {
                    breakpoint: 767,
                    settings: {
                        arrows: false,
                    }
                },
                {
                    breakpoint: 481,
                    settings: {
                        arrows: false,
                        centerMode: true,
                        centerPadding: '40px',
                        slidesToShow: 1
                    }
                }
            ],
            onInit: function(){
                setArrowTexts();
            },
            onAfterChange: function(){
                setArrowTexts();
            }
        });

        setEqualHeightCards();

        $(document).on('click','.fg-upload',triggerFileUploadDialogue);

        $(window).on('resize',setEqualHeightCards);
    };

    /*
     PAGE SPECIFIC PRIVATE FUNCTIONS
     */
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


    /*
     PUBLIC FUNCTION EXPORTS
     */
    return {
        /*
         PUBLIC FUNCTIONS HERE
         */
        Login: Login,
        Profile: Profile
    };

})(jQuery, window);


$.fn.setAllToMaxHeight = function(){
    return this.height( Math.max.apply(this, $.map( this , function(e){ return $(e).height() }) ) );
}

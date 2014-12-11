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

        content.css('transform','translate3d('+ (steps * idx)*-1 +'%,0,0)');
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
            setActivePanel('#'+target);
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
    var initCards = function initCards() {
        $('.profile-form-wrapper').slick({
            centerMode: true,
            centerPadding: '20%',
            infinite: false,
            slidesToShow: 1,
            arrows: false,
            dots: true,
            responsive: [
                {
                    breakpoint: 1024,
                    settings: {
                        centerPadding: '15%'
                    }
                },
                {
                    breakpoint: 480,
                    settings: {
                        centerPadding: '10%'
                    }
                },
                {
                    breakpoint: 320,
                    settings: {
                        centerPadding: '30px'
                    }
                }
            ]
        });
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

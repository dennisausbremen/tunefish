var helper = (function ($) {
    "use strict";

    /*
     PRIVATE FUNCTIONS
     */
    var setActivePanel = function setActiveTab(target) {
        var tabs = $('.tabs'),
            children = tabs.children().length,
            steps = 100/children,
            tab = tabs.find('a'),
            idx = $(target).index(),
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

            setActivePanel(target);
            setLoginContainerHeight();
            return false;
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


    /*
     PUBLIC FUNCTION EXPORTS
     */
    return {
        /*
        PUBLIC FUNCTIONS HERE
         */
        Login: Login
    };

})(jQuery, window);

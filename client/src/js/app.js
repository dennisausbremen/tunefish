var tf = (function ($) {
    'use strict';

    //Import helpers
    var helper = window.helper || {};

    /*
    PRIVATE FUNCTIONS
     */
    var _init = function _init() {
        console.log('init');

        var setLoginContainerHeight = function setLoginContainerHeight() {
            var i = $('.tabs a.active').parent().index();
            var th = $('.tabs').outerHeight();
            var h = $('.form-action-wrapper .form-action').eq(i).outerHeight();

            $('.login-container').height(th+h);
        };

        setLoginContainerHeight();

        $(document).on('click','.tabs a:not(.active)',function(){
            var el = $(this),
                idx = el.parent().index(),
                tabs = el.parents('.tabs'),
                children = tabs.children().length,
                steps = 100/children,
                tab = tabs.find('a'),

                content = $('.form-action-wrapper');

            tab.removeClass('active');
            el.addClass('active');

            setLoginContainerHeight();

            content.css('transform','translate3d('+ (steps * idx)*-1 +'%,0,0)');

            return false;
        });
    };

    /*
    PUBLIC FUNCTION EXPORTS
     */
    return {
        init: _init
    };

})(jQuery, window);


//Initialize all the scripts!!!
tf.init();


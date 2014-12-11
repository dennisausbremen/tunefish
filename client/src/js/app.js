var tf = (function ($) {
    'use strict';

    //Import helpers
    var helper = window.helper || {};

    /*
    PRIVATE FUNCTIONS
     */
    var _init = function _init() {

        if ($('.login').length) {
           tf.helper.Login.init();
        }

        if ($('.profile').length) {
            tf.helper.Profile.init();
        }

    };

    /*
    PUBLIC FUNCTION EXPORTS
     */
    return {
        init: _init,
        helper: helper
    };

})(jQuery, window);


//Initialize all the scripts!!!
tf.init();


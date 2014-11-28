var tf = (function ($) {
    'use strict';

    //Import helpers
    var helper = window.helper || {};

    /*
    PRIVATE FUNCTIONS
     */
    var _init = function _init() {
        console.log('init');
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


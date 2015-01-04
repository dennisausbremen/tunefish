jQuery(document).ready(function($){
    'use strict';

    //set animation timing
    var animationDelay = 2500;


    var initHeadline = function initHeadline() {
        animateHeadline($('.headline'));
    };

    var setContainerWidth = function setContainerWidth() {
        var width = $('.words-wrapper .is-visible').width();
        $('.words-wrapper').css('width', width);
    };

    var animateHeadline = function animateHeadline($headlines) {
        var duration = animationDelay;
        $headlines.each(function(){
            var headline = $(this);
            //trigger animation
            setTimeout(function(){ hideWord( headline.find('.is-visible').eq(0) );  }, duration);
        });
    };

    var hideWord = function hideWord($word) {
        var nextWord = takeNext($word);

        switchWord($word, nextWord);
        setTimeout(function(){ hideWord(nextWord); }, animationDelay);
    };

    var takeNext = function takeNext($word) {
        return (!$word.is(':last-child')) ? $word.next() : $word.parent().children().eq(0);
    };

    var switchWord = function switchWord($oldWord, $newWord) {
        $oldWord.removeClass('is-visible').addClass('is-hidden');
        $newWord.removeClass('is-hidden').addClass('is-visible');

        setContainerWidth();
    };

    //Init Headline Switch
    initHeadline();

});

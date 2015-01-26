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


    var initScriptsAfterLoad = function initScriptsAfterLoad(){
        //MIXITUP!
        alert('foo');
        $('#container').mixItUp();
    };


    var App = {
      init: function initAmberApp () {

          //INIT MESSAGES
          $(document).on('ajaxComplete messageChange', Messages.init);

          if ($('#messages div').length) {
              $(document).trigger('messageChange');
          }


          $('.band-tile').velocity('transition.slideUpIn',500,{stagger: true});

          window.Tunefish = Ember.Application.create({
              rootElement: '#app_container'
          });

          Ember.LinkView.reopen({
              attributeBindings: ['data-sort','data-voted']
          });

          Tunefish.Router.map(function () {
              this.resource('bands', { path: '/' });
              this.resource('band', { path: '/:band_id'});
          });


          Tunefish.BandsRoute = Ember.Route.extend({
              model: function () {
                  return $.getJSON('/vote/ajax/bands').then(function (data) {
                      return data.bands;
                  });
              }
          });

          Tunefish.BandRoute = Ember.Route.extend({
              model: function (params) {
                  return $.getJSON('/vote/ajax/bands/' + params.band_id);
              }
          });

          Tunefish.BandController = Ember.ObjectController.extend({
              comment: '',

              actions : {
                  'vote' : function(vote) {
                      var self = this;
                      $.post('/vote/ajax/bands/vote', {
                          'band_id' : this.get('model.id'),
                          'vote': vote
                      }).then(function (result) {
                          self.set('model.vote_count', result.vote_count);
                          self.set('model.vote_average', result.vote_average);
                      });
                  },

                  'addComment': function() {
                      var self = this;
                      $.post('/vote/ajax/comments/add', {
                          'band_id' : this.get('model.id'),
                          'comment' : this.get('comment')
                      }).then(function (result) {
                          self.get('model.comments').pushObject(result);
                          self.set('comment', ' ');
                      });
                  }
              }
          });

          Tunefish.BandgridView = Ember.View.extend({
              didInsertElement: function() {
                  this.$().mixItUp({
                      selectors: {
                          target: '.band-tile'
                      },
                      animation: {
                          duration: 700,
                          effects: 'fade translateY(50px) rotateX(-30deg) stagger(35ms)',
                          //easing: 'cubic-bezier(0.86, 0, 0.07, 1)',
                          reverseOut: true
                      },
                  });
              }
          });
      }
    };

    var Login = {
        init: function initLoginPage() {
            checkInvalidLogin();
            initTabs();
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
        Messages: Messages
    };

})(jQuery, window);

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



    var App = {
      init: function initAmberApp () {
          //INIT MESSAGES
          $(document).on('ajaxComplete messageChange', Messages.init);

          if ($('#messages div').length) {
              $(document).trigger('messageChange');
          }


          window.Tunefish = Ember.Application.create({
              rootElement: '#app_container'
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
                  },

                  'calcDistance': function() {
                      var self = this;
                      console.log(this.get('model.city'));

                      $.post('/vote/ajax/distance', {
                            'band_id' : this.get('model.id')
                          }
                      ).then(function(result) {
                          console.log(result);
                      });
                      $("button#calcDist").text('55 km');

                  }


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

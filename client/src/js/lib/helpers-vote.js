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
            steps = 100 / children,
            tab = tabs.find('a'),
            idx = target.parent().index(),
            content = $('.form-action-wrapper');

        tab.removeClass('active');
        tab.eq(idx).addClass('active');

        content.css('transform', 'translate3d(-' + (steps * idx) + '%,0,0)');
    };

    var setLoginContainerHeight = function setLoginContainerHeight() {
        var i = $('.tabs a.active').parent().index();
        var th = $('.tabs').outerHeight();
        var h = $('.form-action-wrapper .form-action').eq(i).outerHeight();
        $('.login-container').height(th + h);
    };

    var checkInvalidLogin = function checkInvalidLogin() {
        var target = $('.fail').parents('.form-action').attr('id');


        if (target) {
            setActivePanel($('[href=#' + target + ']'));
        }
        setLoginContainerHeight();
    };

    var initTabs = function initTabs() {
        $(document).on('click', '.tabs a:not(.active)', function () {
            var el = $(this),
                target = el.attr('href');

            setActivePanel($('[href=' + target + ']'));
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

          Ember.LinkView.reopen({
              attributeBindings: ['data-sort','data-voted']
          });

          Tunefish.ApplicationStore = DS.Store.extend();

          Tunefish.Router.map(function () {
              this.resource('bands', { path: '/' });
              this.resource('band', { path: '/:band_id'});
          });

            Tunefish.ApplicationAdapter = DS.RESTAdapter.extend({
                namespace: 'vote/ajax'
            });

            Tunefish.Band = DS.Model.extend({
                name: DS.attr('string'),
                members: DS.attr('number'),
                city: DS.attr('string'),
                website: DS.attr('string'),
                facebookUrl: DS.attr('string'),
                youtubeUrl: DS.attr('string'),
                descp: DS.attr('string'),
                image: DS.attr('string'),
                thumbnail: DS.attr('string'),
                voteCount: DS.attr('number'),
                voteAverage: DS.attr('number'),
                voted: DS.attr('boolean'),
                ownVote: DS.attr('number'),
                comments: DS.hasMany('comment'),
                tracks: DS.hasMany('track')
            });

            Tunefish.Comment = DS.Model.extend({
                author: DS.attr('string'),
                timestamp: DS.attr('string'),
                message: DS.attr('string'),
                band: DS.belongsTo('band')
            });

            Tunefish.Track = DS.Model.extend({
                trackname: DS.attr('string'),
                url: DS.attr('string'),
                band: DS.belongsTo('band')
            });

            Tunefish.QueueitemView = Ember.View.extend({
                tagName: 'li',
                classNameBindings: ['isPlaying:playing'],
                isPlaying: function () {
                    return this.get('item.index') === this.get('controller.currentIndex');
                }.property('item', 'controller.currentIndex')
            });

            Tunefish.Router.map(function () {
                this.resource('main', {'path': '/'}, function () {
                    this.resource('bands', { path: '/bands/' });
                    this.resource('band', { path: '/bands/:band_id'});
                });
            });

            Tunefish.BandsRoute = Ember.Route.extend({
                model: function () {
                    return this.store.find('band');
                }
            });


            Tunefish.BandRoute = Ember.Route.extend({
                model: function (params) {
                    return this.store.find('band', params.band_id);
                }
            });


            Tunefish.MainController = Ember.ObjectController.extend({
                tracks: [],
                currentIndex: -1,
                current: null,
                currentTime: 0,
                currentDuration: 0,
                playerState: 'idle',
                player: function () {
                    return document.getElementById('#tunefishPlayer');
                },
                actions: {
                    vote: function (vote) {
                        var current = this.get('current');
                        if (current === null) {
                            return;
                        }
                        var band = current.get('band');
                        band.set('ownVote', vote);
                        band.save();
                    },
                    addTrack: function (track) {
                        var currentIndex = this.get('currentIndex');
                        var tracks = this.get('tracks');

                        tracks.pushObject({
                            'index': tracks.length,
                            'track': track
                        });
                        if (currentIndex < 0 && tracks.length > 0) {
                            this.send('next');
                            this.send('play');
                        }
                    },
                    jumpTo: function (index) {
                        var tracks = this.get('tracks');

                        if (index >= 0 && index < tracks.length) {
                            this.set('currentIndex', index);
                            this.set('current', tracks.get(index).track);
                        }
                    },
                    play: function () {
                        var self = this;
                        var currentIndex = this.get('currentIndex');
                        var $player = $('#tunefishPlayer');
                        if (currentIndex === -1) {
                            return;
                        }

                        this.set('playerState', 'playing');
                        $player.attr('autoplay', 'autoplay');
                        $player.get(0).play();
                        $player.on('ended', function () {
                            self.send('next');
                        });
                        $player.on('timeupdate', function() {
                            self.set('currentTime', Math.ceil($player.get(0).currentTime));
                            self.set('currentDuration', Math.ceil($player.get(0).duration));
                        });

                    },
                    pause: function () {
                        var $player = $('#tunefishPlayer');

                        $player.removeAttr('autoplay');
                        $player.get(0).pause();
                        $player.off('ended');
                        $player.off('timeupdate');
                        this.set('playerState', 'idle');
                    },
                    next: function () {
                        var currentIndex = this.get('currentIndex');
                        var tracks = this.get('tracks');

                        if (currentIndex < tracks.length - 1) {
                            this.set('currentIndex', currentIndex + 1);
                            this.set('current', tracks.get(currentIndex + 1).track);
                        }
                    },
                    prev: function () {
                        var currentIndex = this.get('currentIndex');
                        var tracks = this.get('tracks');

                        if (currentIndex > 0) {
                            this.set('currentIndex', currentIndex - 1);
                            this.set('current', tracks.get(currentIndex - 1).track);
                        }
                    }

                }
            });


            Tunefish.BandController = Ember.ObjectController.extend({
                needs: ['main'],
                comment: '',

                actions: {
                    vote: function (vote) {
                        var band = this.get('model');
                        band.set('ownVote', vote);
                        band.save();
                    },

                    addComment: function () {
                        var comment = this.store.createRecord('comment', {
                            message: this.get('comment'),
                            band: this.get('model')
                        });
                        comment.save();
                    },
                    addTrack: function (track) {
                        this.get('controllers.main').send('addTrack', track);
                    },
                    calcDistance: function () {
                        $.post('/vote/ajax/distance', {
                                'band_id': this.get('model.id')
                            }
                        ).then(function (result) {
                                $('button#calcDist').text(result.distance);
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
        init: function initMessages() {
            var messageContainer = $('#messages'),
                messages = $('div', messageContainer);

            messages
                .velocity('transition.slideDownIn', {stagger: 250})
                .delay(5000)
                .velocity('transition.slideUpOut', {stagger: 250, backwards: true});

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

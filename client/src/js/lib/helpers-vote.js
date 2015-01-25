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
        init: function initAmberApp() {
            //INIT MESSAGES
            $(document).on('ajaxComplete messageChange', Messages.init);

            if ($('#messages div').length) {
                $(document).trigger('messageChange');
            }


            window.Tunefish = Ember.Application.create({
                rootElement: '#app_container'
            });

            Tunefish.ApplicationStore = DS.Store.extend();

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

            Tunefish.Router.map(function () {
                this.resource('main', {'path': '/'}, function() {
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
                current: null,
                actions: {
                    addTrack: function(track) {
                        this.set('current', track);
                        this.get('tracks').pushObject(track);
                    }
                }
            });


            Tunefish.BandController = Ember.ObjectController.extend({
                needs: ['main'],
                comment: '',

                actions : {
                    vote : function(vote) {
                        var band = this.get('model');
                        band.set('ownVote', vote);
                        band.save();
                    },

                    addComment: function() {
                        var comment = this.store.createRecord('comment', {
                            message: this.get('comment'),
                            band: this.get('model')
                        });
                        console.log(comment);
                        comment.save();
                    },
                    addTrack: function(track) {
                        this.get('controllers.main').send('addTrack', track);
                    },
                    calcDistance: function() {
                        $.post('/vote/ajax/distance', {
                                'band_id' : this.get('model.id')
                            }
                        ).then(function(result) {
                                $('button#calcDist').text(result.distance);
                            });
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

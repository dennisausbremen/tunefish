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
                distance: DS.attr('number'),
                voted: DS.attr('boolean'),
                ownVote: DS.attr('number'),
                comments: DS.hasMany('comment'),
                tracks: DS.hasMany('track'),
                bandBG: function() {
                    return 'background-image: url(\''+this.get('image') + '\');';
                }.property('image'),
                map: function() {
                     return 'http://maps.googleapis.com/maps/api/staticmap?key=AIzaSyDRzrscCqKGd66mLS6jOayfUw9d4SICKOY&markers=' + this.get('city') + '&zoom=10&size=550x300&sensor=false';
                }.property('city')
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

            Ember.LinkView.reopen({
                attributeBindings: ['data-sort', 'data-voted']
            });

            Tunefish.VotecontrolsView = Ember.View.extend({
                templateName: 'votecontrols',
                classNames: ['voting']
            });

            Tunefish.StarView = Ember.View.extend(Ember.ViewTargetActionSupport, {
                tagName: 'a',
                templateName: 'star',
                classNameBindings: ['active'],
                attributeBindings: ['href'],
                href: '#',
                active: function () {
                    return this.get('band.ownVote') >= this.get('vote');
                }.property('band.ownVote', 'vote'),
                click: function() {
                    this.triggerAction({
                        action: 'vote',
                        actionContext: this.get('vote')
                    });
                    return false;
                }
            });


            Tunefish.MainView = Ember.View.extend({
                 didInsertElement: function () {

                    // slide up the band image for a proper view of the queue on small screens
                    var slidedUp = false;
                    var slideUpElem = $('#playerSlideUp');

                    slideUpElem.on('click', function() {
                        if (slidedUp) {
                            $('.player-image').slideDown();
                            slidedUp = false;
                        } else {
                            $('.player-image').slideUp();
                            slidedUp = true;
                        }
                    });

                    var seek = document.getElementById('seek');
                    var audio = document.getElementById('tunefishPlayer');

                    var seekBlocked, audioPaused = false;

                    function createRangeInputChangeHelper(range, inputFn, changeFn) {
                        var inputTimer, releaseTimer, isActive;

                        var destroyRelease = function() {
                            clearTimeout(releaseTimer);
                            range.removeEventListener('blur', releaseRange, false);
                            document.removeEventListener('mouseup', releaseRange, false);
                        };

                        var setupRelease = function () {
                            if (!isActive) {
                                destroyRelease();
                                isActive = true;
                                range.addEventListener('blur', releaseRange, false);
                                document.addEventListener('mouseup', releaseRange, true);
                            }
                        };

                        var _releaseRange = function () {
                            if (isActive) {
                                destroyRelease();
                                isActive = false;
                                if (changeFn) {
                                    changeFn();
                                }
                            }
                        };

                        var releaseRange = function () {
                            setTimeout(_releaseRange, 9);
                        };

                        var onInput = function () {
                            if (inputFn) {
                                clearTimeout(inputTimer);
                                inputTimer = setTimeout(inputFn);
                            }
                            clearTimeout(releaseTimer);
                            releaseTimer = setTimeout(releaseRange, 999);
                            if (!isActive) {
                                setupRelease();
                            }
                        };

                        range.addEventListener('input', onInput, false);
                        range.addEventListener('change', onInput, false);

                    }

                     function onSeek() {
                         if (!seekBlocked) {
                             seekBlocked = true;
                             audioPaused = audio.paused;
                             audio.pause();
                         }
                         audio.currentTime = seek.value;
                     }

                     function onSeekRelease() {
                         if (!audioPaused) {
                             audio.play();
                         }
                         seekBlocked = false;
                     }

                     createRangeInputChangeHelper(seek, onSeek, onSeekRelease);
                 }
            });

            Tunefish.QueueitemView = Ember.View.extend({
                tagName: 'li',
                classNameBindings: ['isPlaying:playing'],
                isPlaying: function () {
                    return this.get('item.index') === this.get('controller.currentIndex');
                }.property('item', 'controller.currentIndex')
            });

            Tunefish.BandsingleView = Ember.View.extend({
                tagName: 'div',
                classNames: ['content-area band-view'],
                didInsertElement: function () {
                    $('#tunefish_loading').hide();
                }
            });

            Tunefish.BandgridView = Ember.View.extend({
                tagName: 'div',
                classNames: ['content-area band-grid'],
                didInsertElement: function () {
                    $('#tunefish_loading').hide();

                    // TODO add me for funky animations
                    /*
                    this.$().mixItUp({
                        selectors: {
                            target: '.band-tile'
                        },
                        animation: {
                            duration: 700,
                            effects: 'fade translateY(50px) stagger(25ms)',
                            //easing: 'cubic-bezier(0.86, 0, 0.07, 1)',
                            reverseOut: true
                        }
                    });
                    */
                }
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


            function shuffleArray(array) {
            // see http://stackoverflow.com/a/2450976
                var currentIndex = array.length, temporaryValue, randomIndex;
                while (0 !== currentIndex) {

                    // Pick a remaining element...
                    randomIndex = Math.floor(Math.random() * currentIndex);
                    currentIndex -= 1;

                    // And swap it with the current element.
                    temporaryValue = array[currentIndex];
                    array[currentIndex] = array[randomIndex];
                    array[randomIndex] = temporaryValue;
                }
            }

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
                setTitle: function () {
                    var track = this.get('tracks').get(this.currentIndex).track;
                    var trackname = track.get('trackname');
                    var bandname = track.get('band').get('name');
                    document.title = 'tunefish | "' + trackname + '" by ' + bandname;
                },
                actions: {
                    vote: function (vote) {
                        var current = this.get('current');
                        if (current === null) {
                            return;
                        }

                         // close voting
                        var now = new Date().getTime();
                        var end = new Date(2015,3,1,16).getTime();

                        if(end < now) {
                            alert('Das Voting ist beendet. Deine Stimme wird nicht mehr gezählt!');
                            return;
                        }

                        var band = current.get('band');
                        band.set('ownVote', vote);
                        band.save();
                    },
                    clear: function() {
                        var tracks = this.get('tracks');

                        this.send('pause');
                        this.set('current', null);
                        this.set('currentIndex', -1);
                        this.set('currentTime', '0');
                        this.set('currentDuration', '0');
                        tracks.clear();
                        document.title = 'tunefish';

                    },
                    addTrack: function (track, autoplay) {
                        autoplay = typeof autoplay !== 'undefined' ? autoplay : true;

                        var currentIndex = this.get('currentIndex');
                        var tracks = this.get('tracks');

                        tracks.pushObject({
                            'index': tracks.length,
                            'track': track
                        });
                        if (currentIndex < 0 && tracks.length > 0) {
                            this.send('next');
                            if (autoplay) {
                                this.send('play');
                            }
                        }
                    },
                    jumpTo: function (index) {
                        var tracks = this.get('tracks');

                        if (index >= 0 && index < tracks.length) {
                            this.set('currentIndex', index);
                            this.set('current', tracks.get(index).track);
                            this.setTitle();
                        }
                    },
                    play: function () {
                        var self = this;
                        var currentIndex = this.get('currentIndex');
                        var $player = $('#tunefishPlayer');
                        if (currentIndex === -1) {
                            return;
                        }
                        this.setTitle();

                        this.set('playerState', 'playing');
                        $player.attr('autoplay', 'autoplay');
                        $player.get(0).play();
                        $player.on('ended', function () {
                            self.send('next');
                        });
                        $player.on('timeupdate', function () {
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
                        document.title = 'tunefish | paused';
                    },
                    next: function () {
                        var currentIndex = this.get('currentIndex');
                        var tracks = this.get('tracks');

                        if (currentIndex < tracks.length - 1) {
                            this.set('currentIndex', currentIndex + 1);
                            this.set('current', tracks.get(currentIndex + 1).track);
                            this.setTitle();
                        }
                    },
                    prev: function () {
                        var currentIndex = this.get('currentIndex');
                        var tracks = this.get('tracks');

                        if (currentIndex > 0) {
                            this.set('currentIndex', currentIndex - 1);
                            this.set('current', tracks.get(currentIndex - 1).track);
                            this.setTitle();
                        }
                    },

                    addUnvotedTracks: function () {
                        var self = this;
                        this.store.findAll('band').then(function(bands) {
                            bands.forEach(function(band) {
                                var voted = band.get('voted');
                                if(!voted) {
                                    var tracks = band.get('tracks');
                                    var length = tracks.get('length');
                                    var idx = Math.floor(Math.random() * length);
                                    var track = tracks.objectAt(idx);

                                    self.send('addTrack', track, false);
                                }
                            });
                        });
                    },


                    showRandomUnvotedBand: function (router) {
                        var self = this;
                        this.store.findAll('band').then(function(bands) {
                            var unvoted = [];
                            bands.forEach(function(band) {
                                var voted = band.get('voted');
                                if(!voted) {
                                    unvoted.push(band);
                                }
                            });

                            if (unvoted.length === 0) {
                                alert('Glückwunsch! Du hast bereits alle Bands bewertet!');
                                return true;
                            }

                            var randomBand = Math.floor(Math.random()* unvoted.length);
                            self.transitionToRoute('band', unvoted[randomBand].get('id'));

                        });
                    },

                    shuffle: function() {
                        var tracks = [];
                        var shuffledTracks = [];
                        this.get('tracks').forEach(function(track) {
                            shuffledTracks.pushObject(track.track);
                        });

                        shuffleArray(shuffledTracks);
                        for (var i = 0; i < shuffledTracks.length; i++) {
                            tracks.pushObject({
                                index: i,
                                track: shuffledTracks[i]
                            });
                        }

                        this.set('tracks', tracks);
                        this.send('jumpTo', 0);

                    }
                }

            });





            Tunefish.BandController = Ember.ObjectController.extend({
                needs: ['main'],
                comment: '',

                actions: {
                    vote: function (vote) {
                         // close voting
                        var now = new Date().getTime();
                        var end = new Date(2015,3,1,16).getTime(); // month -1!!!

                        if(end < now) {
                            alert('Das Voting ist beendet. Deine Stimme kann leider nicht mehr gezählt werden!');
                            return;
                        }

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
                        this.set('comment', '');
                    },

                    addAllTracks: function () {
                        var self = this;
                        var tracks = this.get('model.tracks');

                        tracks.forEach(function(track){
                            self.get('controllers.main').send('addTrack', track);
                        });
                    },

                    addTrack: function (track) {
                        this.get('controllers.main').send('addTrack', track);
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

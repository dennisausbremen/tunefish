var tunefish = angular.module('tunefishApp', ['ngRoute', 'angularSoundManager']);
var apiBase = 'http://localhost:5000/vote/api/v2/';

tunefish.config(function ($routeProvider) {
    $routeProvider
        .when('/', {templateUrl: 'bands.html'})
        .when('/stats', {templateUrl: 'stats.html'})
        .when('/results', {templateUrl: 'results.html'})
        .when('/login', {templateUrl: 'login.html'})
        .when('/playlist', {templateUrl: 'playlist.html'})
        .when('/band/:bandID', {templateUrl: 'band.html'})
        .otherwise({redirectTo: '/'});
});


tunefish.controller('MainCtrl', function ($scope, $location, BandFactory, angularPlayer, JwtFactory) {
    $scope.searchBand = function () {
        $location.path('/');
    };

    $scope.minRating = 0;
    $scope.maxRating = 5;

    $scope.setRating = function (min, max) {
        $scope.minRating = min;
        $scope.maxRating = max;
    }

    $scope.allToPlaylist = function (filteredBands) {
        angular.forEach(filteredBands, function (band) {
            BandFactory.getBand(band.id).then(function (fullBand) {
                fullBand.tracks.forEach(function (track) {
                    track.url = track.url + '?Authorization=JWT%20' + JwtFactory.getToken();
                    angularPlayer.addTrack(track);
                });
            });

        });
    }

});

tunefish.filter('ownRating', function () {
    return function (values, minRating, maxRating) {
        var filtered = [];
        angular.forEach(values, function (value) {
            if (value.rating <= maxRating && value.rating >= minRating) {
                filtered.push(value);
            }
        });
        return filtered;
    }
});

tunefish.controller('LoginCtrl', function ($scope, $http, $sce, $location, JwtFactory) {
   // $scope.user = {username: 'test', password: 'testtest'};
    $scope.login = function (user) {
        $scope.feedback = '';

        JwtFactory.determineToken(user).then(function (result) {
            if (result) {
                $scope.feedback = $sce.trustAsHtml('<div class="alert alert-success">Login erfolgreich!</div>');
                $location.path('/');
            } else {
                $scope.feedback = $sce.trustAsHtml('<div class="alert alert-danger">Falsche Zugangsdaten</div>');
            }
        });
    }

});

tunefish.controller('BandsCtrl', function ($scope, $location, BandsFactory, JwtFactory) {
    if (JwtFactory.hasToken()) {
        BandsFactory.getBands().then(function (bands) {
            $scope.bands = bands;
        });
    }
});


tunefish.controller('BandCtrl', function ($scope, $routeParams, $http, $sce, angularPlayer, BandsFactory, BandFactory, JwtFactory) {

    var band = {};
    if (JwtFactory.hasToken()) {

        band = BandsFactory.getBand($routeParams.bandID);
        $scope.band = band;
        $scope.loading = true;

        BandFactory.getBand($routeParams.bandID).then(function (gotBand) {
            band = gotBand;
            $scope.band = band;

            band.tracks.forEach(function (track) {
                track.url = track.url + '?Authorization=JWT%20' + JwtFactory.getToken();
            });

            $scope.description = $sce.trustAsHtml(band.description);
            $scope.loading = false;


        });

        $scope.saveComment = function (comment) {
            var success = function (commentData) {
                band.comments.push(commentData.data.comment);
            };

            var fail = function (commentData) {
                // TODO handle error case
                console.log('error occured while savin comment: ', comment);
            };
            $http.post(apiBase + "bands/" + band.id + "/comment", {'comment': comment}, JwtFactory.getHeaders()).then(success, fail);
        }
    }
});

tunefish.controller('JWTCheckCtrl', function (JwtFactory) {
    JwtFactory.hasToken();
});


tunefish.factory('JwtFactory', function ($http, $location) {
    var jwt = undefined;

    return {
        determineToken: function (user) {
            var success = function (response) {
                jwt = response.data.access_token;
                return true;
            };

            var error = function () {
                return false;
            };

            return $http.post(apiBase + "auth", user).then(success, error);
        },

        hasToken: function () {
            if (jwt == undefined) {
                $location.path('/login');
            }
            return jwt != undefined;
        },

        clearToken: function () {
            jwt = undefined;
        },

        getToken: function () {
            return jwt;
        },

        getHeaders: function () {
            return {headers: {'Authorization': 'JWT ' + jwt}};
        }
    }
});


tunefish.factory('BandFactory', function ($http, $q, $location, JwtFactory) {

    var bandCache = [];
    var bands = [];
    return {
        getBand: function (bandId) {
            // -- check if band is in local cache ...
            // necessary for voting, as else the reference for the band object in the
            // track objects is no longer given and so the votes on the band page aren't
            // updated

            if (bandId in bandCache) {
                // TODO: But maybe reload the comments?
                var deferred = $q.defer();
                deferred.resolve(bandCache[bandId]);
                return deferred.promise;
            }

            var success = function (bandResponse) {
                band = bandResponse.data;
                band.tracks.forEach(function (track) {
                    track.band = band;
                });

                bandCache[band.id] = band;
                return band;
            };

            var fail = function (bandResponse) {
                if (bandResponse.status == 401) {
                    $location.path('/login');
                }
                // TODO: In other cases?
                console.log('Bands couldn\'t be fetched ...');
            };

            return $http.get(apiBase + 'bands/' + bandId, JwtFactory.getHeaders()).then(success, fail);
        }
    };
});


tunefish.factory('BandsFactory', function ($http, $q, $location, JwtFactory) {
    var bands = [];
    return {
        getBand: function (bandId) {
            var singleBand = {artist: '', id: bandId};

            bands.forEach(function (band) {
                if (band.id == bandId) {
                    singleBand = band;
                }
            });

            singleBand.mocked = true;

            return singleBand;
        },
        getBands: function () {
            if (bands.length == 0) {
                var success = function (bandResponse) {
                    bands = bandResponse.data.bands;
                    return bands;
                };

                var fail = function (bandResponse) {
                    if (bandResponse.status == 401) {
                        $location.path('/login');
                    }
                    // TODO: In other cases?
                    console.log('Bands couldn\'t be fetched ...');
                };

                return $http.get(apiBase + 'bands', JwtFactory.getHeaders()).then(success, fail);
            }

            var deferred = $q.defer();
            deferred.resolve(bands);
            return deferred.promise;
        },
        setRating: function (bandId, rating) {
            bands.forEach(function (band) {
                if (band.id == bandId) {
                    band.rating = rating;
                }
            });
        }
    };
});

tunefish.directive('voting', function () {
    return {
        restrict: 'E',
        scope: {
            band: '='
        },
        template: '<span ng-repeat="cnt in [1,2,3,4,5]"><star digit="cnt" band="band"></star></span>'
    };
});

tunefish.directive('star', function ($http, JwtFactory, BandsFactory) {
    return {
        restrict: 'E',
        scope: {
            digit: '=',
            band: '='
        },
        link: function (scope, element) {
            element.bind('click', function () {

                var success = function () {
                    scope.band.rating = scope.digit;
                    BandsFactory.setRating(scope.band.id, scope.digit);
                };

                var fail = function () {
                    // TODO: notify the user?, check whether token was still valid
                    console.log('voting failed');
                };

                $http.put(apiBase + 'bands/' + scope.band.id + '/vote', {vote: scope.digit}, JwtFactory.getHeaders()).then(success, fail);
            });
        },
        template: '<i class="glyphicon " ng-class="{\'glyphicon-star\': digit <= band.rating, \'glyphicon-star-empty\': digit > band.rating}"></i>'
    };
});


tunefish.directive('addAll', ['angularPlayer', function (angularPlayer) {
    return {
        restrict: "EA",
        scope: {
            songs: '=addAll'
        },
        link: function (scope, element) {
            element.bind('click', function () {
                //add songs to playlist
                for (var i = 0; i < scope.songs.length; i++) {
                    angularPlayer.addTrack(scope.songs[i]);
                }

                if (!angularPlayer.isPlayingStatus()) {
                    angularPlayer.play();
                }
            });
        }
    }
}]);


tunefish.directive('random', ['angularPlayer', function (angularPlayer) {
    return {
        restrict: "EA",
        scope: {
            songs: '=random'
        },
        link: function (scope, element) {
            element.bind('click', function () {
                alert('need to implement random');
            });
        }
    }
}]);

// https://gist.github.com/marshall007/6039852#gistcomment-945767
tunefish.directive('timeago', function () {
    var getTimeAgo, template, templates;
    templates = {
        seconds: 'vor einigen Sekunden',
        minute: 'vor einer Minute',
        minutes: 'vor %d Minuten',
        hour: 'vor einer Stunde',
        hours: 'vor %d Studen',
        day: 'vor einem Tag',
        days: 'vor %d Tagen',
        month: 'vor einem Monat',
        months: 'vor %d Monaten',
        year: 'vor einem Jahr',
        years: 'vor %d Jahren'
    };
    template = function (name, value) {
        var ref;
        return (ref = templates[name]) != null ? ref.replace(/%d/i, Math.abs(Math.round(value))) : void 0;
    };
    getTimeAgo = function (time) {
        var d2 = new Date(Date.parse(time));

        var days, hours, minutes, now, seconds, years;
        if (!time) {
            return 'Never';
        }
        time = time.replace(/\.\d+/, '');
        time = time.replace(/-/, '/').replace(/-/, '/');
        time = time.replace(/T/, ' ').replace(/Z/, ' UTC');
        time = time.replace(/([\+\-]\d\d)\:?(\d\d)/, ' $1$2');
        time = new Date(time * 1000 || time);

        now = new Date;

        seconds = ((now.getTime() - time) * .001) >> 0;

        minutes = seconds / 60;
        hours = minutes / 60;
        days = hours / 24;
        years = days / 365;
        if (seconds < 30) {
            return template('seconds', seconds);
        }
        if (seconds < 90) {
            return template('minute', 1);
        }
        if (minutes < 45) {
            return template('minutes', minutes);
        }
        if (minutes < 90) {
            return template('hour', 1);
        }
        if (hours < 24) {
            return template('hours', hours);
        }
        if (hours < 42) {
            return template('day', 1);
        }
        if (days < 30) {
            return template('days', days);
        }
        if (days < 45) {
            return template('month', 1);
        }
        if (days < 365) {
            return template('months', days / 30);
        }
        if (years < 1.5) {
            return template('year', 1);
        }
        return template('years', years);
    };
    return {
        restrict: 'E',
        replace: true,
        template: '<time datetime="{{time}}" title="{{time|date:\'medium\'}}">{{timeago}}</time>',
        scope: {
            time: "="
        },
        controller: [
            '$scope', '$interval', function ($scope, $interval) {
                $scope.timeago = getTimeAgo($scope.time);
                return $interval(function () {
                    return $scope.timeago = getTimeAgo($scope.time);
                }, 30000);
            }
        ]
    };
});

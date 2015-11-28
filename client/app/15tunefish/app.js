var tunefish = angular.module('tutorialApp', ['ngAnimate', 'ngRoute', 'angularSoundManager']);
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


tunefish.controller('LoginCtrl', function ($scope, $http, $sce, $location, JwtFactory) {
    $scope.user = {username: 'ebroda', password: ''};
    $scope.login = function (user) {
        $scope.feedback = '';

        JwtFactory.determineToken(user).then(function (result) {
            if (result) {
                $scope.feedback = $sce.trustAsHtml('<div class="alert alert-success">Login erfolgreich!</div>');
                $location.path('/bands');
            } else {
                $scope.feedback = $sce.trustAsHtml('<div class="alert alert-danger">Falsche Zugangsdaten</div>');
            }
        });
    }

});

tunefish.controller('BandsCtrl', function ($scope, $location, Bands, JwtFactory) {
    if (JwtFactory.hasToken()) {
        Bands.getBands().then(function (bands) {
            $scope.bands = bands;
        });
    }
});


tunefish.controller('BandCtrl', function ($scope, $routeParams, angularPlayer, $sce, Bands, BandFactory, JwtFactory) {

    var band = {};
    if (JwtFactory.hasToken()) {
        band = Bands.getBand($routeParams.bandID);;
        $scope.band = band;
        $scope.loading = true;

        BandFactory.getBand($routeParams.bandID).then(function (gotBand) {
            band = gotBand;
            $scope.band = band;

            band.tracks.forEach(function(track) {
                track.url = track.url + '?Authorization=JWT%20' + JwtFactory.getToken()
            });

            $scope.description = $sce.trustAsHtml(band.description);
            $scope.loading = false;
        });
    }

    $scope.addAll = function() {
        band.tracks.forEach(function(track) {
            angularPlayer.addTrack(track);
        });
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
    var bands = [];
    return {
        getBand: function (bandId) {
            var success = function (bandResponse) {
                return bandResponse.data;
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


tunefish.factory('Bands', function ($http, $q, $location, JwtFactory) {
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
        }
    };
});

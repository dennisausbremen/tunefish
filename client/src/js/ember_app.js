window.Tunefish = Ember.Application.create({
    rootElement: '#app_container'
});

Tunefish.Router.map(function () {
    this.resource('main', {'path': '/main'}, function() {
        this.resource('bands', { path: '/bands/' });
        this.resource('band', { path: '/:band_id'});
    });
});


Tunefish.MainController = Ember.ObjectController.extend({
    index: -1,
    tracks: [],
    actions : {
        "addTrack" : function(track) {
            this.get('tracks').pushObject(track);
        }
    }
});

Tunefish.BandsRoute = Ember.Route.extend({
    model: function () {
        return $.getJSON('/vote/ajax/bands').then(function (data) {
            return data["bands"];
        });
    }
});

Tunefish.BandRoute = Ember.Route.extend({
    model: function (params) {
        return $.getJSON('/vote/ajax/bands/' + params.band_id);
    }
});

Tunefish.BandController = Ember.ObjectController.extend({
    needs: 'main',
    actions : {
        "vote" : function(vote) {
            var self = this;
            $.post("/vote/ajax/bands/vote", {
                "band_id" : this.get("model.id"),
                "vote": vote
            }).then(function (result) {
                self.set("model.vote_count", result.vote_count);
                self.set("model.vote_average", result.vote_average);
            });
        },
        "addTrack": function(track) {
            this.get('controllers.main').send('addTrack', track);
        }
    }
});

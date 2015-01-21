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
    comment: "",

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

        "addComment": function() {
            var self = this;
            $.post("/vote/ajax/comments/add", {
                "band_id" : this.get("model.id"),
                "comment" : this.get("comment")
            }).then(function (result) {
                self.get("model.comments").pushObject(result);
                self.set("comment", ' ');
            });
        }
    }
});

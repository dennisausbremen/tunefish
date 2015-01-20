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

var bands = [
    {
        'name': 'Foo Fighters olol'
    }
]


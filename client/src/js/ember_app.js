window.Tunefish = Ember.Application.create({
    rootElement: '#app_container'
});

Tunefish.Router.map(function() {
    this.resource('bands', { path: '/' });
});


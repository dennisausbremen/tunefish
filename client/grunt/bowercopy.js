module.exports = {
    dist: {
        options: {
            destPrefix: '<%= dirs.tmp %>/<%= dirs.js %>'
        },
        files: {
            'jquery.min.js': 'jquery/dist/jquery.min.js',
            'vendor/general/01-velocity.min.js': 'velocity/velocity.min.js',
            'vendor/general/02-velocity.ui.min.js': 'velocity/velocity.ui.min.js',
            'vendor/bands/01-slick.min.js': 'slick.js/slick/slick.min.js',
            'vendor/voters/01-handlebars.min.js': 'handlebars/handlebars.min.js',
            'vendor/voters/02-unveil.min.js': 'unveil/jquery.unveil.min.js',
            'vendor/voters/03-ember.min.js': 'ember/ember.min.js',
            'vendor/voters/04-ember.min.js': 'ember-data/ember-data.min.js'
        }
    }
};

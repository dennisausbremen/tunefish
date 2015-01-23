module.exports = {
    dist: {
        options: {
            mangle: true,
            compress: {
                drop_console: true
            },
            report: 'min',
            preserveComments: false
        },
        files: {
            '<%= dirs.tmp %>/<%= dirs.js %>/app.js': ['<%= dirs.src %>/<%= dirs.js %>/app.js'],
            '<%= dirs.tmp %>/<%= dirs.js %>/intro.js': ['<%= dirs.src %>/<%= dirs.js %>/intro.js'],
            '<%= dirs.tmp %>/<%= dirs.js %>/ember_app.js': ['<%= dirs.src %>/<%= dirs.js %>/ember_app.js'],
            '<%= dirs.tmp %>/<%= dirs.js %>/lib/helpers.js': ['<%= dirs.src %>/<%= dirs.js %>/lib/*.js']
        }
    }
};

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
            '<%= dirs.tmp %>/<%= dirs.js %>/app-vote.js': ['<%= dirs.src %>/<%= dirs.js %>/app-vote.js'],
            '<%= dirs.tmp %>/<%= dirs.js %>/lib/helpers.js': ['<%= dirs.src %>/<%= dirs.js %>/lib/helpers.js'],
            '<%= dirs.tmp %>/<%= dirs.js %>/lib/helpers-vote.js': ['<%= dirs.src %>/<%= dirs.js %>/lib/helpers-vote.js']
        }
    }
};

module.exports = {
    options: {
        jshintrc: '.jshintrc'
    },
    dist: [
        '<%= dirs.src %>/<%= dirs.js %>/**/*.js',
        '!<%= dirs.src %>/<%= dirs.js %>/**/*.min.js'
    ]
};

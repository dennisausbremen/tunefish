module.exports = {
    options: {
        jshintrc: '.jshintrc'
    },
    all: [
        '<%= dirs.src %>/<%= dirs.js %>/**/*.js',
        '!<%= dirs.src %>/<%= dirs.js %>/**/*.min.js'
    ]
};

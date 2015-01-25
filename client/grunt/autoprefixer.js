module.exports = {
    options: {
        options: {
            browsers: ['last 2 versions']
        }
    },

    dist: {
        expand: true,
        flatten: true,
        src: '<%= dirs.tmp %>/<%= dirs.css %>/*.css',
        dest: '<%= dirs.tmp %>/<%= dirs.css %>/'
    }
};


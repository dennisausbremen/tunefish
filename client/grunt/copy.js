module.exports = {
    // Copy All
    deploy: {

        files: [
            {
                expand: true,
                cwd: '<%= dirs.tmp %>/',
                src: ['**/*', '!**/*.css'],
                dest: '<%= dirs.dist %>/'
            }
        ]
    },

    //Copy JS
    js: {
        files: [
            {
                expand: true,
                cwd: '<%= dirs.src %>/<%= dirs.js %>/',
                src: ['**'],
                dest: '<%= dirs.dist %>/<%= dirs.js %>'
            }
        ]
    },

    jsTmp: {
        files: [
            {
                expand: true,
                cwd: '<%= dirs.tmp %>/<%= dirs.js %>/',
                src: ['**', '!app.js', '!intro.js', '!lib/helpers.js'],
                dest: '<%= dirs.dist %>/<%= dirs.js %>'
            }
        ]
    },

    //Copy Images
    img: {
        files: [
            {
                expand: true,
                cwd: '<%= dirs.tmp %>/<%= dirs.img %>/',
                src: ['**'],
                dest: '<%= dirs.dist %>/<%= dirs.js %>'
            }
        ]
    },

    //Copy Html
    html: {
        files: [
            {
                expand: true,
                cwd: '<%= dirs.src %>/',
                src: ['*.html'],
                dest: '<%= dirs.dist %>/',
                filter: 'isFile'
            }
        ]
    },

    //Copy CSS
    css: {
        files: [
            {
                expand: true,
                cwd: '<%= dirs.tmp %>/<%= dirs.css %>/',
                src: ['**.min.css'],
                dest: '<%= dirs.dist %>/<%= dirs.css %>',
                filter: 'isFile'
            }
        ]
    }

}

module.exports = {
    options: {
        livereload: true
    },
    sass: {
        files: ['<%= dirs.src %>/<%= dirs.scss %>/{,*/}*.{scss,sass}'],
        tasks: ['sass:dev', 'autoprefixer:dist', 'copy:css']
    },
    js: {
        files: ['<%= dirs.src %>/<%= dirs.js %>/**/*'],
        tasks: ['jshint', 'copy:js', 'copy:jsTmp']
    },
    images: {
        files: ['<%= dirs.src %>/<%= dirs.img %>/**/*'],
        tasks: ['imagemin:dist', 'copy:img']
    },
    html: {
        files: ['<%= dirs.src %>/*.html'],
        tasks: ['copy:html']
    }
};

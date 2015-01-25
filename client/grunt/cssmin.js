module.exports = {
    dist: {
        files: [
            {
                expand: true,
                cwd: '<%= dirs.tmp %>/<%= dirs.css %>/',
                src: ['*.css', '!*.min.css'],
                dest: '<%= dirs.dist %>/<%= dirs.css %>/',
                ext: '.min.css'
            }
        ]
    }
};

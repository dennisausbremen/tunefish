module.exports = {
    dist: {                         // Another target
        files: [
            {
                expand: true,                  // Enable dynamic expansion
                cwd: '<%= dirs.src %>/<%= dirs.img %>',                   // Src matches are relative to this path
                src: '{,*/}**/*.{png,jpg,jpeg,svg}',   // Actual patterns to match
                dest: '<%= dirs.tmp %>/<%= dirs.img %>'                  // Destination path prefix
            }
        ]
    }
};

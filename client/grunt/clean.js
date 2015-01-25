module.exports = {
    prepare: {
        files: [
            {
                src: ['<%= dirs.dist %>/', '<%= dirs.tmp %>/']
            }
        ]
    },
    tmp: {
        files: [
            {
                src: ['<%= dirs.tmp %>/']
            }
        ]
    },
    jsTmp: {
        files: [
            {
                src: ['<%= dirs.tmp %>/<%= dirs.js %>/vendor/']
            }
        ]
    }
};

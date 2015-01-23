module.exports = {
    options: {
        separator: ';',
        stripBanners: true
    },
    dist: {
        files: {
            '<%= dirs.tmp %>/<%= dirs.js %>/plugins.js': ['<%= dirs.tmp %>/<%= dirs.js %>/vendor/general/*.js','<%= dirs.tmp %>/<%= dirs.js %>/vendor/bands/*.js'],
            '<%= dirs.tmp %>/<%= dirs.js %>/plugins-vote.js': ['<%= dirs.tmp %>/<%= dirs.js %>/vendor/general/*.js','<%= dirs.tmp %>/<%= dirs.js %>/vendor/voters/*.js']
        }
    }
};

module.exports = {
    options: {
        includePaths: ['<%= dirs.src %>/<%= dirs.scss %>']
    },
    dist: {
        options: {
            outputStyle: 'expanded',
            sourceComments: 'none'
        },
        files: {
            '<%= dirs.tmp %>/<%= dirs.css %>/app.css': '<%= dirs.src %>/<%= dirs.scss %>/app.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/app-vote.css': '<%= dirs.src %>/<%= dirs.scss %>/app-vote.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/app-vote-admin.css': '<%= dirs.src %>/<%= dirs.scss %>/app-vote-admin.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/intro.css': '<%= dirs.src %>/<%= dirs.scss %>/intro.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/source-sans-pro.css': '<%= dirs.src %>/<%= dirs.scss %>/source-sans-pro.woff.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/bootstrap.css': '<%= dirs.src %>/<%= dirs.scss %>/bootstrap.min.scss'
        }
    },
    dev: {
        options: {
            sourceMap: true,
            sourceComments: 'none',
            outputStyle: 'expanded'
        },
        files: {
            '<%= dirs.tmp %>/<%= dirs.css %>/app.min.css': '<%= dirs.src %>/<%= dirs.scss %>/app.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/app-vote.min.css': '<%= dirs.src %>/<%= dirs.scss %>/app-vote.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/app-vote-admin.min.css': '<%= dirs.src %>/<%= dirs.scss %>/app-vote-admin.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/intro.min.css': '<%= dirs.src %>/<%= dirs.scss %>/intro.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/source-sans-pro.min.css': '<%= dirs.src %>/<%= dirs.scss %>/source-sans-pro.woff.scss',
            '<%= dirs.tmp %>/<%= dirs.css %>/bootstrap.min.css': '<%= dirs.src %>/<%= dirs.scss %>/bootstrap.min.scss'
        }
    }
};

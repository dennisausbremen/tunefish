'use strict';

module.exports = function (grunt) {
    //Get execution time
    require('time-grunt')(grunt);

    // Load up tasks
    require('load-grunt-tasks')(grunt);

    // configurable paths
    var appConfig = {
        src: 'src',
        dist: 'app'
    };

    // Project configuration.
    grunt.initConfig({
        cfg: appConfig,

        // Watch Tasks
        watch: {
            options: {
                livereload: true
            },
            sass: {
                files: ['<%= cfg.src %>/scss/{,*/}*.{scss,sass}'],
                tasks: ['sass:dev', 'autoprefixer:dist', 'cssmin:dist']
            },
            js: {
                files: ['<%= cfg.src %>/js/**/*'],
                tasks: ['jshint','copy:js']
            },
            images: {
                files: ['<%= cfg.src %>/img/**/*'],
                tasks: ['imagemin:dist']
            },
            views: {
                files: ['<%= cfg.src %>/views/**/*.html'],
                tasks: ['copy:views']
            },
            html: {
                files: ['<%= cfg.src %>/index.html'],
                tasks: ['copy:html']
            }
        },

        // Clean CSS & Generated JS
        clean: {
            dist: {
                files: [{
                    dot: true,
                    src: ['<%= cfg.dist %>/**/*', '<%= cfg.src %>/css/**/*']
                }]
            }
        },

        //Optimize Images
        imagemin: {
            dist: {                         // Another target
                files: [{
                    expand: true,                  // Enable dynamic expansion
                    cwd: '<%= cfg.src %>/img',                   // Src matches are relative to this path
                    src: ['**/*.{png,jpg,gif,svg}'],   // Actual patterns to match
                    dest: '<%= cfg.dist %>/img'                  // Destination path prefix
                }]
            }
        },

        //Compile SASS
        sass: {
            options:{
                includePaths : ['<%= cfg.src %>/scss']
            },
            dist: {
                options: {
                    outputStyle: 'nested',
                    sourceComments: 'none'
                },
                files: {
                    '<%= cfg.dist %>/css/app.css': '<%= cfg.src %>/scss/app.scss'
                }
            },
            dev: {
                options: {
                    sourceMap: true,
                    sourceComments: 'none',
                    outputStyle: 'nested'
                },
                files: {
                    '<%= cfg.dist %>/css/app.css': '<%= cfg.src %>/scss/app.scss',
                    '<%= cfg.dist %>/css/source-sans-pro.woff.css': '<%= cfg.src %>/scss/source-sans-pro.woff.scss'
                }
            }
        },

        cssmin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= cfg.dist %>/css/',
                    src: ['*.css', '!*.min.css'],
                    dest: '<%= cfg.dist %>/css/',
                    ext: '.min.css'
                }]
            }
        },

        autoprefixer: {

            options: {
                options: {
                    browsers: ['last 2 versions']
                }
            },

            // prefix the specified file
            dist: {
                options: {
                    // Target-specific options go here.
                },
                src: '<%= cfg.dist %>/css/app.css',
                dest: '<%= cfg.dist %>/css/app.css'
            }
        },


        bowercopy: {
            dev: {
                options: {
                    destPrefix: '<%= cfg.src %>/js/vendor/'
                },
                files: {
                    'jquery.min.js': 'jquery/dist/jquery.min.js'
                }
            },
            dist: {
                options: {
                    // Bower components folder will be removed afterwards
                    clean: true,
                    destPrefix: '<%= cfg.src %>/js/vendor/'
                },
                files: {
                    'jquery.min.js': 'jquery/dist/jquery.min.js'
                }
            }
        },

        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            all: [
                '<%= cfg.src %>/js/*.js'
            ]
        },

        copy: {
            // Copy All
            all: {

               files: [
                   //Copy Views
                   {
                       expand: true,
                       cwd: '<%= cfg.src %>/views/',
                       filter: 'isFile',
                       src: ['**'],
                       dest: '<%= cfg.dist %>/views/'
                   },
                   //Copy Html
                   {
                       expand: true,
                       cwd: '<%= cfg.src %>/',
                       src: ['*.html'],
                       dest: '<%= cfg.dist %>/',
                       filter: 'isFile'
                   },
                   //Copy Views
                   {
                        expand: true,
                        cwd: '<%= cfg.src %>/views/',
                        filter: 'isFile',
                        src: ['**'],
                        dest: 'views/'
                   },
                   {
                       expand: true,
                       cwd: '<%= cfg.src %>/js/',
                       src: ['**'],
                       dest: '<%= cfg.dist %>/js'
                   }
               ]
            },

            //Copy Views
            views: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= cfg.src %>/views/',
                        filter: 'isFile',
                        src: ['**'],
                        dest: 'views/'
                    }
                ]
            },

            //Copy JS
            js: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= cfg.src %>/js/',
                        src: ['**'],
                        dest: '<%= cfg.dist %>/js'
                    }
                ]
            },

            //Copy Html
            html: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= cfg.src %>/',
                        src: ['*.html'],
                        dest: '<%= cfg.dist %>/',
                        filter: 'isFile'
                    }
                ]
            },

            //Copy CSS
            css: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= cfg.src %>/css/',
                        src: ['*'],
                        dest: '<%= cfg.dist %>/css',
                        filter: 'isFile'
                    }
                ]
            }

        },

        useminPrepare: {
            html: '<%= cfg.src %>/index.html'
        }




    });

    // TODO
    //grunt.registerTask('build', [
    //    'clean:dist',
    //    'imagemin:dist',
    //    'sass:dist',
    //    'autoprefixer:dist',
    //    'bowercopy:dist',
    //    'jshint',
    //    'useminPrepare',
    //    'concat:generated',
    //    'cssmin:generated',
    //    'uglify:generated',
    //    'filerev',
    //    'usemin',
    //    'copy:all'
    //]);

    grunt.registerTask('dev', [
        'clean:dist',
        'imagemin:dist',
        'sass:dev',
        'autoprefixer:dist',
        'cssmin:dist',
        'bowercopy:dev',
        'jshint',
        'copy:all',
        'watch'
    ]);

    grunt.registerTask('default', ['dev']);
};

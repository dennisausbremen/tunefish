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
                tasks: ['jshint', 'copy:js']
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
                files: ['<%= cfg.src %>/*.html'],
                tasks: ['copy:html']
            }
        },

        // Clean CSS & Generated JS
        clean: {
            dist: {
                files: [
                    {
                        dot: true,
                        src: ['<%= cfg.dist %>/**/*', '<%= cfg.src %>/css/**/*','<%= cfg.src %>/js/vendor/**/*']
                    }
                ]
            }
        },

        //Optimize Images
        imagemin: {
            dist: {                         // Another target
                files: [
                    {
                        expand: true,                  // Enable dynamic expansion
                        cwd: '<%= cfg.src %>/img',                   // Src matches are relative to this path
                        src: '{,*/}**/*.{png,jpg,jpeg,svg}',   // Actual patterns to match
                        dest: '<%= cfg.dist %>/img'                  // Destination path prefix
                    }
                ]
            }
        },

        //Compile SASS
        sass: {
            options: {
                includePaths: ['<%= cfg.src %>/scss']
            },
            dist: {
                options: {
                    outputStyle: 'expanded',
                    sourceComments: 'none'
                },
                files: {
                    '<%= cfg.src %>/css/app.css': '<%= cfg.src %>/scss/app.scss',
                    '<%= cfg.src %>/css/intro.css': '<%= cfg.src %>/scss/intro.scss',
                    '<%= cfg.src %>/css/source-sans-pro.woff.css': '<%= cfg.src %>/scss/source-sans-pro.woff.scss'
                }
            },
            dev: {
                options: {
                    sourceMap: true,
                    sourceComments: 'none',
                    outputStyle: 'expanded'
                },
                files: {
                    '<%= cfg.src %>/css/app.css': '<%= cfg.src %>/scss/app.scss',
                    '<%= cfg.src %>/css/intro.css': '<%= cfg.src %>/scss/intro.scss',
                    '<%= cfg.src %>/css/source-sans-pro.woff.css': '<%= cfg.src %>/scss/source-sans-pro.woff.scss'
                }
            }
        },

        autoprefixer: {

            options: {
                options: {
                    browsers: ['last 2 versions']
                }
            },

            dist: {
                expand: true,
                flatten: true,
                src: '<%= cfg.src %>/css/*.css',
                dest: '<%= cfg.src %>/css/'
            }
        },

        cssmin: {
            dist: {
                files: [
                    {
                        expand: true,
                        cwd: '<%= cfg.src %>/css/',
                        src: ['*.css', '!*.min.css'],
                        dest: '<%= cfg.dist %>/css/',
                        ext: '.min.css'
                    }
                ]
            }
        },


        bowercopy: {
            dev: {
                options: {
                    destPrefix: '<%= cfg.src %>/js'
                },
                files: {
                    'jquery.min.js': 'jquery/dist/jquery.js',
                    'vendor/01-slick.min.js': 'slick.js/slick/slick.js',
                    'vendor/02-velocity.min.js': 'velocity/velocity.js',
                    'vendor/03-velocity.ui.min.js': 'velocity/velocity.ui.js',
                    'vendor/05-handlebars.min.js': 'handlebars/handlebars.js',
                    'vendor/06-ember.min.js': 'ember/ember.js'
                }
            },
            dist: {
                options: {
                    // Bower components folder will be removed afterwards
                    clean: true,
                    destPrefix: '<%= cfg.src %>/js'
                },
                files: {
                    'jquery.min.js': 'jquery/dist/jquery.min.js',
                    'vendor/01-slick.min.js': 'slick.js/slick/slick.min.js',
                    'vendor/02-velocity.min.js': 'velocity/velocity.min.js',
                    'vendor/03-velocity.ui.min.js': 'velocity/velocity.ui.min.js',
                    'vendor/05-handlebars.min.js': 'handlebars/handlebars.min.js',
                    'vendor/06-ember.min.js': 'ember/ember.min.js'
                }
            }
        },

        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            all: [
                '!<%= cfg.src %>/js/vendor/*.js',
                '<%= cfg.src %>/js/lib/*.js',
                '<%= cfg.src %>/js/app.js',
                '<%= cfg.src %>/js/intro.js'
            ]
        },

        uglify: {
            dev: {
                options: {
                    mangle: false
                },
                files: {
                    '<%= cfg.dist %>/js/app.js': ['<%= cfg.src %>/js/app.js'],
                    '<%= cfg.dist %>/js/intro.js': ['<%= cfg.src %>/js/intro.js'],
                    '<%= cfg.dist %>/js/lib/helpers.js': ['<%= cfg.src %>/js/lib/*.js'],
                    '<%= cfg.dist %>/js/plugins.js': ['<%= cfg.src %>/js/vendor/*.js']
                }
            },
            dist: {
                options: {
                    mangle: true,
                    compress: {
                        drop_console: true
                    },
                    report: 'min',
                    preserveComments: false
                },
                files: {
                    '<%= cfg.dist %>/js/app.js': ['<%= cfg.src %>/js/app.js'],
                    '<%= cfg.dist %>/js/intro.js': ['<%= cfg.src %>/js/intro.js'],
                    '<%= cfg.dist %>/js/lib/helpers.js': ['<%= cfg.src %>/js/lib/*.js'],
                    '<%= cfg.dist %>/js/plugins.js': ['<%= cfg.src %>/js/vendor/*.js']
                }
            }
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
                    //Copy JS
                    {
                        expand: true,
                        cwd: '<%= cfg.src %>/js/',
                        src: ['jquery.min.js', 'ember_app.js'],
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

        }


    });

    grunt.registerTask('build', [
        'clean:dist',
        'imagemin:dist',
        'sass:dist',
        'autoprefixer:dist',
        'cssmin:dist',
        'bowercopy:dev',
        'jshint',
        'uglify:dist',
        'copy:all'
    ]);

    grunt.registerTask('dev', [
        'clean:dist',
        'imagemin:dist',
        'sass:dev',
        'autoprefixer:dist',
        'cssmin:dist',
        'bowercopy:dev',
        'jshint',
        'uglify:dev',
        'copy:all',
        'watch'
    ]);



    grunt.registerTask('dev_noimagemin', [
        'clean:dist',
        'sass:dev',
        'autoprefixer:dist',
        'cssmin:dist',
        'bowercopy:dev',
        'jshint',
        'uglify:dev',
        'copy:all',
        'watch'
    ]);

    grunt.registerTask('default', ['dev']);
};

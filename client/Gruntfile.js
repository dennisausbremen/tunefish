'use strict';

// module exports
module.exports = function(grunt) {

    // measures the time each task takes
    require('time-grunt')(grunt);

    require('load-grunt-config')(grunt, {
        jitGrunt: true,
        data: {
            dirs : {
                src : "<%= package.dirs.src%>",
                dist: "<%= package.dirs.dist%>",
                tmp : "<%= package.dirs.tmp%>",
                css : "<%= package.dirs.css%>",
                scss : "<%= package.dirs.scss%>",
                js : "<%= package.dirs.js%>",
                img : "<%= package.dirs.img%>",
                views : "<%= package.dirs.views%>"
            }
        }
    });

};

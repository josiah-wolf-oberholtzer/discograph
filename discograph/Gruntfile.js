module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        less: {
            build: {
                options: {
                    //compress: true,
                    //yuicompress: true,
                    //optimization: 2
                },
                files: {
                    'static/css/discograph.css': 'source/css/discograph.less'
                },
            },
        },
        smash: {
            bundle: {
                src: 'source/js/index.js',
                dest: 'static/js/discograph.js',
            },
        },
        watch: {
            js: {
                files: ['source/js/**'],
                tasks: ['smash'],
                },
            css: {
                files: ['source/css/**'],
                tasks: ['less'],
                }
        }
    });
    grunt.loadNpmTasks('grunt-smash');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask('default', ['smash', 'less', 'watch']);
};
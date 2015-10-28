module.exports = function(grunt) {
    grunt.initConfig({
        copy: {
            build: {
                cwd: 'source',
                src: ['**'],
                dest: 'static',
                expand: true
            },
        },
    });
    grunt.loadNpmTasks('grunt-contrib-copy');
};
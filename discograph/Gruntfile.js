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
        jsbeautifier: {
            files: ['static/js/discograph.js'],
            options: {
                braceStyle: 'collapse',
                breakChainedMethods: true,
                e4x: false,
                evalCode: false,
                indentChar: ' ',
                indentLevel: 4,
                indentSize: 2,
                indentWithTabs: false,
                jslintHappy: true,
                keepArrayIndentation: false,
                keepFunctionIndentation: false,
                maxPreserveNewlines: 0,
                preserveNewLines: false,
                spaceBeforeConditional: true,
                spaceInParen: true,
                unescapeStrings: false,
                wrapLineLength: 79,
                endWithNewline: true
            }
        },
        watch: {
            js: {
                files: ['source/js/**'],
                tasks: ['smash', 'jsbeautifier'],
                },
            css: {
                files: ['source/css/**'],
                tasks: ['less'],
                }
        }
    });
    grunt.loadNpmTasks("grunt-jsbeautifier");
    grunt.loadNpmTasks('grunt-smash');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask('default', ['smash', 'jsbeautifier', 'less', 'watch']);
};
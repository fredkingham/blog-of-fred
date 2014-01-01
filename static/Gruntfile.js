module.exports = function(grunt) {

  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

   compass: {
      dev: {
        options: {
          config: 'config.rb',
          force: true,
        }
      },
      forcecompile: true
    },

  concat: {
    options: {
      stripBanners: true,
      banner: '/*! <%= pkg.name %> - v<%= pkg.version %> - ' +
        '<%= grunt.template.today("yyyy-mm-dd") %> */',
    },
    css: {
      src: ['build/**/*.css'],
      dest: 'dist/stylesheets/main.css',
    }

  },

  watch: {
      sass: {
        files: ['build/stylesheets/**/*.scss'],
        tasks: ['compass:dev', 'concat']
      },
      options: {
         livereload: true
      }
    },

 

  });

  // Default task(s).
  grunt.registerTask('default', 'watch');
  grunt.registerTask('build', ['compass:dev', 'concat']);
  grunt.registerTask('clean', ['uncss']);
};
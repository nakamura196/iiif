var gulp = require('gulp');
var clean = require('gulp-clean');
var linter = require('gulp-jshint');
var minifyCSS = require('gulp-clean-css');
var minifyJS = require('gulp-minify');
var rename = require('gulp-rename');

gulp.task('clean', function(){
  return gulp.src(
    ['*.min.css', '*.min.js'], {read: false}
  ).pipe(clean());
});

gulp.task('lint', function(){
  return gulp.src(['*.js', '!*.min.js', '!gulpfile.js']).pipe(
    linter()
  ).pipe(
    linter.reporter('default')
  );
});

gulp.task('minify-css', ['clean'], function(){
  return gulp.src('*.css').pipe(
    minifyCSS()
  ).pipe(
    rename({ suffix: '.min' })
  ).pipe(
    gulp.dest('.')
  );
});

gulp.task('minify-js', ['clean'], function(){
  return gulp.src(['*.js', '!gulpfile.js']).pipe(
    minifyJS({
      ext:{
        min:'.min.js'
      },
      noSource: true
    })
  ).pipe(
    gulp.dest('.')
  );
});

gulp.task('minify', ['clean', 'minify-css', 'minify-js']);

var gulp = require('gulp');
var concat = require('gulp-concat');
var browserSync = require('browser-sync').create();
var clean = require('gulp-clean');
var cssmin = require('gulp-cssmin');
var flatten = require('gulp-flatten');
var rename = require('gulp-rename');
var htmlmin = require('gulp-htmlmin');


// remove files in the public folder
gulp.task('clean', function(){
	return gulp.src('./public/*', {read: false})
		.pipe(clean());
});

gulp.task('serve', function(){
	browserSync.init({
		server: {
			baseDir: './public'
		}
	});

	gulp.watch('index.html', gulp.series(['pages']));
	gulp.watch('app.css', gulp.series(['styles']));
	gulp.watch('app.js', gulp.series(['scripts']));

  gulp.watch(['app.css', 'app.js', 'index.html']).on('change', browserSync.reload);
});


gulp.task('pages', function(){
	return gulp.src('index.html')
		.pipe(htmlmin({
			collapseWhitespace: true
		}))
		.pipe(gulp.dest('./public'), { base: '.' });

});

// compiles styles with foundation base styles
gulp.task('styles', function(){
	return gulp.src('app.css')
	.pipe(cssmin())
	.pipe(gulp.dest('./public'), { base: '.'});
});


gulp.task('scripts', function(){
	return gulp.src('app.js')
		.pipe(gulp.dest('./public'));
});


gulp.task('default', gulp.series(['pages', 'styles','scripts', 'serve']));

gulp.task('build', gulp.series(['pages', 'styles', 'scripts']));

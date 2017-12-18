System.config({
  defaultJSExtensions: true,
  map: {
    'usatu/app': 'usatu/app3',

    '@angular/core': 'node_modules/@angular/core/bundles/core.umd.min.js',
    '@angular/common': 'node_modules/@angular/common/bundles/common.umd.min.js',
    '@angular/compiler': 'node_modules/@angular/compiler/bundles/compiler.umd.min.js',
    '@angular/forms': 'node_modules/@angular/forms/bundles/forms.umd.min.js',
    '@angular/http': 'node_modules/@angular/http/bundles/http.umd.min.js',
    '@angular/platform-browser': 'node_modules/@angular/platform-browser/bundles/platform-browser.umd.min.js',
    '@angular/platform-browser-dynamic': 'node_modules/@angular/platform-browser-dynamic/bundles/platform-browser-dynamic.umd.min.js',
    '@angular/material': 'node_modules/@angular/material/bundles/material.umd.min.js',
    '@angular/platform-browser/animations': 'node_modules/@angular/platform-browser/bundles/platform-browser-animations.umd.min.js',
    '@angular/animations': 'node_modules/@angular/animations/bundles/animations.umd.min.js',
    '@angular/animations/browser': 'node_modules/@angular/animations/bundles/animations-browser.umd.min.js',
    '@angular': 'node_modules/@angular',
    'angular2-recaptcha': 'node_modules/angular2-recaptcha',
    'jquery': 'node_modules/jquery/dist',
    'jquery.cookie': 'node_modules/jquery.cookie',
    'rxjs': 'node_modules/rxjs'
  },
  paths: {
    //'node_modules/@angular/*': 'node_modules/@angular/*/bundles'
  },
  meta: {
    '@angular/*': {'format': 'cjs'}
  },
  packages: {
    'rxjs': {main: 'Rx'},
    'jquery': {main: 'jquery.min.js'},
    'jquery.cookie': {main: 'jquery.cookie.js'},
    'angular2-recaptcha': {main: 'index.js'},
  }
});

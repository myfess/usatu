System.config({
  defaultJSExtensions: true,
  map: {
    'static/app/app': 'static/app/app_es5',

    '@angular/core': 'https://cdn.jsdelivr.net/npm/@angular/core@4.2.0/bundles/core.umd.min.js',
    '@angular/common': 'https://cdn.jsdelivr.net/npm/@angular/common@4.2.0/bundles/common.umd.min.js',
    '@angular/compiler': 'https://cdn.jsdelivr.net/npm/@angular/compiler@4.2.0/bundles/compiler.umd.min.js',
    '@angular/forms': 'https://cdn.jsdelivr.net/npm/@angular/forms@4.2.0/bundles/forms.umd.min.js',
    '@angular/http': 'https://cdn.jsdelivr.net/npm/@angular/http@4.2.0/bundles/http.umd.min.js',
    '@angular/platform-browser': 'https://cdn.jsdelivr.net/npm/@angular/platform-browser@4.2.0/bundles/platform-browser.umd.min.js',
    '@angular/platform-browser-dynamic': 'https://cdn.jsdelivr.net/npm/@angular/platform-browser-dynamic@4.2.0/bundles/platform-browser-dynamic.umd.min.js',
    '@angular/material': 'https://cdn.jsdelivr.net/npm/@angular/material@2.0.0-beta.7/bundles/material.umd.min.js',
    '@angular/platform-browser/animations': 'https://cdn.jsdelivr.net/npm/@angular/platform-browser@4.2.0/bundles/platform-browser-animations.umd.min.js',
    '@angular/animations': 'https://cdn.jsdelivr.net/npm/@angular/animations@4.2.0/bundles/animations.umd.min.js',
    '@angular/animations/browser': 'https://cdn.jsdelivr.net/npm/@angular/animations@4.2.0/bundles/animations-browser.umd.min.js',
    'angular2-recaptcha': 'https://cdn.jsdelivr.net/npm/angular2-recaptcha@0.6.0',
    'jquery': 'https://cdn.jsdelivr.net/npm/jquery@2.2.2/dist',
    'jquery.cookie': 'https://cdn.jsdelivr.net/npm/jquery.cookie@1.4.1',
    'rxjs': 'https://cdn.jsdelivr.net/npm/rxjs@5.0.1'

    // ,'@angular': 'node_modules/@angular'
  },
  paths: {
  },
  meta: {
    '@angular/*': {'format': 'cjs'}
  },
  packages: {
    'rxjs': {main: 'Rx'},
    'jquery': {main: 'jquery.min.js'},
    'jquery.cookie': {main: 'jquery.cookie.js'},
    'angular2-recaptcha': {main: 'index.js'}
  }
});

// Чтобы заработали короткие названия модулей: "moduleId: module.id"
// Используется маги описанная вот здесь: https://github.com/systemjs/systemjs/issues/1266
// transpiler: 'ts',
// meta: { 'typescript': { 'exports': 'ts' } }
// 'ts': 'node_modules/plugin-typescript/lib/plugin.js',
// 'typescript': 'node_modules/typescript/lib/typescript.js'


System.config({

  transpiler: 'ts',
  typescriptOptions: {
    emitDecoratorMetadata: true,
    experimentalDecorators: true,
    module: 'commonjs'
  },

  meta: {
    'typescript': {
      'exports': 'ts'
    },

    '@angular/*': {'format': 'cjs'}
  },

  map: {
	// '@angular/core': 'node_modules/@angular/core/bundles/core.umd.min.js',
	'@angular/core': 'https://cdn.jsdelivr.net/npm/@angular/core@4.2.0/bundles/core.umd.min.js',
	// '@angular/compiler': 'node_modules/@angular/compiler/bundles/compiler.umd.min.js',
	'@angular/compiler': 'https://cdn.jsdelivr.net/npm/@angular/compiler@4.2.0/bundles/compiler.umd.min.js',
	// '@angular/forms': 'node_modules/@angular/forms/bundles/forms.umd.min.js',
	'@angular/forms': 'https://cdn.jsdelivr.net/npm/@angular/forms@4.2.0/bundles/forms.umd.min.js',
	// '@angular/http': 'node_modules/@angular/http/bundles/http.umd.min.js',
	'@angular/http': 'https://cdn.jsdelivr.net/npm/@angular/http@4.2.0/bundles/http.umd.min.js',
	// '@angular/platform-browser': 'node_modules/@angular/platform-browser/bundles/platform-browser.umd.min.js',
	'@angular/platform-browser': 'https://cdn.jsdelivr.net/npm/@angular/platform-browser@4.2.0/bundles/platform-browser.umd.min.js',
    // '@angular/platform-browser-dynamic': 'node_modules/@angular/platform-browser-dynamic/bundles/platform-browser-dynamic.umd.min.js',
	'@angular/platform-browser-dynamic': 'https://cdn.jsdelivr.net/npm/@angular/platform-browser-dynamic@4.2.0/bundles/platform-browser-dynamic.umd.min.js',
	// '@angular/platform-browser/animations': 'node_modules/@angular/platform-browser/bundles/platform-browser-animations.umd.min.js',
	'@angular/platform-browser/animations': 'https://cdn.jsdelivr.net/npm/@angular/platform-browser@4.2.0/bundles/platform-browser-animations.umd.min.js',
	// '@angular/common': 'node_modules/@angular/common/bundles/common.umd.min.js',
	'@angular/common': 'https://cdn.jsdelivr.net/npm/@angular/common@4.2.0/bundles/common.umd.min.js',
	// 'jquery': 'node_modules/jquery/dist',
	'jquery': 'https://cdn.jsdelivr.net/npm/jquery@2.2.2/dist',
	// 'jquery.cookie': 'node_modules/jquery.cookie',
	'jquery.cookie': 'https://cdn.jsdelivr.net/npm/jquery.cookie@1.4.1',
	// 'rxjs': 'node_modules/rxjs',
	'rxjs': 'https://cdn.jsdelivr.net/npm/rxjs@5.0.1',
	// 'ts': 'node_modules/plugin-typescript/lib/plugin.js',
	'ts': 'https://cdn.jsdelivr.net/npm/plugin-typescript@7.1.1/lib/plugin.js',
	// 'typescript': 'node_modules/typescript/lib/typescript.js'
	'typescript': 'https://cdn.jsdelivr.net/npm/typescript@2.3.2/lib/typescript.js',
    // 'angular2-recaptcha': 'node_modules/angular2-recaptcha'
    'angular2-recaptcha': 'https://cdn.jsdelivr.net/npm/angular2-recaptcha@0.6.0',
    // '@angular/material': 'node_modules/@angular/material/bundles/material.umd.min.js',
    '@angular/material': 'https://cdn.jsdelivr.net/npm/@angular/material@2.0.0-beta.7/bundles/material.umd.min.js',
    // '@angular/animations': 'node_modules/@angular/animations/bundles/animations.umd.min.js',
    '@angular/animations': 'https://cdn.jsdelivr.net/npm/@angular/animations@4.2.0/bundles/animations.umd.min.js',
    // '@angular/animations/browser': 'node_modules/@angular/animations/bundles/animations-browser.umd.min.js',
    '@angular/animations/browser': 'https://cdn.jsdelivr.net/npm/@angular/animations@4.2.0/bundles/animations-browser.umd.min.js',

    '@angular': 'node_modules/@angular'
  },

  paths: {
  },

  packages: {
	'static': { main: 'main', defaultExtension: 'ts' },
    'rxjs': {main: 'Rx'},
    'jquery': {main: 'jquery.js'},
    'angular2-recaptcha': {main: 'index.js'},
    'jquery.cookie': {main: 'jquery.cookie.js'}
  }
});


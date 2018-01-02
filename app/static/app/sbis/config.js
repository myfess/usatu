(function () {
   var
      global = (function(){ return this || (0,eval)('this'); }()),
      wsPath = ((global.wsConfig ? global.wsConfig.wsRoot : undefined) ||  '/ws/').replace(/^\//, ''),
      mysbis = global.wsConfig.mysbis,
      usatusbis = global.wsConfig.usatusbis,
      resourcesPath = ((global.wsConfig ? global.wsConfig.resourceRoot : undefined) || '/resources/').replace(/^\//, ''),
      isNode = typeof process !== 'undefined',
      bundles = global.bundles,
      options, pathjoin;

   if (isNode) {
      pathjoin = require('path').join;
   } else {
      function removeLeadingSlash(path) {
         if (path) {
            var head = path.charAt(0);
            if (head == '/' || head == '\\') {
               path = path.substr(1);
            }
         }
         return path;
      }

      function removeTrailingSlash(path) {
         if (path) {
            var tail = path.substr(path.length - 1);
            if (tail == '/' || tail == '\\') {
               path = path.substr(0, path.length - 1);
            }
         }
         return path;
      }

      pathjoin = function(path1, path2) {
         return removeTrailingSlash(path1) + '/' + removeLeadingSlash(path2);
      };
   }

   function createRequirejsConfig(baseUrl, wsPath, resourcesPath, options) {
      var cfg = {
         baseUrl: baseUrl,
         paths: {
            'Lib': pathjoin(wsPath, 'lib'),
            'Ext': pathjoin(wsPath, 'lib/Ext'),
            'Core': pathjoin(wsPath, 'core'),
            'unit': '/~ws/test/unit',
            'Demo': "/~ws/Demo",
            'Deprecated': pathjoin(wsPath, 'deprecated'),
            'Helpers': pathjoin(wsPath, 'core/helpers'),
            'Transport': pathjoin(wsPath, 'transport'),
            'Resources': resourcesPath,
            'native-css': pathjoin(wsPath, 'ext/requirejs/plugins/native-css'),
            // Грузим css через собственный плагин
            'css': pathjoin(mysbis, 'css'),
            'js': pathjoin(wsPath, 'ext/requirejs/plugins/js'),
            'normalize': pathjoin(wsPath, 'ext/requirejs/plugins/normalize'),
            'html': pathjoin(wsPath, 'ext/requirejs/plugins/html'),
            'tmpl': pathjoin(wsPath, 'ext/requirejs/plugins/tmpl'),
            'text': pathjoin(wsPath, 'ext/requirejs/plugins/text'),
            'is': pathjoin(wsPath, 'ext/requirejs/plugins/is'),
            'is-api': pathjoin(wsPath, 'ext/requirejs/plugins/is-api'),
            'i18n': pathjoin(wsPath, 'ext/requirejs/plugins/i18n'),
            'json': pathjoin(wsPath, 'ext/requirejs/plugins/json'),
            'order': pathjoin(wsPath, 'ext/requirejs/plugins/order'),
            'template': pathjoin(wsPath, 'ext/requirejs/plugins/template'),
            'cdn': pathjoin(wsPath, 'ext/requirejs/plugins/cdn'),
            'datasource': pathjoin(wsPath, 'ext/requirejs/plugins/datasource'),
            'xml': pathjoin(wsPath, 'ext/requirejs/plugins/xml'),
            'preload': pathjoin(wsPath, 'ext/requirejs/plugins/preload'),
            'browser': pathjoin(wsPath, 'ext/requirejs/plugins/browser'),
            'optional': pathjoin(wsPath, 'ext/requirejs/plugins/optional'),
            'remote': pathjoin(wsPath, 'ext/requirejs/plugins/remote'),
            'bootup' : pathjoin(wsPath, 'res/js/bootup'),
            'bootup-min' : pathjoin(wsPath, 'res/js/bootup-min'),
            'old-bootup' : pathjoin(wsPath, 'res/js/old-bootup')
         },

         /**
          * Дикая наркомания из-за того что я гружу ws с чужого CDN
          * https://stackoverflow.com/questions/38351956/requirejs-text-plugin-cannot-load-html-from-other-domain
          */
         config: {
             'text': {
                 useXhr: function (url, protocol, hostname, port) {
                     return true;
                 }
             }
         },

         /*
          * А это чтобы css грузить с своего сайта
          */
         usatu: {
           'mysbis': mysbis,
           'usatusbis': usatusbis,
           'wsRoot': wsPath
         },

         testing: typeof jstestdriver !== 'undefined',
         waitSeconds: 60
      };

      if (typeof window !== 'undefined' && window.buildnumber) {
         cfg.cacheSuffix = '.v' + window.buildnumber;
      }

      if (options) {
         for (var prop in options) {
            if (options.hasOwnProperty(prop)) {
               if (prop == 'requirejsPaths') {
                  for (var p in options[prop]) {
                     if (!options[prop].hasOwnProperty(p)) continue;
                     cfg.paths[p] = pathjoin(baseUrl, options[prop][p]);
                  }
               } else {
               cfg[prop] = options[prop];
            }
         }
      }
      }

      return cfg;
   }

   // На ноде мы только возвращаем конфигурацию, не инициализируем дефолтный requirejs
   if (isNode) {
      module.exports = createRequirejsConfig;
   } else {
      if (bundles && resourcesPath.indexOf('debug/') === -1) {
         for (bundle in bundles) {
            if (bundle.indexOf(resourcesPath) === 0) {
               continue;
            }
            bundles[resourcesPath + bundle.replace('resources/', '')] = bundles[bundle];
            delete bundles[bundle];
         }
         options = {
            bundles: bundles || {}
         };
      }
      global.requirejs.config(createRequirejsConfig('/', wsPath, resourcesPath, options));
   }
}());

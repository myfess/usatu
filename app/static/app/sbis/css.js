(function() {

    "use strict";

    var global = (function() {
            return this || (0, eval)('this');
        }()),
        define = global.define || (global.requirejs && global.requirejs.define) || (requirejsVars && requirejsVars.define);
   function getCookie(name) {
      var matches = document.cookie.match(new RegExp(
         "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
      ));
      return matches ? decodeURIComponent(matches[1]) : undefined;
   }
    function itIsControl(path) {
        return ~path.indexOf('SBIS3.CONTROLS/components');
    };
    /**
     @author Кочнев Н.С.
     @workaround Временное решение. Нужно, для того чтобы никто кроме онлайна не смог загрузить css'ки контролов
     TODO: Выпилить, когда научимся компилить контролы под разные темы и определять пренадлежность теме конкретного сервиса
     */
    function resolveSuffix(path) {
        var config = window.wsConfig;
        var themeNameFromCookies = getCookie('thmname');
        var themeNames;

        if (!config) {
            return '';
        }
        if (itIsControl(path)) {

            if (config.themeName) {
                    return '__' + config.themeName;
            } else {
                if (themeNameFromCookies) {
                    return '__' + themeNameFromCookies;
                } else {
                    return '';
                }
            }
        }
        else {
            return '';
        }
    };

    define('css', ['native-css', 'Core/pathResolver', 'Core/detection'], function(cssAPI, pathResolver, detection) {
        return {
            load: function(name, require, load, conf) {
                if (conf.testing || require.isBrowser === false) {
                    load(true);
                } else {

                    var path = pathResolver(name, 'css');
                    var suffix = resolveSuffix(path);

                    if (suffix) {
                       load(null);
                       return;
                    }

                    if (path.substr(path.length - 4, 4) == '.css') {
                        path = path.substr(0, path.length - 4);
                    }
                    path = path + suffix;
                    // Заменяем путь чтобы грузить css с основного сайта
                    path = path.replace(conf.usatu.wsRoot, conf.usatu.usatusbis);
                    cssAPI.load(path, require, load, conf);
                }
            }
        };
    });

})();

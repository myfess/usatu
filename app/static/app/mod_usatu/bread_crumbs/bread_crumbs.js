define('js!mod_usatu/bread_crumbs/bread_crumbs',
  [
  'js!SBIS3.CORE.CompoundControl',
  'tmpl!mod_usatu/bread_crumbs/bread_crumbs'
  ],

  function(CompoundControl, dotTplFn) {
    var moduleClass = CompoundControl.extend({
      _dotTplFn: dotTplFn,
      $protected: {
        _options: {
          crumbs: global_bread_crumbs
        }
      },
   });

   return moduleClass;
});

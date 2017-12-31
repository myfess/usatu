define('js!mod_usatu/add_theme_btn/add_theme_btn',
[
'js!SBIS3.CORE.CompoundControl',
'tmpl!mod_usatu/add_theme_btn/add_theme_btn',
'js!SBIS3.CORE.Button'
],

function(CompoundControl, dotTplFn) {
  var moduleClass = CompoundControl.extend({
    _dotTplFn: dotTplFn,

    init: function() {
      moduleClass.superclass.init.call(this);
      var btn = this.getChildControlByName('b_new_theme');
      btn.subscribe('onActivated', function() {
        document.location.href = 'board_theme';
      });
    }
 });

 return moduleClass;
});

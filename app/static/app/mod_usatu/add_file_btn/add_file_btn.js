define('js!mod_usatu/add_file_btn/add_file_btn',
  [
  'js!SBIS3.CORE.CompoundControl',
  'tmpl!mod_usatu/add_file_btn/add_file_btn',
  'js!SBIS3.CORE.Button'
  ],

  function(CompoundControl, dotTplFn) {
    var moduleClass = CompoundControl.extend({
      _dotTplFn: dotTplFn,

      init: function() {
        moduleClass.superclass.init.call(this);
        var btn = this.getChildControlByName('b_upload');
        btn.subscribe('onActivated', function() {
          document.location.href = 'files_for_edu/add_file';
        });
      }
   });

   return moduleClass;
});

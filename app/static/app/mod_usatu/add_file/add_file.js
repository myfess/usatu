define('js!mod_usatu/add_file/add_file',
  [
  'js!SBIS3.CORE.CompoundControl',
  'tmpl!mod_usatu/add_file/add_file',
  'js!WS.Data/Source/SbisService',
  'Core/ContextBinder',
  'css!mod_usatu/add_file/add_file',
  'js!SBIS3.CORE.Button',
  'js!SBIS3.CORE.FieldText',
  'js!mod_usatu/my_drop_down/my_drop_down'
  ],

  function(CompoundControl, dotTplFn, SbisService, ContextBinder) {
    var moduleClass = CompoundControl.extend({
      _dotTplFn: dotTplFn,
      $protected: {
        _options: {
          settings: global_add_file_settings,
          show_subject: null,
          show_type: null
        }
      },

      $constructor: function() {
          var
            bindings = [
                ['show_subject', 'ctx_show_subject', true, 'fromProperty'],
                ['show_type', 'ctx_show_type', true, 'fromProperty']
            ],
            binder = new ContextBinder({bindings: bindings});
          binder.bindControl(this, this.getLinkedContext(), 'syncContext');
      },

      init: function() {
        moduleClass.superclass.init.call(this);

        var
          self = this,
          subject = this.getChildControlByName('fd_subject'),
          type = this.getChildControlByName('fd_type'),
          btn = this.getChildControlByName('b_add_file'),
          _form = document.getElementById('form_file');

        subject.subscribe('onValueChange', function(eo, v) {
          self.setProperty('show_subject', (v == 0));
          self._notifyOnPropertyChanged('show_subject');
        });

        type.subscribe('onValueChange', function(eo, v) {
          self.setProperty('show_type', (v == 0));
          self._notifyOnPropertyChanged('show_type');
        });

        btn.subscribe('onActivated', function() {
          _form.submit();
        });

      }
   });

   return moduleClass;
});

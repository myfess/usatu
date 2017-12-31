define('js!mod_usatu/subject_cats/subject_cats',
  [
  'js!SBIS3.CORE.CompoundControl',
  'tmpl!mod_usatu/subject_cats/subject_cats',
  'js!WS.Data/Source/Memory',
  'js!WS.Data/Source/SbisService'
  ],

  function(CompoundControl, dotTplFn, Memory, SbisService) {
    var moduleClass = CompoundControl.extend({
      _dotTplFn: dotTplFn,
      $protected: {
        _options: {
          subject_id: global_subject_id,
          subs: []
        }
      },

      $constructor: function() {
      },

      init: function() {
        moduleClass.superclass.init.call(this);
        var self = this;

        new SbisService({
          endpoint: {
            contract: 'edu_files'
          }
        }).call('sub_list', {subject_id: self._options.subject_id})
          .addCallback(function(dataSet) {
            self.setProperty('subs', dataSet.getAll());
            self.rebuildMarkup();
          }
        );
      }
   });

   return moduleClass;
});

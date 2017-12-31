define('js!mod_usatu/my_drop_down/my_drop_down',
  [
    'js!SBIS3.CORE.FieldDropdown',
    'js!WS.Data/Source/SbisService'
  ],

  function(FieldDropdown, SbisService) {
    var moduleClass = FieldDropdown.extend({
      $protected: {
        _options: {
          method_name: '',
          params: {},
          key_id: 'id',
          key_value: 'value',
          init_value: null
        }
      },

      init: function() {
        moduleClass.superclass.init.call(this);

        var self = this;

        new SbisService({
          endpoint: {
            contract: 'edu_files'
          }}).call(this._options.method_name, this._options.params)

          .addCallback(function(dataSet) {
            var
              subs = dataSet.getAll(),
              _data = [];
            _data.push({key: -1, value: ''});
            _data.push({key: 0, value: 'Ввести вручную'});
            for (var i = 0; i < subs.getCount(); i++) {
              var rec = subs.at(i);
              _data.push({
                key: rec.get(self._options.key_id),
                value: rec.get(self._options.key_value)
              });
            }
            self.setData(_data);
            self.setValue(self._options.init_value);
          }
        );
      }

   });

   return moduleClass;
});

define('js!mod_usatu/my_data_grid_view/my_data_grid_view',
[
'js!SBIS3.CORE.CompoundControl',
'tmpl!mod_usatu/my_data_grid_view/my_data_grid_view',
'js!WS.Data/Query/Query'
],

function(CompoundControl, dotTplFn, Query) {
  var moduleClass = CompoundControl.extend({
    _dotTplFn: dotTplFn,
    $protected: {
      _options: {
        columns: [],
        filter: {},
        dataSource: null,
        _data: null,
        border_spacing: 10,
        data_handler: null
      }
    },

    init: function() {
      moduleClass.superclass.init.call(this);
    },

    setColumns: function(columns) {
      this._options.columns = columns;
      this._rebuild();
    },

    setFilter: function(filter) {
      this._options.filter = filter;
      this._reload();
    },

    setDataSource: function(data_source) {
      this._options.dataSource = data_source;
      this._reload();
    },

    _reload: function() {
      if (!this._options.dataSource) {
        return;
      }

      var
        self = this,
        query = new Query();

      query.where(this._options.filter);
      this._options.dataSource.query(query)
        .addCallback(function(dataSet) {
          self._options._data = dataSet.getAll();
          if (self._options.data_handler !== null) {
            self._options._data = self._options.data_handler(self._options._data);
          }
          self._rebuild();
        }
      );
    },

    _rebuild: function() {
      this.rebuildMarkup();
    }

 });

 return moduleClass;
});

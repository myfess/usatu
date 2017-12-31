/**
 * @author my_fess
 */
define('js!mod_usatu/board/board',
[
  'js!SBIS3.CORE.CompoundControl',
  'tmpl!mod_usatu/board/board',
  'js!WS.Data/Source/Memory',
  'js!WS.Data/Source/SbisService',
  'js!mod_usatu/my_data_grid_view/my_data_grid_view',
  'tmpl!mod_usatu/board/caption',
  'tmpl!mod_usatu/board/last_msg',
  'css!mod_usatu/board/board',
],

function(CompoundControl, dotTplFn, Memory, SbisService) {
  var moduleClass = CompoundControl.extend({
    _dotTplFn: dotTplFn,
    $protected: {
      _options: {
      }
    },

    init: function() {
      moduleClass.superclass.init.call(this);

      var dataSource = new SbisService({
        endpoint: {
          contract: 'board'
        },
        binding: {
            query: 'theme_list'
        }
      });
      var myDataView = this.getChildControlByName('TableA');


      var newColumns = [
        {
          title: 'Тема',
          cellTemplate: 'tmpl!mod_usatu/board/caption'
        },
        {
          title: 'Последнее сообщение',
          cellTemplate: 'tmpl!mod_usatu/board/last_msg',
          width: 160
        }

      ];

      myDataView.setColumns(newColumns);
      myDataView.setDataSource(dataSource);
    },

    date_converter: function(_data) {
      var _options = {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
      };
      _data.addField({name: 'dt_format', type: 'string'});
      for (var i = 0; i < _data.getCount(); i++) {
        var _d = new Date(0);
        _d.setUTCSeconds(_data.at(i).get('dt_last_msg'));
        var _dd = _d.toLocaleString('ru-ru', _options);
        _data.at(i).set('dt_format', _dd.replace(/ г./i, ''));
      }
      return _data;
    }


  });

  return moduleClass;
});

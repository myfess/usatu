/**
 * @author my_fess
 */
define('js!mod_usatu/files_brws/files_brws',
  [
    'js!SBIS3.CORE.CompoundControl',
    'tmpl!mod_usatu/files_brws/files_brws',
    'js!WS.Data/Source/Memory',
    'js!WS.Data/Source/SbisService',
    'css!mod_usatu/files_brws/files_brws',
    'tmpl!mod_usatu/files_brws/desc_cell',
    'tmpl!mod_usatu/files_brws/date_cell',
    'tmpl!mod_usatu/files_brws/subject_cell',
    'js!mod_usatu/my_data_grid_view/my_data_grid_view'
  ],

  function(CompoundControl, dotTplFn, Memory, SbisService) {
    /**
     * mod_usatu/files_brws
     * @class mod_usatu/files_brws
     * @extends SBIS3.CORE.CompoundControl
     */
    var moduleClass = CompoundControl.extend(/** @lends mod_usatu/files_brws.prototype */{
      _dotTplFn: dotTplFn,
      $protected: {
        _options: {
          subject: global_subject_id,
          type: global_type_id
         }
      },
      $constructor: function() {
      },

      init: function() {
         moduleClass.superclass.init.call(this);

          var dataSource = new SbisService({
            endpoint: {
              contract: 'edu_files'
            },
            binding: {
                query: 'list'
            }
          });
          var myDataView = this.getChildControlByName('TableA');

          // Берем глобальные настройки того где мы сейчас находимся
          var _filter = {
            'subject': this._options.subject,
            'type': this._options.type
          };

          var newColumns = [];
          if (this._options.subject !== null) {
            newColumns = [
              {
                title: 'Описание',
                cellTemplate: 'tmpl!mod_usatu/files_brws/desc_cell',
                additional_data: {
                  is_editor: usatu_global_config.is_editor,
                  show_type: (this._options.type === null)
                }
              },
              {
                title: 'Дата',
                width: 100,
                cellTemplate: 'tmpl!mod_usatu/files_brws/date_cell'
              }
            ];
          } else {
            newColumns = [
              {
                title: 'Дисциплина',
                cellTemplate: 'tmpl!mod_usatu/files_brws/subject_cell'
                // width: 300
              },
              {
                title: 'Количество',
                width: 50,
                field: 'count'
              }
            ];
          }

          myDataView.setColumns(newColumns);
          myDataView.setFilter(_filter);
          myDataView.setDataSource(dataSource);
      }
   });

   return moduleClass;
});

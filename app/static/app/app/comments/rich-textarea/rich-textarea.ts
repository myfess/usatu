import { Component, NgModule, ElementRef, ViewChild } from '@angular/core';
import { Input, Output, EventEmitter } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'rich-textarea',
  templateUrl: 'rich-textarea.html',
  styleUrls: [ 'rich-textarea.css' ]
})
export class RichTextAreaComponent {
  @ViewChild("textareamain") _textarea: ElementRef;
  @Input('disabled') _disabled:boolean = true;
  @Input('messageText') message_text: string;
  @Output() messageTextChange: EventEmitter<string> = new EventEmitter<string>();

  constructor() {
  }

  textChanged(input_text) {
    this.messageTextChange.emit(input_text);
  }

  /////////////////////////////
  // RTE

  openTags = [''];
  closedTags = ['dummy', 'b', 'i', 'u', 's', 'code', 'quote', 'me', 'list'];

  font_colors = [
    ['skyblue', 'Светло-голубой'],
    ['royalblue', 'Голубой'],
    ['blue', 'Синий'],
    ['darkblue', 'Тёмно-синий'],
    ['orange', 'Оранжевый'],
    ['orangered', 'Морковный'],
    ['crimson', 'Бордовый'],
    ['red', 'Красный'],
    ['firebrick', 'Кирпичный'],
    ['darkred', 'Коричневый'],
    ['green', 'Зелёный'],
    ['limegreen', 'Салатовый'],
    ['seagreen', 'Болотный'],
    ['deeppink', 'Розовый'],
    ['tomato', 'Томатный'],
    ['coral', 'Coral'],
    ['purple', 'Сиреневый'],
    ['indigo', 'Фиолетовый'],
    ['burlywood', 'Горчичный'],
    ['sandybrown', 'Песчаный'],
    ['sienna', 'Кофейный'],
    ['chocolate', 'Шоколадный'],
    ['teal', 'Морской'],
    ['silver', 'Серебряный']
  ];

  font_sizes = [
    ['9', 'Мелкий'],
    ['11', 'Небольшой'],
    ['13', 'Средний'],
    ['16', 'Большой'],
    ['20', 'Огромный']
  ];

  font_fonts = [
    ['arial', 'Arial'],
    ['courier', 'Courier'],
    ['impact', 'Impact'],
    ['tahoma', 'Tahoma'],
    ['times', 'Times'],
    ['verdana', 'Verdana']
  ];

  select_list = [
    ['1', '1 Пункт'],
    ['2', '2 Пункта'],
    ['3', '3 Пункта'],
    ['4', '4 Пункт'],
    ['5', '5 Пунктов']
  ];

  select_align = [
    ['left', 'По левому краю'],
    ['center', 'По центру'],
    ['right', 'По правому краю']
  ];

  toolbar_buttons = [
    ['ubbBasic', 'b', 'Жирный[B]', 'bold.gif'],
    ['ubbBasic', 'i', 'Наклонный[I]', 'italics.gif'],
    ['ubbBasic', 'u', 'Подчёркнутый[U]', 'underline.gif'],
    ['ubbBasic', 'code', 'Код [G]', 'code.gif'],
    ['ubbBasic', 'quote', 'Цитата[Q]', 'quote.gif'],
    ['ubbList', '', 'Список [L]', 'list.gif'],
    ['ubbListItem', null, 'Пункт списка [K]', 'listitem.gif'],
    ['ubbHref', null, 'Ссылка [H]', 'url.gif'],
    ['ubbEmail', null, '[E]mail', 'email.gif'],
    ['ubbImage', null, 'Картинка[P]', 'image.gif'],
    ['ubbSpoil', null, 'Скрытый текст', 'spoiler.gif']
  ];

  smiles = [
    [':huh:', 'huh'],
    [':o', 'ohmy'],
    [';)', 'wink'],
    [':P', 'tongue'],
    [':D', 'biggrin'],
    [':lol:', 'laugh'],
    ['B)', 'cool'],
    [':rolleyes:', 'rolleyes'],
    ['{_{', 'dry'],
    [':)', 'smile'],
    [':angry:', 'mad'],
    [':(', 'sad'],
    [':unsure:', 'unsure'],
    [':blink:', 'blink'],
    [':ph34r:', 'ph34r']
  ];

  ubbCode(code) {
    let textarea = this.get_textarea();
    let v = textarea.value;
    let len = v.length;
    let start = textarea.selectionStart;
    let end = textarea.selectionEnd;
    let scrollTop = textarea.scrollTop;
    let scrollLeft = textarea.scrollLeft;
    let new_value = v.substring(0, start) + code + v.substring(end, len);
    textarea.value = new_value;
    this.message_text = new_value;
    textarea.scrollTop = scrollTop;
    textarea.scrollLeft = scrollLeft;
    textarea.focus();
    textarea.setSelectionRange(start, start + code.length);
    this.textChanged(textarea.value);
  }

  getText() {
    let textarea = this.get_textarea();
    let len = textarea.value.length;
    let start = textarea.selectionStart;
    let end = textarea.selectionEnd;
    let sel = textarea.value.substring(start, end);
    return sel;
  }

  get_textarea():HTMLTextAreaElement {
    return this._textarea.nativeElement;
  }

  isUrl(text) {
    return true;
  }

  isEmail(str) {
    let r1 = new RegExp("(@.*@)|(\\.\\.)|(@\\.)|(^\\.)");
    let r2 = new RegExp("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,4}|[0-9]{1,3})(\\]?)$");
    return (!r1.test(str) && r2.test(str));
  }

  returnFocus() {
    setTimeout(this.get_textarea().focus, 10);
  }

  resetList(list) {
    let _tmp = function () {
      list.options[0].selected = true;
    }
    setTimeout(_tmp, 10);
  }

  removeElement(array, value) {
    array = array.split(',');
    let pos;
    for (let i = 0; i < array.length; i++) {
      if (array[i] == value) {
        pos = i;
        break;
      }
    }
    for (let i = pos; i < (array.length - 1); i++) {
      array[i] = array[i + 1];
    }
    array.length = array.length - 1;
    return array.join(',');
  }

  ubbBasic(code) {
    let text = this.getText();
    if (text) {
      code = '[' + code + ']' + text + '[/' + code + ']';
      this.ubbCode(code);
    } else {
      let tag;
      if (this.openTags.join(',').indexOf(','+code) != -1) {
        tag = '[/' + code + ']';
        this.openTags = this.removeElement(this.openTags.join(','),code).split(',');
        this.closedTags[this.closedTags.length] = code;
      } else {
        tag = '[' + code + ']';
        this.closedTags = this.removeElement(this.closedTags.join(','),code).split(',');
        this.openTags[this.openTags.length] = code;
      }
      this.ubbCode(tag);
    }
  }

  ubbFont(list) {
    let attrib = list.name.substring(1, list.name.length);
    let value = list.options[list.selectedIndex].value;
    if (value && attrib) {
      let code = '[' + attrib + '=' + value + ']' + this.getText() + '[/' + attrib + ']';
      this.ubbCode(code);
    }
    this.resetList(list);
  }

  ubbAlign(align) {
    if (!align.value) {
      return;
    }
    let code = '[align=' + align.value + ']' + this.getText() + '[/align]';
    this.ubbCode(code);
    this.resetList(align);
  }

  ubbList(size) {
    let text = this.getText();
    if (!size.value && !text) {
      this.ubbBasic('list');
    } else if (!size.value && text) {
      let regExp = /\n/g;
      text = text.replace(regExp,'\n[*]');
      let code = '[list]\n[*]' + text + '\n[/list]\n';
      this.ubbCode(code);
    } else {
      if (text) {
        text += '\n';
      }
      let code = text + '[list]\n';
      for (let i = 0; i < size.value; i++) {
        code += '[*]\n';
      }
      code += '[/list]\n';
      this.ubbCode(code);
      this.resetList(size);
    }
  }

  ubbListItem() {
    this.ubbCode('[*]' + this.getText());
  }

  ubbHref() {
    let url = 'http://';
    let desc = '';
    let text = this.getText();
    if (text) {
      if (this.isUrl(text)) {
        url = text;
      } else {
        desc = text;
      }
    }
    url = prompt('Введите ссылку:', url) || '';
    desc = prompt('Описание ссылки:', desc) || url;
    if (!this.isUrl(url)) {
      this.returnFocus();
      return;
    }
    let code = '[url=' + url + ']' + desc + '[/url]';
    this.ubbCode(code);
  }

  ubbEmail() {
    let email = '';
    let desc = '';
    let text = this.getText();
    if (text) {
      if (this.isEmail(text)) {
        email = text;
      } else {
        desc = text;
      }
    }
    email = prompt('Введите E-mail адрес:', email) || '';
    desc = prompt('Введите описание:', desc) || email;
    if (!this.isEmail(email)) {
      this.returnFocus(); return;
    }
    let code = '[email=' + email + ']' + desc + '[/email]';
    this.ubbCode(code);
  }

  ubbImage() {
    let text = this.getText();
    let url = (text && this.isUrl) ? text : prompt("\nВведите URL картинки:", "http://") || "";
    if (!url) {
      return;
    }
    let code = "[IMG]" + url + "[/IMG]";
    this.ubbCode(code);
  }

  rand_string() {
    let digi = [
      "A","B","C","D","E","F","G","H","J","K","L","M","N","P","Q","R","S","T","U","V","W","Y","Z",
      "a","b","c","d","e","f","g","h","j","k","l","m","n","p","q","r","s","t","u","v","w","y","z"
    ];
    let res = "";
    let n = digi.length - 1;
    for (let i = 1; i <= 10; i++) {
      let rand = Math.floor(Math.random() * (n + 1));
      res += digi[rand];
    }
    return res;
  }

  ubbSpoil() {
    let tag_id = this.rand_string();
    let caption_open = 'Читать далее';
    let caption_close = 'Скрыть';
    let content = 'ЗДЕСЬ ВВЕДИТЕ СКРЫТЫЙ ТЕКСТ'

    let text = this.getText();
    if (text) {
      content = text;
    }
    tag_id =  prompt('Введите идентификатор:', tag_id) || tag_id;
    caption_open = prompt('Введите заголовок при скрытом:', caption_open) || caption_open;
    caption_close = prompt('Введите заголовок при показаном:', caption_close) || caption_close;
    content = prompt('Введите текст:',content) || content;

    let code = '[htext=' + tag_id + ',' + caption_open + ',' + caption_close + ']';
    code += content + '[/htext]';
    this.ubbCode(code);
  }

  emoticon(theSmilie) {
    this.ubbCode(this.getText() + ' ' + theSmilie + ' ');
  }
}


@NgModule({
  imports: [BrowserModule, FormsModule],
  declarations: [RichTextAreaComponent],
  providers: [],
  exports: [RichTextAreaComponent]
})
export class RichTextAreaModule { }

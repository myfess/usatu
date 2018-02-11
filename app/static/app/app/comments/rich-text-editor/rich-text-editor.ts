import { Component, Input, NgModule, ElementRef, ViewChild } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { ReCaptchaModule } from 'angular2-recaptcha';
import { MdButtonModule, MdProgressSpinnerModule } from '@angular/material';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { UsatuRpcService } from '../../usatu-rpc/usatu-rpc.service';
import { UsatuConfigService } from '../../usatu-config/usatu-config.service';
import { RichTextAreaModule } from '../rich-textarea/rich-textarea';

import { Subject } from 'rxjs/Subject';
import 'rxjs/add/operator/debounceTime';
import "rxjs/add/operator/distinctUntilChanged"

@Component({
  moduleId: module.id,
  selector: 'rich-text-editor',
  templateUrl: 'rich-text-editor.html',
  styleUrls: [ 'rich-text-editor.css' ]
})
export class RichTextEditorComponent {
  message = {
    'id': null,
    'id_parent': null,
    'text': '',
    'title': '',
    'attach': false,
    'draft': false,
    'is_news': true,
    'is_board_theme': false,
    'is_comment': false,
    'is_blog_post': false
  };

  loading:boolean = false;
  rowsCount:number = 20;
  preview_text = '';
  modelChanged: Subject<string> = new Subject<string>();
  g_recaptcha_response = null;

  constructor(
      private rpcService: UsatuRpcService,
      private _config: UsatuConfigService,
      public elementRef: ElementRef) {

    this.getInputAttribute('message-id', 'id');
    this.getInputAttribute('parent-id', 'id_parent');
    this.getInputAttribute('board-theme', 'is_board_theme');
    this.getInputAttribute('blog-post', 'is_blog_post');

    if (this.message.is_blog_post) {
        this.rowsCount = 42;
    }

    this.message.is_comment = (this.message.id_parent !== null && this.message.id_parent != 0);
    this.message.is_news = !this.message.is_comment;

    if (this.message.is_board_theme) {
      this.message.is_news = false;
      this.message.is_comment = false;
    }

    this.modelChanged
      .debounceTime(4000)
      .distinctUntilChanged() // only emit if value is different from previous value
      .subscribe(v => this.updatePreview(v));
  }

  getInputAttribute(attribute_name, property_name) {
    // Ограничение Angular 2: корневой компоент не принимает входные свойства
    let native = this.elementRef.nativeElement;

    if (!native.hasAttribute(attribute_name)) {
      return;
    }

    let v = native.getAttribute(attribute_name);
    if (v === null || v == 'null') {
      this.message[property_name] = null;
    } else if (v == 'true') {
        this.message[property_name] = true;
    } else if (v == 'false') {
        this.message[property_name] = false;
    } else {
      this.message[property_name] = Number(v);
    }
  }

  ngOnInit(): void {
    this.get_message();
  }

  handleCorrectCaptcha(event) {
    this.g_recaptcha_response = event;
  }

  handleExpiredCaptcha() {
    this.g_recaptcha_response = null;
  }

  get_message() {
    if (this.message.id === null) {
      return;
    }
    this.loading = true;
    return this.rpcService.call('get_message',
      { 'id': this.message.id })
      .then(res => this.handlerRead(res));
  }

/*
  textChanged(input_text) {
    this.modelChanged.next(input_text);
  }
*/
    updatePreview(input_text) {
        return this.rpcService.call('get_message_preview',
        {
            'text': input_text,
            'blog_post': this.message.is_blog_post
        })
        .then(res => this.handlerPreview(res));
    }

  deleteMessage() {
    let _msg = 'Вы уверены, что хотите удалить это сообщение';
    if (!confirm(_msg)) {
      return;
    }

    this.loading = true;
    return this.rpcService.call('delete_message',
      { 'id': this.message.id })
      .then(res => this.handlerDelete(res));
  }

  private handlerRead(data) {
    this.message = data;
    this.loading = false;
    //this.message_text = this.message.text;
    this.updatePreview(this.message.text);
  }

  private handlerPreview(data) {
    this.preview_text = data.preview;
  }

  private handlerDelete(data) {
    document.location.href = $.cookie('usatu_last_page');
  }

  private handlerWrite(data) {
    document.location.href = $.cookie('usatu_last_page');
  }

  writeMessage() {
    if (this._config.config().captcha_on && this.message.id === null) {
      if (!this.g_recaptcha_response) {
        alert("Необходимо ввести капчу");
        return;
      }
    }

    this.loading = true;
    return this.rpcService.call('write_message',
      {
        'id': this.message.id,
        'id_parent': this.message.id_parent,
        'board_theme': this.message.is_board_theme,
        'title': this.message.title,
        'text': this.message.text,
        'attach': this.message['attach'],
        'draft': this.message['draft'],
        'g-recaptcha-response': this.g_recaptcha_response
      })
      .then(res => this.handlerWrite(res));
  }


  @Input() set message_text(data: string) {
    this.message.text = data;
    this.modelChanged.next(this.message.text);
  }

  get message_text() {
    return this.message.text;
  }
}


@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    RichTextAreaModule,
    NoopAnimationsModule, MdButtonModule, MdProgressSpinnerModule,
    ReCaptchaModule
  ],
  declarations: [RichTextEditorComponent],
  providers: [UsatuRpcService, UsatuConfigService],
  bootstrap: [RichTextEditorComponent]
})
export class RichTextEditorModule { }

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
  enableProdMode();
}

platformBrowserDynamic().bootstrapModule(RichTextEditorModule);

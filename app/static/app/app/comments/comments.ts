import { Component, Input, ElementRef } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { UsatuRpcService } from '../usatu-rpc/usatu-rpc.service';
import { UsatuConfigService } from '../usatu-config/usatu-config.service';
import { CommentModule } from './comment/comment';
import { ReplyModule } from './reply/reply';
import { PagesModule } from './pages/pages';

@Component({
  moduleId: module.id,
  selector: 'comments',
  templateUrl: 'comments.html',
  styleUrls: [ 'comments.css' ]
})
export class CommentsComponent {
  object_id:Number = null;
  pages_count:Number = 0;
  page_link:string = '';
  comments = [];

  constructor(
      private rpcService: UsatuRpcService,
      private _config: UsatuConfigService,
      public elementRef: ElementRef) {

    let native = this.elementRef.nativeElement;
    this.object_id = Number(native.getAttribute("object-id"));
    this.page_link = native.getAttribute("page-link");
  }

  ngOnInit(): void {
    this.get_comments();
  }

  get_comments() {
    return this.rpcService.call('get_comments',
      {
        'id': this.object_id,
        'page': this._config.config().comments_page
      })
      .then(res => this.handlerRead(res));
  }

  private handlerRead(data) {
    this.comments = data.comments;
    this.pages_count = data.pages_count;
    for (let c of this.comments) {
      // Преобразуем время секунд эпохи в локальное время
      c['dt'] = new Date(0);
      c['dt'].setUTCSeconds(c.time);
    }
  }
}


@NgModule({
  imports: [
    BrowserModule,
    HttpModule,
    CommentModule,
    ReplyModule,
    PagesModule
  ],
  declarations: [CommentsComponent],
  providers: [UsatuRpcService, UsatuConfigService],
  bootstrap: [CommentsComponent]
})
export class CommentsModule { }

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
  enableProdMode();
}

platformBrowserDynamic().bootstrapModule(CommentsModule);

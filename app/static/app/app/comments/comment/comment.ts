import { Component, Input } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { UsatuConfigService } from '../../usatu-config/usatu-config.service';
import { DatePipe } from '@angular/common'
import { ReplyModule } from '../reply/reply';

@Component({
  moduleId: module.id,
  selector: 'comment',
  templateUrl: 'comment.html',
  styleUrls: [ 'comment.css' ]
})
export class CommentComponent {
  @Input('_data') _data = null;
  @Input('delete-comments') delete_comments = false;
  show_reply_block = false;

  constructor(
    private _config: UsatuConfigService,
    public datepipe: DatePipe) {
  }

  ngOnInit(): void {
  }

  show_reply() {
    this.show_reply_block = !this.show_reply_block;
  }

  public format_datetime(dt) {
    return this.datepipe.transform(dt, 'yyyy-MM-dd HH:mm');
  }
}


@NgModule({
  imports: [ BrowserModule, ReplyModule ],
  declarations: [CommentComponent],
  providers: [UsatuConfigService, DatePipe],
  exports: [CommentComponent]
})
export class CommentModule { }


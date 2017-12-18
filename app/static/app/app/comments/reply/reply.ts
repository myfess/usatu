import { Component, Input, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { BrowserModule } from '@angular/platform-browser';
import { UsatuConfigService } from '../../usatu-config/usatu-config.service';
import { UsatuRpcService }     from '../../usatu-rpc/usatu-rpc.service';
import { ReCaptchaModule } from 'angular2-recaptcha';
import { MdProgressSpinnerModule } from '@angular/material';

@Component({
  moduleId: module.id,
  selector: 'reply',
  templateUrl: 'reply.html',
  styleUrls: [ 'reply.css' ]
})
export class ReplyComponent {
  @Input('object-id') object_id:number = null;
  input_text = '';
  avatar = null;
  g_recaptcha_response = null;
  loading = false;

  constructor(
    private _config: UsatuConfigService,
    private rpcService: UsatuRpcService) {
  }

  handleCorrectCaptcha(event) {
    this.g_recaptcha_response = event;
  }

  handleExpiredCaptcha() {
    this.g_recaptcha_response = null;
  }

  ngOnInit(): void {
    let uid = this._config.config().user_id;
    let _avatar = this._config.config().avatar;
    if (uid !== null && _avatar === null) {
      this.rpcService.call('get_user_info', {'id': uid})
        .then(res => this.handlerUserInfo(res));
    } else if (_avatar !== null) {
      this.avatar = _avatar;
    }
  }

  add_comment(parent_id) {
    if (this._config.config().captcha_on) {
      if (!this.g_recaptcha_response) {
        alert("Необходимо ввести капчу");
        return;
      }
    }

    this.loading = true;
    this.rpcService.call('new_comment',
      {
        'g-recaptcha-response': this.g_recaptcha_response,
        'text': this.input_text,
        'parent_id': this.object_id
      })
      .then(res => this.handlerNewComment(res));
  }

  private handlerUserInfo(data) {
    this.avatar = data.avatar;
    // Запоминаем автарку чтобы второй раз не грузить
    this._config.config().avatar = data.avatar;
  }

  private handlerNewComment(data) {
    this.loading = false;
    if (data['result']) {
      this.input_text = '';
      location.reload();
    } else {
      if (data['error']) {
        alert(data['error']);
      }
    }
  }
}


@NgModule({
  imports: [ BrowserModule, FormsModule, ReCaptchaModule, MdProgressSpinnerModule ],
  declarations: [ReplyComponent],
  providers: [UsatuConfigService, UsatuRpcService ],
  exports: [ReplyComponent]
})
export class ReplyModule { }


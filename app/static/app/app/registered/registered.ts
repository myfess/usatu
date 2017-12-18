import { Component, Input } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { UsatuRpcService } from '../usatu-rpc/usatu-rpc.service';
import { UsatuConfigService } from '../usatu-config/usatu-config.service';
import { isDevMode } from '@angular/core';

import 'rxjs/add/operator/toPromise';
import 'jquery.cookie';

declare var __moduleName: string;
@Component({
  moduleId: module.id,
  selector: 'registered',
  templateUrl: 'registered.html',
  styleUrls: [ 'registered.css' ]
})
export class RegisteredComponent {
  user_name: string;
  user_id: number;
  show_user_link: boolean;
  loading:boolean = false;

  constructor(
      private rpcService: UsatuRpcService,
      private _config: UsatuConfigService) {
    this.user_name = _config.config().user_name;
    this.user_id = parseInt(_config.config().user_id, 10);
    this.show_user_link = (this.user_id != -1);
  }

  sign_out() {
    this.loading = true;
    this.rpcService.call('sign_out', {})
      .then(res => this.handlerSignOut(res));
  }

  private handlerSignOut(data) {
    $.cookie('usatu_auth', null, { path: '/' });
    location.reload();
  }
}


@NgModule({
  imports: [
    BrowserModule,
    HttpModule
  ],
  declarations: [RegisteredComponent],
  providers: [UsatuRpcService, UsatuConfigService],
  bootstrap: [RegisteredComponent]
})
export class RegisteredModule { }

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
  enableProdMode();
}

platformBrowserDynamic().bootstrapModule(RegisteredModule);

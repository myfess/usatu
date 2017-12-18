import { Component } from '@angular/core';
import { UsatuRpcService }     from '../usatu-rpc/usatu-rpc.service';

import 'rxjs/add/operator/toPromise';
import 'jquery.cookie';


@Component({
  moduleId: module.id,
  selector: 'auth',
  templateUrl: 'auth.component.html',
  styleUrls: [ 'auth.component.css' ]
})
export class AuthComponent {
  login:string = null;
  pass:string = null;
  auth_msg = '';
  loading:boolean = false;

  constructor(private chairsService: UsatuRpcService) {
  }

  sign_in() {
    if (this.login.length == 0) {
      this.auth_msg = 'LOGIN_ERROR';
      return;
    }
    if (this.pass.length == 0) {
      this.auth_msg = 'PASSWORD_ERROR';
      return;
    }

    this.loading = true;
    this.chairsService.call('sign_in',
      {
        'login': this.login,
        'password': this.pass
      })
      .then(res => this.handlerSignIn(res));
  }

  private handlerSignIn(data) {
    if (!('token' in data) || data.token === null) {
      this.auth_msg = data.auth_msg;
      this.loading = false;
    } else {
      $.cookie("usatu_auth", data.token, { expires : 90, path: '/' });
      location.reload();
    }
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    // for demo purposes only
    return Promise.reject(error.message || error);
  }

  is_backend_msg() {
    return ((this.auth_msg != 'LOGIN_ERROR') && (this.auth_msg != 'PASSWORD_ERROR'));
  }
}



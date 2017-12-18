import { Injectable, Inject, Component }    from '@angular/core';
import { Headers, Http, RequestOptions } from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class UsatuRpcService {
  private apiUrl = '/api_usatu';
  private dialog;

  constructor(private http: Http) {
  }

  call(method_name, data): Promise<any> {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });

    let post_data = {
      'method': method_name,
      'data': data
    };

    return this.http.post(this.apiUrl, post_data, options).toPromise().then(
        res => this.handlerCallResult(res.json()))
      .catch(this.handleError);
  }

  private handlerCallResult(res) {
    if ('error_msg' in res) {
      alert(res.error_msg);
      return res;
    } else {
      return res;
    }
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error);
    // for demo purposes only
    return Promise.reject(error.message || error);
  }
}


import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule }    from '@angular/http';
import { UsatuRpcService }          from './usatu-rpc/usatu-rpc.service';
import { FormsModule } from '@angular/forms';
import { AuthComponent }  from './auth/auth.component';


@NgModule({
  imports:      [
    BrowserModule,
    HttpModule,
    FormsModule
  ],
  declarations: [ AuthComponent ],
  providers:    [ UsatuRpcService ],
  bootstrap:    [ AuthComponent ]
})
export class AuthModule { }

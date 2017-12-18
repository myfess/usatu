import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule }    from '@angular/http';
import { UsatuRpcService }          from '../usatu-rpc/usatu-rpc.service';
import { ChairsStructComponent }  from './chairs-struct';


@NgModule({
  imports:      [ BrowserModule, HttpModule ],
  declarations: [ ChairsStructComponent ],
  providers:    [ UsatuRpcService ],
  exports: [ ChairsStructComponent ]
})
export class ChairsStructModule { }

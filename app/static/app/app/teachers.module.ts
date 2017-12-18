import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule }    from '@angular/http';
import { UsatuRpcService }          from './usatu-rpc/usatu-rpc.service';
import { UsatuConfigService } from './usatu-config/usatu-config.service';
import { ChairsStructComponent }  from './chairs-struct/chairs-struct';
import { TeachersIndexComponent }  from './teachers-index/teachers-index.component';


@NgModule({
  imports:      [ BrowserModule, HttpModule ],
  declarations: [ ChairsStructComponent, TeachersIndexComponent ],
  providers:    [ UsatuRpcService, UsatuConfigService ],
  bootstrap:    [ ChairsStructComponent, TeachersIndexComponent ]
})
export class TeachersModule { }

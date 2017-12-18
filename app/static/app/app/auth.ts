import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AuthModule }  from './auth.module';
import { enableProdMode } from '@angular/core';
import { UsatuConfigService } from './usatu-config/usatu-config.service';

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
  enableProdMode();
}

platformBrowserDynamic().bootstrapModule(AuthModule);

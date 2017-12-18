import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { TeachersModule }  from './teachers.module';
import { enableProdMode } from '@angular/core';
import { UsatuConfigService } from './usatu-config/usatu-config.service';
import { isDevMode } from '@angular/core';

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
  enableProdMode();
}

platformBrowserDynamic().bootstrapModule(TeachersModule);

import { Component, Input, NgModule } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { BrowserModule } from '@angular/platform-browser';
import { UsatuConfigService } from '../../usatu-config/usatu-config.service';

@Component({
  moduleId: module.id,
  selector: 'pages',
  templateUrl: 'pages.html',
  styleUrls: [ 'pages.css' ]
})
export class PagesComponent {
  @Input('pages-count') pages_count:Number = 0;
  @Input('page-link') page_link:string = '';

  constructor(private _config: UsatuConfigService) { }

  createRange(n) {
    let pages_range = 4;
    let items: number[] = [];
    let current = this._config.config().comments_page;
    let last_page = false;
    for (let i = 1; i <= n; i++) {
      if (Math.abs(i - current) < pages_range
          || Math.abs(i - 1) < pages_range
          || Math.abs(i - n) < pages_range) {
        last_page = true;
        items.push(i);
      } else {
        if (last_page) {
          items.push(0);
        }
        last_page = false;
      }
    }
    return items;
  }
}


@NgModule({
  imports: [ BrowserModule ],
  declarations: [PagesComponent],
  providers: [UsatuConfigService ],
  exports: [PagesComponent]
})
export class PagesModule { }


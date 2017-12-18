import { Injectable } from '@angular/core';

declare var usatu_global_config: any;

@Injectable()
export class UsatuConfigService {
  constructor() { }

  config() {
    return usatu_global_config;
  }
}

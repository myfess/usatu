import { Component, OnInit } from '@angular/core';
import { DomSanitizer }     from '@angular/platform-browser';
import { UsatuConfigService } from '../usatu-config/usatu-config.service';

@Component({
  moduleId: module.id,
  selector: 'teachers-index',
  templateUrl: 'teachers-index.component.html'
})
export class TeachersIndexComponent {
  chars_en = [
    'A', 'B', 'V', 'G', 'D', 'E', 'JO', 'ZH', 'Z', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F', 'KH', 'C', 'CH', 'SH',
    'SHCH', 'EH', 'JU', 'JA'];
  chars_ru = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л',
    'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш',
    'Щ', 'Э', 'Ю', 'Я'];

  constructor(
    private domSanitizer: DomSanitizer,
    private _config: UsatuConfigService) {
  }

  testfunc(_char) {
    let a =  "javascript:goto('" + _char + "')";
    let b = this.domSanitizer.bypassSecurityTrustUrl(a);
    return b;
  }

}



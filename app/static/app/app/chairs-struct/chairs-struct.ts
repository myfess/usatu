import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import { UsatuRpcService }     from '../usatu-rpc/usatu-rpc.service';

@Component({
  moduleId: module.id,
  selector: 'chairs-struct',
  templateUrl: 'chairs-struct.html',
  styleUrls: [ 'chairs-struct.css' ]
})
export class ChairsStructComponent implements OnInit {
  chairs = [];
  @Input('full-name') full_name:boolean;
  @Input('selected-chair') selected_chair:number; // По умолчанию неизвестная кафедра
  selected_faculty:number;

  constructor(private chairsService: UsatuRpcService) {
  }

  getData(): Promise<any> {
    return this.chairsService.call('get_chairs_struct', {})
      .then(res => this.chairs = res.faculties);
  }

  ngOnInit(): void {
    let def = this.getData();
    def.then(res => this.openSelectedFaculty());
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['selected_chair']) {
      this.openSelectedFaculty();
    }
  }

  openSelectedFaculty() {
    for (let f of this.chairs) {
      for (let c of f.chairs) {
        if (c.id == this.selected_chair) {
          this.selected_faculty = f.id;
        }
      }
    }
  }

  public chair_click_tree(event, item) {
    if ($('#pic_' + item)) {
      this.choose_image(item);
    }
    this.view(item);
  }

  private view(_id) {
    let id = '#tree_' + _id;
    if ($(id).css('display') == 'none' || $(id).css('display') == '') {
      $(id).css('display', 'block');
    } else {
      $(id).css('display', 'none');
    }
  }

  private choose_image(_id) {
    let id = '#pic_' + _id;
    if ($(id).attr('src').slice(-7) == 'plu.gif') {
      $(id).attr('src', '/static/app/picture/tree/min.gif');
    } else {
      $(id).attr('src', '/static/app/picture/tree/plu.gif');
    }
  }
}




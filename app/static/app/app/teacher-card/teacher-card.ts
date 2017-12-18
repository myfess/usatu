import { Component, OnInit } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { UsatuRpcService }     from '../usatu-rpc/usatu-rpc.service';
import { UsatuConfigService } from '../usatu-config/usatu-config.service';
import { ChairsStructModule } from '../chairs-struct/chairs-struct.module';

import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {MdButtonModule, MdProgressSpinnerModule} from '@angular/material';
import { FormGroup, FormBuilder, Validators,
  FormControl, ReactiveFormsModule } from '@angular/forms';


@Component({
  moduleId: module.id,
  selector: 'teacher-card',
  templateUrl: 'teacher-card.html',
  styleUrls: [ 'teacher-card.css' ]
})
export class TeacherCardComponent implements OnInit {
  teacher_id:number = null;
  chair_id:number = 58; // По умолчанию неизвестная кафедра
  name:string = null;
  subject:string = null;
  information:string = null;
  photos:string = null;
  loading:boolean = false;
  show_form:boolean = true;

  error_msg:string = null;
  success_top_msg:string = null;
  success_bot_msg:string = null;

  chairs = [];

  teacherForm: FormGroup;

  constructor(
    private rpcService: UsatuRpcService,
    private _config: UsatuConfigService,
    private fb: FormBuilder) {
  }

  teacher_write() {
    let chair_id = $('input[name=teacher_chair]:checked').val();
    this.name = this.teacherForm.value.name;
    this.loading = true;
    let data = {
      'name': this.name,
      'id_chair': chair_id,
      'subject': this.subject,
      'information': this.information,
      'photos': this.photos
    };

    if (this.teacher_id !== null) {
      data['id'] = this.teacher_id;
    }

    this.error_msg = null;
    this.success_top_msg = null;
    this.success_bot_msg = null;

    this.rpcService.call('teacher_write', data)
      .then(res => this.handlerWrite(res));
  }

  teacher_read() {
    return this.rpcService.call('teacher_read',
      { 'id': this.teacher_id })
      .then(res => this.handlerRead(res));
  }

  private handlerRead(data) {
    this.name = data.name;
    this.subject = data.subject;
    this.information = data.information;
    this.photos = data.fotos;
    this.chair_id = data.id_chair;
  }

  private handlerWrite(data) {
    this.loading = false;

    if ('result' in data && data.result) {
      if (data.state == 'inserted') {
        this.show_form = false;
        this.success_top_msg = data.teacher_msg;
      } else {
        this.show_form = true;
        this.success_bot_msg = data.teacher_msg;
      }
    } else {
      this.error_msg = data.teacher_msg;
    }
  }


  ngOnInit(): void {
    let tid = this._config.config().teacher_id;

    if (typeof tid != 'undefined') {
      this.teacher_id = tid;
      this.teacher_read();
    }

    this.buildForm();
  }

  buildForm(): void {
    this.teacherForm = this.fb.group({
      'name': [this.name, [
          Validators.required,
          this.validateNameFactory()
        ]
      ],
    });

    this.teacherForm.valueChanges.subscribe(data => this.onValueChanged(data));
    this.onValueChanged(); // (re)set validation messages now
  }

  validateNameFactory() {
    let tpl = /^[ ]*[А-Яа-яёЁa-zA-Z]+[ ]+[А-Яа-яёЁa-zA-Z]+[ ]+[А-Яа-яёЁa-zA-Z]+[ ]*$/i;

    function _validate(c: FormControl) {
      let _valid = tpl.test(c.value);
      return _valid ? null : { validateName: { valid: false } };
    }

    return _validate;
  }

  onValueChanged(data?: any) {
    if (!this.teacherForm) { return; }
    const form = this.teacherForm;

    for (const field in this.formErrors) {
      // clear previous error message (if any)
      this.formErrors[field] = '';
      const control = form.get(field);

      if (control && control.dirty && !control.valid) {
        const messages = this.validationMessages[field];
        for (const key in control.errors) {
          if (this.formErrors[field].length == 0) {
            this.formErrors[field] += messages[key];
          }
        }
      }
    }
  }

  formErrors = {
    'name': ''
  };

  validationMessages = {
    'name': {
      'required': 'Необходимо ввести ФИО',
      'validateName': 'ФИО должно соответствовать формату: Фамилия Имя Отчество'
    }
  };
}

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    ChairsStructModule,
    NoopAnimationsModule, MdButtonModule, MdProgressSpinnerModule,
    ReactiveFormsModule,
    HttpModule
  ],
  declarations: [TeacherCardComponent],
  providers: [UsatuRpcService, UsatuConfigService],
  bootstrap: [TeacherCardComponent]
})
export class TeacherCardModule { }

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
  enableProdMode();
}

platformBrowserDynamic().bootstrapModule(TeacherCardModule);

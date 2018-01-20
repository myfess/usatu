import { Component, OnInit } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { enableProdMode } from '@angular/core';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { UsatuRpcService }     from '../usatu-rpc/usatu-rpc.service';
import { UsatuConfigService } from '../usatu-config/usatu-config.service';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {MdButtonModule, MdProgressSpinnerModule} from '@angular/material';
import { FormGroup, FormBuilder, Validators,
  FormControl, ReactiveFormsModule } from '@angular/forms';


@Component({
  moduleId: module.id,
  selector: 'restore-password',
  templateUrl: 'restore-password.html'
})
export class RestorePasswordComponent implements OnInit {
    show_form:boolean = true;
    email:string = null;
    regForm: FormGroup;
    loading:boolean = false;
    error_msg:string = null;
    success_top_msg:string = null;

    constructor(
        private rpcService: UsatuRpcService,
        private _config: UsatuConfigService,
        private fb: FormBuilder) {
    }

    restorePassword() {
        this.email = this.regForm.value.email;
        this.loading = true;
        let data = { 'email': this.email };
        this.error_msg = null;

        this.rpcService.call('restore_pass', data)
            .then(res => this.handlerRestorePassword(res));
    }

    private handlerRestorePassword(data) {
        this.loading = false;
        if ('result' in data && data.result) {
            this.show_form = false;
            this.success_top_msg =
                'На вашу почту отправлено письмо с ссылкой для восстановления пароля';
        } else {
            this.error_msg = data.msg;
        }
    }

    ngOnInit(): void {
        this.buildForm();
    }

    buildForm(): void {
        this.regForm = this.fb.group({
            'email': [this.email, [Validators.required]]
        });
        this.regForm.valueChanges.subscribe(data => this.onValueChanged(data));
        this.onValueChanged();
    }

    onValueChanged(data?: any) {
        if (!this.regForm) { return; }
        for (const field in this.formErrors) {
            this.formErrors[field] = '';
            let control = this.regForm.get(field);
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
        'email': ''
    };

    validationMessages = {
        'email': {
            'required': 'Необходимо ввести email',
            'email': 'Необходимо ввести настоящий email.'
        }
    };
}

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        NoopAnimationsModule, MdButtonModule, MdProgressSpinnerModule,
        ReactiveFormsModule,
        HttpModule
    ],
    declarations: [RestorePasswordComponent],
    providers: [UsatuRpcService, UsatuConfigService],
    bootstrap: [RestorePasswordComponent]
})
export class RestorePasswordModule { }

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
    enableProdMode();
}

platformBrowserDynamic().bootstrapModule(RestorePasswordModule);

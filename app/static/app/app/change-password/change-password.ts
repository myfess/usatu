import { Component, OnInit, ElementRef } from '@angular/core';
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
  selector: 'change-password',
  templateUrl: 'change-password.html'
})
export class ChangePasswordComponent implements OnInit {
    show_form:boolean = true;
    password:string = null;
    password2:string = null;
    secret:string = null;
    regForm: FormGroup;

    loading:boolean = false;
    error_msg:string = null;
    success_top_msg:string = null;

    constructor(
            private rpcService: UsatuRpcService,
            private _config: UsatuConfigService,
            private fb: FormBuilder,
            public elementRef: ElementRef) {

        let native = this.elementRef.nativeElement;
        this.secret = native.getAttribute('secret');
    }

    changePassword() {
        this.password = this.regForm.value.matchingPassword.password;

        this.loading = true;
        let data = {
            'secret': this.secret,
            'password': this.password
        };

        this.error_msg = null;

        this.rpcService.call('restore_change_pass', data)
            .then(res => this.handlerChangePassword(res));
    }

    private handlerChangePassword(data) {
        this.loading = false;
        if ('result' in data && data.result) {
            this.show_form = false;
            this.success_top_msg = 'Вы успешно сменили пароль.';
        } else {
            this.error_msg = data.msg;
        }
    }

    ngOnInit(): void {
        this.buildForm();
    }

    buildForm(): void {
        this.regForm = this.fb.group({
            'matchingPassword': this.fb.group({
                'password': ['', Validators.compose([
                    Validators.required,
                    Validators.minLength(4)
                ])],
                'password2': ['', []]
            }, { validator: this.areEqual })
        });

        this.regForm.valueChanges.subscribe(data => this.onValueChanged(data));
        this.onValueChanged();
    }

    areEqual(group: FormGroup) {
        let last = null;
        for (let name in group.controls) {
            var val = group.controls[name].value

            if (last === null) {
                last = val;
                continue;
            }

            if (last !== val) {
                return { 'match': { 'valid': false } };
            }
        }
        return null;
    }

    onValueChanged(data?: any) {
        if (!this.regForm) { return; }
        const form = this.regForm;

        for (const field in this.formErrors) {
            this.formErrors[field] = '';
            let control = null;
            if (field.includes('/')) {
                let fs = field.split('/');
                control = form.get(fs[0]).get(fs[1]);
            } else {
                control = form.get(field);
            }

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
        'matchingPassword/password': '',
        'matchingPassword/password2': '',
        'matchingPassword': ''
    };

    validationMessages = {
        'matchingPassword/password': {
            'required': 'Необходимо ввести пароль',
            'minlength': 'Пароль должен быть длинной минимум 4 символа'
        },

        'matchingPassword/password2': {
            'required': 'Необходимо подтвердить пароль2'
        },

        'matchingPassword': {
            'required': 'Необходимо подтвердить пароль3',
            'match': 'Пароль не совпадает'
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
    declarations: [ChangePasswordComponent],
    providers: [UsatuRpcService, UsatuConfigService],
    bootstrap: [ChangePasswordComponent]
})
export class ChangePasswordModule { }

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
    enableProdMode();
}

platformBrowserDynamic().bootstrapModule(ChangePasswordModule);

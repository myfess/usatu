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
  selector: 'registration',
  templateUrl: 'registration.html',
  styleUrls: [ 'registration.css' ]
})
export class RegistrationComponent implements OnInit {
    show_form:boolean = true;
    login:string = null;
    email:string = null;
    password:string = null;
    password2:string = null;
    regForm: FormGroup;

    loading:boolean = false;
    error_msg:string = null;
    success_top_msg:string = null;

    constructor(
        private rpcService: UsatuRpcService,
        private _config: UsatuConfigService,
        private fb: FormBuilder) {
    }

    registration() {
        this.login = this.regForm.value.login;
        this.password = this.regForm.value.matchingPassword.password;
        this.email = this.regForm.value.email;

        this.loading = true;
        let data = {
            'login': this.login,
            'password': this.password,
            'email': this.email
        };

        this.error_msg = null;

        this.rpcService.call('registraion', data)
            .then(res => this.handlerRegistraion(res));
    }

    private handlerRegistraion(data) {
        this.loading = false;
        if ('result' in data && data.result) {
            this.show_form = false;
            this.success_top_msg = 'Вы успешно зарегистрировались.';
        } else {
            this.error_msg = data.msg;
        }
    }

    ngOnInit(): void {
        this.buildForm();
    }

    buildForm(): void {
        this.regForm = this.fb.group({
            'login': [this.login, [
                Validators.required,
                this.validateRegexFactory(/^[a-zA-Z0-9-_]+$/i, 'validateLogin')
                ]
            ],
            'email': [this.email, [Validators.required]],

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

    validateRegexFactory(tpl: RegExp, message_name: String) {
        function _validate(c: FormControl) {
            if (tpl.test(c.value)) {
                return null;
            }
            return { [message_name]: { 'valid': false } };
        }
        return _validate;
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
            // clear previous error message (if any)
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
        'login': '',
        'email': '',
        'matchingPassword/password': '',
        'matchingPassword/password2': '',
        'matchingPassword': ''
    };

    validationMessages = {
        'login': {
            'required': 'Необходимо ввести логин',
            'validateLogin':
                'В логине можно использовать латинские буквы, цифры, подчеркивание или тире.'
        },
        'email': {
            'required': 'Необходимо ввести email',
            'email': 'Необходимо ввести настоящий email.'
        },
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
    declarations: [RegistrationComponent],
    providers: [UsatuRpcService, UsatuConfigService],
    bootstrap: [RegistrationComponent]
})
export class RegistrationModule { }

let conf = new UsatuConfigService();
if (conf.config().enableProdMode()) {
    enableProdMode();
}

platformBrowserDynamic().bootstrapModule(RegistrationModule);

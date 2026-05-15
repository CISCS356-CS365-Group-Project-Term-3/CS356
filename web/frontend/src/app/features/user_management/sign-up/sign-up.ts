import { Component, signal} from '@angular/core';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {merge} from 'rxjs';
import {MatRadioModule} from '@angular/material/radio';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';

/** @title Sign up page */
  @Component({
    selector: 'app-sign-up',
    imports: [
      MatFormFieldModule,
      MatInputModule,
      FormsModule,
      ReactiveFormsModule,
      MatRadioModule,
      MatButtonModule,
      MatIconModule
    ],
    templateUrl: 'sign-up.html',
    styleUrl: 'sign-up.scss',
    standalone: true
  })

export class SignUp {


// set up account form
  readonly accountForm = new FormGroup({
    username: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required),
    reenteredPassword: new FormControl('', Validators.required),
    accountType: new FormControl('', Validators.required)
  });

  usernameErrorMessage = signal('');
  passwordErrorMessage = signal('');
  reenteredPasswordErrorMessage = signal('');
  hide = signal(true);

  constructor() {
    merge(
      this.accountForm.valueChanges,
      this.accountForm.statusChanges
    )
      .pipe(takeUntilDestroyed())
      .subscribe(() => {
        this.updateUsernameErrorMessage();
        this.updatePasswordErrorMessage();
        this.updateReenteredPasswordErrorMessage();
      });
  }

  updateUsernameErrorMessage() {
    if (this.accountForm.get('username')?.hasError('required')) {
      this.usernameErrorMessage.set('You must enter a value');
    } else {
      this.usernameErrorMessage.set('');
    }
  }
  updatePasswordErrorMessage() {
    if (this.accountForm.get('password')?.hasError('required')) {
      this.passwordErrorMessage.set('You must enter a value');

    // check if password meets requirements
    } else {
      this.passwordErrorMessage.set('');
    }

    // add more checks
    // check Validators. options
  }

  clickPasswordEvent(event: MouseEvent) {
    this.hide.set(!this.hide());
    event.stopPropagation();
  }

  updateReenteredPasswordErrorMessage() {
    const reenteredPassword = this.accountForm.get('reenteredPassword');
    const password = this.accountForm.get('password');

    if (reenteredPassword?.hasError('required')) {
      this.reenteredPasswordErrorMessage.set('You must enter a value');
    } else if (reenteredPassword?.value && password?.value && reenteredPassword.value !== password?.value) {
      this.reenteredPasswordErrorMessage.set('Passwords do not match')
    }
    else {
      this.reenteredPasswordErrorMessage.set('');
    }
}

submitDetails(){

  const username = this.accountForm.get('username');
  const password = this.accountForm.get('password');
  const accountType = this.accountForm.get('accountType');

// submit details to API endpoint

}
}


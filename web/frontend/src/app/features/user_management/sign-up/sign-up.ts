import { Component, signal} from '@angular/core';
import { UserManagementService } from '../user-management-service';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators, AbstractControl, ValidationErrors} from '@angular/forms';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {merge} from 'rxjs';
import {MatRadioModule} from '@angular/material/radio';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { Router } from '@angular/router';

// custom validators
function specialCharacterValidator(control: AbstractControl): ValidationErrors | null {
  const value = control.value;
  if (!value) {
    return null;
  }
  const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(value);
  return hasSpecialChar ? null : { noSpecialCharacter: true };
}

function passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
  const password = control.parent?.get('password');
  const reenteredPassword = control.value;

  if (!password || !reenteredPassword) {
    return null;
  }

  return password.value === reenteredPassword ? null : { passwordMismatch: true };
}

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
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
      specialCharacterValidator
    ]),
    reenteredPassword: new FormControl('', [
      Validators.required,
      passwordMatchValidator
    ]),
    accountType: new FormControl('', Validators.required)
  });

  usernameErrorMessage = signal('');
  emailErrorMessage = signal('');
  passwordErrorMessage = signal('');
  reenteredPasswordErrorMessage = signal('');
  hide = signal(true);
  signUpErrorMessage: string = '';

  constructor(private userManagementService: UserManagementService, private router: Router) {
    merge(
      this.accountForm.valueChanges,
      this.accountForm.statusChanges
    )
      .pipe(takeUntilDestroyed())
      .subscribe(() => {
        this.updateUsernameErrorMessage();
        this.updateEmailErrorMessage();
        this.updatePasswordErrorMessage();
        this.updateReenteredPasswordErrorMessage();
      });

    // update reenteredPassword validation when password changes
    this.accountForm.get('password')?.valueChanges.pipe(takeUntilDestroyed()).subscribe(() => {
      this.accountForm.get('reenteredPassword')?.updateValueAndValidity({ emitEvent: false });
    });
  }

  updateUsernameErrorMessage() {
    if (this.accountForm.get('username')?.hasError('required')) {
      this.usernameErrorMessage.set('You must enter a value');
    } else {
      this.usernameErrorMessage.set('');
    }
  }

  updateEmailErrorMessage() {
    const emailControl = this.accountForm.get('email');
    if (emailControl?.hasError('required')) {
      this.emailErrorMessage.set('You must enter a value');
    } else if (emailControl?.hasError('email')) {
      this.emailErrorMessage.set('Not a valid email');
    } else {
      this.emailErrorMessage.set('');
    }
  }
  updatePasswordErrorMessage() {
    const passwordControl = this.accountForm.get('password');

    if (passwordControl?.hasError('required')) {
      this.passwordErrorMessage.set('You must enter a value');
    } else if (passwordControl?.hasError('minlength')) {
      this.passwordErrorMessage.set('Password must be at least 8 characters');
    } else if (passwordControl?.hasError('noSpecialCharacter')) {
      this.passwordErrorMessage.set('Password must contain at least one special character');
    } else {
      this.passwordErrorMessage.set('');
    }
  }

  clickPasswordEvent(event: MouseEvent) {
    this.hide.set(!this.hide());
    event.stopPropagation();
  }

  updateReenteredPasswordErrorMessage() {
    const reenteredPassword = this.accountForm.get('reenteredPassword');

    if (reenteredPassword?.hasError('required')) {
      this.reenteredPasswordErrorMessage.set('You must enter a value');
    } else if (reenteredPassword?.hasError('passwordMismatch')) {
      this.reenteredPasswordErrorMessage.set('Passwords do not match');
    } else {
      this.reenteredPasswordErrorMessage.set('');
    }
}

submitDetails(){

  const username = this.accountForm.get('username')?.value;
  const email = this.accountForm.get('email')?.value;
  const reenteredPassword = this.accountForm.get('reenteredPassword')?.value;
  const password = this.accountForm.get('password')?.value;
  const accountType = this.accountForm.get('accountType')?.value;

  if (!username || !email || !reenteredPassword || !password || !accountType) {
    return;
  }

  this.userManagementService.registerUser(username, password, reenteredPassword, email, accountType).subscribe({
      next: (data: unknown) => {
        if (!data || data === false) {
          console.error('Sign up failed');
          return;
        }
        this.userManagementService.loginUser(username, password).subscribe({
          next: (data: unknown) => {
            if (!data || data === false) {
              console.error('Login failed');
              return;
            }

            const token = (data as any).access_token;

            localStorage.setItem('access_token', token);
            console.log('Login successful');
            this.router.navigate(['/landing-page']);
          },
          error: (err) => {
            console.error('Login request failed', err);
            this.signUpErrorMessage = err?.error?.error?.message || 'Login failed';

          }
        });



    },
    error: (err) => {
      console.error('Failed to create an account', err);
      this.signUpErrorMessage = err?.error?.error?.message || 'Failed to create an account';

    }
  });

}
}


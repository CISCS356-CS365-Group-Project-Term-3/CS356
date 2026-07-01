import { Component, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
  AbstractControl,
  ValidationErrors,
} from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { merge } from 'rxjs';
import { MatRadioModule } from '@angular/material/radio';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { UserManagementService } from '../user-management-service';
import { MatSnackBar } from '@angular/material/snack-bar';

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

/** @title Password reset page */
@Component({
  selector: 'app-reset-password',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatRadioModule,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: 'reset-password.html',
  styleUrl: 'reset-password.scss',
  standalone: true,
})
export class ResetPassword {
  // set up reset password form
  readonly resetPasswordForm = new FormGroup({
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
      specialCharacterValidator,
    ]),
    reenteredPassword: new FormControl('', [Validators.required, passwordMatchValidator]),
  });

  passwordErrorMessage = signal('');
  reenteredPasswordErrorMessage = signal('');
  hide = signal(true);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
    private userManagementService: UserManagementService,
    private snackBar: MatSnackBar,
  ) {
    merge(this.resetPasswordForm.valueChanges, this.resetPasswordForm.statusChanges)
      .pipe(takeUntilDestroyed())
      .subscribe(() => {
        this.updatePasswordErrorMessage();
        this.updateReenteredPasswordErrorMessage();
      });

    // update reenteredPassword validation when password changes
    this.resetPasswordForm
      .get('password')
      ?.valueChanges.pipe(takeUntilDestroyed())
      .subscribe(() => {
        this.resetPasswordForm
          .get('reenteredPassword')
          ?.updateValueAndValidity({ emitEvent: false });
      });
  }

  updatePasswordErrorMessage() {
    const passwordControl = this.resetPasswordForm.get('password');

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
    const reenteredPassword = this.resetPasswordForm.get('reenteredPassword');

    if (reenteredPassword?.hasError('required')) {
      this.reenteredPasswordErrorMessage.set('You must enter a value');
    } else if (reenteredPassword?.hasError('passwordMismatch')) {
      this.reenteredPasswordErrorMessage.set('Passwords do not match');
    } else {
      this.reenteredPasswordErrorMessage.set('');
    }
  }

  savePassword() {
    if (this.resetPasswordForm.invalid) return;

    const token = this.route.snapshot.queryParamMap.get('token');
    const new_password = this.resetPasswordForm.get('password')?.value;

    if (!token) {
      console.error('Missing reset token');
      return;
    }
    if (!new_password) {
      console.error('Missing new password');
      return;
    }
    this.userManagementService.resetPasswordConfirm(token, new_password).subscribe({
      next: () => {
        this.snackBar.open('Password updated', 'Close');
        this.router.navigate(['/login']);
      },
      error: (err) => console.error('Reset failed', err),
    });
  }
}

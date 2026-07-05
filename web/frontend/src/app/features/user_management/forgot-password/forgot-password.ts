import { Component, signal, inject } from '@angular/core';
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
import { HttpClient } from '@angular/common/http';
import { UserManagementService } from '../user-management-service';
import { MatSnackBar } from '@angular/material/snack-bar';

/** @title Forgot password page */
@Component({
  selector: 'app-forgot-password',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatRadioModule,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: 'forgot-password.html',
  styleUrl: 'forgot-password.scss',
  standalone: true,
})
export class ForgotPassword {
  private http = inject(HttpClient);

  readonly emailForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
  });

  emailErrorMessage = signal('');
  successMessage = signal('');

  constructor(
    private userManagementService: UserManagementService,
    private snackBar: MatSnackBar,
  ) {
    merge(this.emailForm.valueChanges, this.emailForm.statusChanges)
      .pipe(takeUntilDestroyed())
      .subscribe(() => {
        this.updateEmailErrorMessage();
      });
  }

  updateEmailErrorMessage() {
    const emailControl = this.emailForm.get('email');
    if (emailControl?.hasError('required')) {
      this.emailErrorMessage.set('You must enter a value');
    } else if (emailControl?.hasError('email')) {
      this.emailErrorMessage.set('Not a valid email');
    } else {
      this.emailErrorMessage.set('');
    }
  }

  sendEmail() {
    const email = this.emailForm.get('email')?.value;
    if (!email) return;
    this.userManagementService.resetPassword(email).subscribe({
      next: () =>
        this.snackBar.open(
          'If an account exists, a reset link has been sent to your email.',
          'Close',
        ),
      error: () =>
        this.snackBar.open(
          'If an account exists, a reset link has been sent to your email.',
          'Close',
        ),
    });
  }
}

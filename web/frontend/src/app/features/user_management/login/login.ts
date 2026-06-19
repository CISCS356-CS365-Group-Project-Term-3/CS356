import { Component, signal} from '@angular/core';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {merge} from 'rxjs';
import {MatRadioModule} from '@angular/material/radio';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {RouterLink, Router} from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../services/auth.service';

/** @title Login page */
@Component({
  selector: 'app-login',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatRadioModule,
    MatButtonModule,
    MatIconModule,
    RouterLink
  ],
  templateUrl: 'login.html',
  styleUrl: 'login.scss',
  standalone: true
})

export class Login {


// set up login form
  readonly loginForm = new FormGroup({
    username: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required),
  });

  usernameErrorMessage = signal('');
  passwordErrorMessage = signal('');
  hide = signal(true);

  constructor(private http: HttpClient, private router: Router, private authService: AuthService) {
    merge(
      this.loginForm.valueChanges,
      this.loginForm.statusChanges
    )
      .pipe(takeUntilDestroyed())
      .subscribe(() => {
        this.updateUsernameErrorMessage();
        this.updatePasswordErrorMessage();
      });
  }

  updateUsernameErrorMessage() {
    if (this.loginForm.get('username')?.hasError('required')) {
      this.usernameErrorMessage.set('You must enter a value');
    } else {
      this.usernameErrorMessage.set('');
    }
  }
  updatePasswordErrorMessage() {
    if (this.loginForm.get('password')?.hasError('required')) {
      this.passwordErrorMessage.set('You must enter a value');
    } else {
      this.passwordErrorMessage.set('');
    }
  }

  clickPasswordEvent(event: MouseEvent) {
    this.hide.set(!this.hide());
    event.stopPropagation();
  }


  submitDetails(){

    const username = this.loginForm.get('username')?.value;
    const password = this.loginForm.get('password')?.value;

    if (!username || !password) return;

    // call backend login endpoint
    this.http.post<{ access_token: string }>('http://localhost:8000/auth/login', { user_name: username, password })
      .subscribe({
        next: (res) => {
          if (res && res.access_token) {
            this.authService.setToken(res.access_token);
            this.router.navigate(['/experiments']);
          }
        },
        error: (err) => {
          console.error('Login failed', err);
        }
      });
  }
}

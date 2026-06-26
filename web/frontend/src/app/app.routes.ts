import { Routes } from '@angular/router';
import { Login } from './features/user_management/login/login';
import { SignUp } from './features/user_management/sign-up/sign-up';
import { Home } from './features/user_management/home/home';
import { LandingPage } from './features/user_management/landing-page/landing-page';
import { ResetPassword } from './features/user_management/reset-password/reset-password';
import { ForgotPassword} from './features/user_management/forgot-password/forgot-password';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'sign-up', component: SignUp },
  { path: 'home', component: Home },
  { path: 'landing-page', component: LandingPage},
  { path: 'reset-password', component: ResetPassword},
  { path: 'forgot-password', component: ForgotPassword},
  { path: '', component: Home }
];

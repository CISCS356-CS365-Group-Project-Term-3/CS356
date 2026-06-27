import { Routes } from '@angular/router';
import { Login } from './features/user_management/login/login';
import { Dashboard } from './features/experiments/dashboard/dashboard';
import { NewExperiment } from './features/experiments/new-experiment/new-experiment';
import { AuthGuard } from './guards/auth.guard';
import { SignUp } from './features/user_management/sign-up/sign-up';
import { Home } from './features/user_management/home/home';
import { LandingPage } from './features/user_management/landing-page/landing-page';
import { ResetPassword } from './features/user_management/reset-password/reset-password';
import { ForgotPassword } from './features/user_management/forgot-password/forgot-password';
import { Profile } from './features/user_management/profile/profile';

export const routes: Routes = [
  { path: 'experiments', component: Dashboard, canActivate: [AuthGuard] },
  { path: 'experiments/new', component: NewExperiment, canActivate: [AuthGuard] },
  { path: 'profile', component: Profile, canActivate: [AuthGuard] },
  { path: 'login', component: Login },
  { path: 'sign-up', component: SignUp },
  { path: 'forgot-password', component: ForgotPassword },
  { path: 'reset-password', component: ResetPassword },
  { path: 'home', component: Home },
  { path: 'landing-page', component: LandingPage },
  { path: '', component: Home },
];

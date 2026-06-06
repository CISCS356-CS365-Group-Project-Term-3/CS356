import { Routes } from '@angular/router';
import { Login } from './features/user_management/login/login';
import { Dashboard } from './features/experiments/dashboard/dashboard';
import { NewExperiment } from './features/experiments/new-experiment/new-experiment';
import { SignUp } from './features/user_management/sign-up/sign-up';
import { Home } from './features/user_management/home/home';
import { LandingPage } from './features/user_management/landing-page/landing-page';

export const routes: Routes = [
  { path: 'experiments', component: Dashboard },
  { path: 'experiments/new', component: NewExperiment },
  { path: 'login', component: Login },
  { path: 'sign-up', component: SignUp },
  { path: 'home', component: Home },
  { path: 'landing-page', component: LandingPage },
  { path: '', component: Home },
];

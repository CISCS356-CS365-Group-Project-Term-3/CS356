import { Routes } from '@angular/router';
import { Login } from './features/user_management/login/login';
import { SignUp } from './features/user_management/sign-up/sign-up';
import { Home } from './features/user_management/home/home';


export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'sign-up', component: SignUp },
  { path: 'home', component: Home },
];

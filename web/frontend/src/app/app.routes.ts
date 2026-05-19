import { Routes } from '@angular/router';
import {Login} from './features/user_management/login/login';
import { SignUp} from './features/user_management/sign-up/sign-up';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'sign-up', component: SignUp }];

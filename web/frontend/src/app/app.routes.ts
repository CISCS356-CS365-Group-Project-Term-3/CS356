import { Routes } from '@angular/router';
import { Login } from './features/user_management/login/login';
import { Home} from './features/user_management/home/home';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'home', component: Home },
];

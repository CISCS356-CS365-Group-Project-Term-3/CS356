import { Routes } from '@angular/router';
import { NewExperiment } from './features/experiments/new-experiment/new-experiment';
import { SignUp} from './features/user_management/sign-up/sign-up';

export const routes: Routes = [
  { path: 'experiments/new', component: NewExperiment },
  { path: 'sign-up', component: SignUp }
];

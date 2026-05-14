import { Routes } from '@angular/router';
import { Dashboard } from './features/experiments/dashboard/dashboard';
import { NewExperiment } from './features/experiments/new-experiment/new-experiment';

export const routes: Routes = [
  { path: 'experiments', component: Dashboard },
  { path: 'experiments/new', component: NewExperiment },
];

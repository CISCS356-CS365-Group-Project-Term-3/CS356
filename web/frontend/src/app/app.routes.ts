import { Routes } from '@angular/router';
import { NewExperiment } from './features/experiments/new-experiment/new-experiment';

export const routes: Routes = [
  { path: 'experiments/new', component: NewExperiment },
];

import { Routes } from '@angular/router';
import { Login } from './features/user_management/login/login';
import { Dashboard } from './features/experiments/dashboard/dashboard';
import { NewExperiment } from './features/experiments/new-experiment/new-experiment';
import { SignUp } from './features/user_management/sign-up/sign-up';
import { Home } from './features/user_management/home/home';
import { LandingPage } from './features/user_management/landing-page/landing-page';
import { ResetPassword } from './features/user_management/reset-password/reset-password';
import { ForgotPassword } from './features/user_management/forgot-password/forgot-password';
import { InfrastructurePortalComponent } from './features/infrastructure-portal/infrastructure-portal';
import { InfrastructureDashboardComponent } from './features/infrastructure-portal/dashboard/infrastructure-dashboard';
import { InfrastructureEncodersComponent } from './features/infrastructure-portal/encoders/infrastructure-encoders';
import { InfrastructureNetworkProfilesComponent } from './features/infrastructure-portal/network-profiles/infrastructure-network-profiles';
import { InfrastructureCodecsComponent } from './features/infrastructure-portal/codecs/infrastructure-codecs';
import { Profile } from './features/user_management/profile/profile';
import { InfrastructureDatasetsComponent} from './features/infrastructure-portal/datasets/infrastruture-datasets';
import { ResultsPage } from './features/results/results';

export const routes: Routes = [
  { path: 'experiments', component: Dashboard },
  { path: 'experiments/new', component: NewExperiment },
  { path: 'login', component: Login },
  { path: 'sign-up', component: SignUp },
  { path: 'home', component: Home },
  { path: 'landing-page', component: LandingPage},
  { path: 'reset-password', component: ResetPassword},
  { path: 'forgot-password', component: ForgotPassword},
  { path: 'profile', component: Profile },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'infrastructurePortal', component: InfrastructurePortalComponent,
    children: [
      { path: '', component: InfrastructureDashboardComponent },
      { path: 'encoders', component: InfrastructureEncodersComponent },
      { path: 'codecs', component: InfrastructureCodecsComponent},
      { path: 'network-profiles', component: InfrastructureNetworkProfilesComponent },
      { path: 'infrastructure-datasets',component:InfrastructureDatasetsComponent},
    ],
  },
  { path: 'results', component: ResultsPage },
  { path: '', component: Home },
];

import { Routes } from '@angular/router';
import { Login } from './features/user_management/login/login';
import { Dashboard } from './features/experiments/dashboard/dashboard';
import { NewExperiment } from './features/experiments/new-experiment/new-experiment';
import { SignUp } from './features/user_management/sign-up/sign-up';
import { Home } from './features/user_management/home/home';
import { LandingPage } from './features/user_management/landing-page/landing-page';
import { ResetPassword } from './features/user_management/reset-password/reset-password';
import { ForgotPassword} from './features/user_management/forgot-password/forgot-password';
import { Profile } from './features/user_management/profile/profile';

<<<<<<< HEAD
import { InfrastructurePortalComponent } from './features/infrastructure-portal/infrastructure-portal';
import { InfrastructureDashboardComponent } from './features/infrastructure-portal/dashboard/infrastructure-dashboard';
import { InfrastructureEncodersComponent } from './features/infrastructure-portal/encoders/infrastructure-encoders';
import { InfrastructureNetworkProfilesComponent } from './features/infrastructure-portal/network-profiles/infrastructure-network-profiles';

export const routes: Routes = [
  {
    path: 'infrastructurePortal',
    component: InfrastructurePortalComponent,
    children: [
      { path: '', component: InfrastructureDashboardComponent },
      { path: 'encoders', component: InfrastructureEncodersComponent },
      { path: 'network-profiles', component: InfrastructureNetworkProfilesComponent },
    ],
  },
  { path: '', redirectTo: 'infrastructurePortal', pathMatch: 'full' },
=======
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
  { path: '', component: Home }
<<<<<<< HEAD
>>>>>>> origin/G-experiment-management-portal
=======
>>>>>>> origin/frontend
];

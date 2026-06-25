import { Routes } from '@angular/router';

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
];

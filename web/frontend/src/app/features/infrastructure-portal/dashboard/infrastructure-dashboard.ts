import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { OnInit } from '@angular/core';
import { UiOptionsService } from '../services/ui-options.service';
@Component({
  selector: 'app-infrastructure-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, MatButtonModule, MatCardModule, MatIconModule],
  templateUrl: './infrastructure-dashboard.html',
  styleUrls: ['./infrastructure-dashboard.scss'],
})

export class InfrastructureDashboardComponent implements OnInit {

  constructor(
    private uiOptionsService: UiOptionsService
  ) {}

  ngOnInit(): void {

    this.uiOptionsService.getUiOptions()
      .subscribe(data => {

        console.log('Backend Data:', data);

      });
  }
}

// export class InfrastructureDashboardComponent {
//   summaryCards = [
//     {
//       title: 'Encoders',
//       value: '12',
//       subtitle: 'Available for experiments',
//       icon: 'memory',
//       link: '/infrastructurePortal/encoders',
//     },
//     {
//       title: 'Running Experiments',
//       value: '3',
//       subtitle: 'Currently processing',
//       icon: 'play_circle',
//       link: '/infrastructurePortal/running-experiments',
//     },
//     {
//       title: 'Datasets',
//       value: '8',
//       subtitle: 'Video clips loaded',
//       icon: 'movie',
//       link: '/infrastructurePortal/datasets',
//     },
//     {
//       title: 'Network Profiles',
//       value: '6',
//       subtitle: 'Simulated conditions',
//       icon: 'dns',
//       link: '/infrastructurePortal/network-profiles',
//     },
//   ];
//
//   quickLinks = [
//     {
//       title: 'Encoders',
//       text: 'View and manage codec options.',
//       icon: 'memory',
//       link: '/infrastructurePortal/encoders',
//     },
//     {
//       title: 'Network Profiles',
//       text: 'Edit packet loss, delay and jitter presets.',
//       icon: 'dns',
//       link: '/infrastructurePortal/network-profiles',
//     },
//     {
//       title: 'Datasets',
//       text: 'Manage the available video clips.',
//       icon: 'movie',
//       link: '/infrastructurePortal/datasets',
//     },
//     {
//       title: 'Running Experiments',
//       text: 'See jobs that are processing right now.',
//       icon: 'play_circle',
//       link: '/infrastructurePortal/running-experiments',
//     },
//   ];
// }

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
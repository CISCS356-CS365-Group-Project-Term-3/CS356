import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { OnInit } from '@angular/core';
import { UiOptionsService } from '../services/ui-options.service';
import { UserManagementService } from '../../user_management/user-management-service';
@Component({
  selector: 'app-infrastructure-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, MatButtonModule, MatCardModule, MatIconModule],
  templateUrl: './infrastructure-dashboard.html',
  styleUrls: ['./infrastructure-dashboard.scss'],
})

export class InfrastructureDashboardComponent implements OnInit {
  isAdmin = false;

  constructor(
    private uiOptionsService: UiOptionsService,
    private userService: UserManagementService
  ) {}

  ngOnInit(): void {
    this.loadUserRole();

    this.uiOptionsService.getUiOptions()
      .subscribe(data => {
        console.log('Backend Data:', data);
      });
  }

  private loadUserRole(): void {
    try {
      this.userService.getUserInfo().subscribe({
        next: (user: any) => {
          this.isAdmin = user.user_role === 'admin';
        },
        error: () => {
          this.isAdmin = false;
        }
      });
    } catch {
      this.isAdmin = false;
    }
  }
}
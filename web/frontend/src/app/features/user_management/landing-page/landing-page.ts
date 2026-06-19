import { Component, ChangeDetectionStrategy } from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {NgOptimizedImage} from '@angular/common';
import {Router, RouterLink} from '@angular/router';
import { ConfirmLogoutDialog} from '../confirm-logout-dialog/confirm-logout-dialog';
import {MatDialog} from '@angular/material/dialog';
import { UserManagementService } from '../user-management-service';

/** @title Landing page */
@Component({
  selector: 'app-landing-page',
  imports: [MatCardModule, MatButtonModule, NgOptimizedImage, RouterLink],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: 'landing-page.html',
  styleUrl: 'landing-page.scss',
  standalone: true
})

export class LandingPage {
  token: string | null = null;
  username: string = '';

  constructor(
    private dialog: MatDialog,
    private router: Router,
    private userManagementService: UserManagementService,
  ) {}

  ngOnInit() {
     this.token = localStorage.getItem('access_token');
     this.getUserName()
  }

  getUserName() {
    this.userManagementService.getUserInfo().subscribe({
      next: (data: any) => {
        this.username = data.username;
      },
      error: (err) => {
        console.error(err);
      }
    });
  }

  openConfirm() {
    const ref = this.dialog.open(ConfirmLogoutDialog);

    ref.afterClosed().subscribe(result => {
      if (result === true) {
        this.onConfirmed();
      }
    });
  }

  onConfirmed() {

    // end user session
    // take back to home page
    this.router.navigate(['/home']);
  }
}

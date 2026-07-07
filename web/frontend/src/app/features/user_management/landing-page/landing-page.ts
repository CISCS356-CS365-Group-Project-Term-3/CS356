import { Component, ChangeDetectionStrategy } from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {Router, RouterLink} from '@angular/router';
import { ConfirmLogoutDialog} from '../confirm-logout-dialog/confirm-logout-dialog';
import {MatDialog} from '@angular/material/dialog';
import { UserManagementService } from '../user-management-service';
import { OnInit } from '@angular/core';
import { ChangeDetectorRef } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';



/** @title Landing page */
@Component({
  selector: 'app-landing-page',
  imports: [MatCardModule, MatButtonModule, RouterLink],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: 'landing-page.html',
  styleUrls: ['landing-page.scss'],
  standalone: true
})

export class LandingPage implements OnInit {
  username: string = '';

  constructor(
    private dialog: MatDialog,
    private router: Router,
    private userManagementService: UserManagementService,
    private cdr: ChangeDetectorRef,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
     this.getUserName()
  }

  getUserName() {
    this.userManagementService.getUserInfo().subscribe({
      next: (data: any) => {
        this.username = data.user_name;
        this.cdr.markForCheck();
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
    localStorage.clear()

    this.snackBar.open(
      "You've been logged out successfully",
      'Close', { duration: 3500});

    // take back to home page
    this.router.navigate(['/home']);
  }
}

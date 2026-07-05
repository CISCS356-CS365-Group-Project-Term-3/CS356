import { Component } from '@angular/core';
import {Router, RouterLink} from '@angular/router';
import { ConfirmLogoutDialog} from '../../features/user_management/confirm-logout-dialog/confirm-logout-dialog';
import {MatDialog} from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import { MatSnackBar } from '@angular/material/snack-bar';


@Component({
  selector: 'app-navbar',
  imports: [MatButtonModule, RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss',
  standalone: true
})
export class Navbar {
  constructor(
    private dialog: MatDialog,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}
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

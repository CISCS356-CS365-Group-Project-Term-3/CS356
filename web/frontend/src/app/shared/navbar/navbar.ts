import { Component } from '@angular/core';
import {Router, RouterLink} from '@angular/router';
import { ConfirmLogoutDialog} from '../../features/user_management/confirm-logout-dialog/confirm-logout-dialog';
import {MatDialog} from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';

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
    private router: Router
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
    // take back to home page
    this.router.navigate(['/home']);
  }
}

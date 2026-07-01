import { Component, ChangeDetectionStrategy } from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {Router, RouterLink} from '@angular/router';
import { ConfirmLogoutDialog} from '../confirm-logout-dialog/confirm-logout-dialog';
import {MatDialog} from '@angular/material/dialog';

/** @title Landing page */
@Component({
  selector: 'app-landing-page',
  imports: [MatCardModule, MatButtonModule, RouterLink],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: 'landing-page.html',
  styleUrls: ['landing-page.scss'],
  standalone: true
})

export class LandingPage {

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

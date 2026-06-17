import { Component } from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import { MatDialogActions, MatDialogContent, MatDialogRef, MatDialogTitle, MatDialogModule} from '@angular/material/dialog';

/** @title Confirm Logout Dialog */
@Component({
  selector: 'app-confirm-logout-dialog',
  imports: [
    MatButtonModule,
    MatDialogModule,
    MatDialogContent,
    MatDialogActions,
    MatDialogTitle
  ],
  templateUrl: './confirm-logout-dialog.html',
  styleUrl: './confirm-logout-dialog.scss',
  standalone: true
})
export class ConfirmLogoutDialog {

  constructor(private dialogRef: MatDialogRef<ConfirmLogoutDialog>) {}

  onCancel() {
    this.dialogRef.close(false);
  }

  onConfirm() {
    this.dialogRef.close(true);
  }
}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-add-network-profile-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './add-network-profile-dialog.html',
  styleUrls: ['./add-network-profile-dialog.scss']
})
export class AddNetworkProfileDialogComponent {

  name = '';

  lower_bound = 0;

  upper_bound = 0;

  unit = '';

  constructor(
    private dialogRef: MatDialogRef<AddNetworkProfileDialogComponent>
  ) {}

  save(): void {

    this.dialogRef.close({

      name: this.name.trim(),

      lower_bound: this.lower_bound,

      upper_bound: this.upper_bound,

      unit: this.unit.trim()

    });

  }

  cancel(): void {

    this.dialogRef.close();

  }

}

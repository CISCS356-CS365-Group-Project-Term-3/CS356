import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-add-codec-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './add-codec-dialog.component.html',
  styleUrls: ['./add-codec-dialog.component.scss']
})
export class AddCodecDialogComponent {

  name = '';
  version = ''
  constructor(
    private dialogRef: MatDialogRef<AddCodecDialogComponent>
  ) {}

  save(): void {

    this.dialogRef.close({

      name: this.name.trim(),
      version: '1.0',
      active: 0
    });
  }

  cancel(): void {

    this.dialogRef.close();
  }
}

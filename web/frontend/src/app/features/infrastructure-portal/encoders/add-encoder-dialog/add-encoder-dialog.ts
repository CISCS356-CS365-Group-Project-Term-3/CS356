import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-add-encoder-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './add-encoder-dialog.html',
  styleUrls: ['./add-encoder-dialog.scss']
})
export class AddEncoderDialogComponent {

  name = '';

  description = '';

  constructor(
    private dialogRef: MatDialogRef<AddEncoderDialogComponent>
  ) {}

  save(): void {
    this.dialogRef.close({
      name: this.name.trim(),
      description: this.description.trim() || 'No description',
      active: 0
    });
  }

  cancel(): void {
    this.dialogRef.close();
  }

}

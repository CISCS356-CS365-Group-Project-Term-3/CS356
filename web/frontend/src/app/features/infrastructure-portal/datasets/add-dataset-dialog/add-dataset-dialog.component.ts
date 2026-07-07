import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-add-dataset-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './add-dataset-dialog.component.html',
  styleUrls: ['./add-dataset-dialog.component.scss']
})
export class AddDatasetDialogComponent {

  name = '';
  description = '';
  filename = '';
  width = 352;
  height = 288;
  fps = 30;
  depth = 10;
  quality = '20';
  gamut = 'Gamut 1';

  constructor(
    private dialogRef: MatDialogRef<AddDatasetDialogComponent>
  ) {}

  save(): void {
    this.dialogRef.close({
      name: this.name.trim(),
      description: this.description.trim() || 'No description',
      active: 1,
      supported: 1,
      video_file: {
        name: this.filename.trim() || `${this.name.trim()}_file`,
        filepath: this.filename.trim() || `${this.name.trim()}.y4m`,
        spacial: [this.width, this.height],
        temporal: this.fps,
        depth: this.depth,
        quality: this.quality,
        gamut: this.gamut
      }
    });
  }

  cancel(): void {
    this.dialogRef.close();
  }

  isFormValid(): boolean {
    return (
      this.name.trim().length > 0 &&
      this.description.trim().length > 0 &&
      this.filename.trim().length > 0 &&
      this.width > 0 &&
      this.height > 0 &&
      this.fps > 0 &&
      this.depth > 0 &&
      this.quality.trim().length > 0 &&
      this.gamut.trim().length > 0
    );
  }
}

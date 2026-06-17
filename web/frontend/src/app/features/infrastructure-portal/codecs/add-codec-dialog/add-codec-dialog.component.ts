import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import {
  MatDialogRef,
  MatDialogModule
} from '@angular/material/dialog';

import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-add-codec-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  templateUrl: './add-codec-dialog.component.html'
})
export class AddCodecDialogComponent {
  codecForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<AddCodecDialogComponent>
  ) {
    this.codecForm = this.fb.group({
      codec: ['', Validators.required],
      version: [''],
      status: ['']
    });
  }

  save(): void {
    if (this.codecForm.valid) {
      this.dialogRef.close(this.codecForm.value);
    }
  }

  cancel(): void {
    this.dialogRef.close();
  }
}

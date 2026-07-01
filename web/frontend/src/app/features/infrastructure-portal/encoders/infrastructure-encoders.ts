import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { AgGridAngular } from 'ag-grid-angular';

import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridReadyEvent,
  ModuleRegistry,
  RowClassParams,
  SelectionChangedEvent,
} from 'ag-grid-community';

import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSnackBarModule } from '@angular/material/snack-bar';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';

import { UiOptionsService } from '../services/ui-options.service';
import { AddEncoderDialogComponent } from './add-encoder-dialog/add-encoder-dialog';

ModuleRegistry.registerModules([AllCommunityModule]);

interface EncoderRow {
  id: number;
  name: string;
  description: string | null;
  active: number;
}

@Component({
  selector: 'app-infrastructure-encoders',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    AgGridAngular,
    MatCardModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatSnackBarModule,
  ],
  templateUrl: './infrastructure-encoders.html',
  styleUrls: ['./infrastructure-encoders.scss'],
})
export class InfrastructureEncodersComponent implements OnInit {

  private gridApi?: GridApi<EncoderRow>;

  rowData: EncoderRow[] = [];

  selectedEncoder?: EncoderRow;

  rowClassRules = {
    'row-active': (params: RowClassParams<EncoderRow>) =>
      params.data?.active === 1,

    'row-inactive': (params: RowClassParams<EncoderRow>) =>
      params.data?.active === 0,
  };

  columnDefs: ColDef<EncoderRow>[] = [

    {
      field: 'id',
      headerName: 'ID',
      width: 90
    },

    {
      field: 'name',
      headerName: 'Encoder Type',
      flex: 1,
      minWidth: 260
    },

    {
      field: 'description',
      headerName: 'Description',
      flex: 2,
      valueFormatter: params =>
        params.value ?? 'No description'
    },

    {
      field: 'active',
      headerName: 'Status',
      width: 170,

      valueFormatter: params =>
        params.value === 1
          ? 'Active'
          : 'Inactive',

      cellClass: params =>
        params.value === 1
          ? 'status-active'
          : 'status-inactive'
    }

  ];

  defaultColDef: ColDef = {
    sortable: true,
    filter: true,
    resizable: true
  };

  constructor(
    private uiOptionsService: UiOptionsService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadEncoderTypes();
  }

  loadEncoderTypes(): void {

    this.uiOptionsService.getUiOptions().subscribe({

      next: (data) => {

        console.log('Encoder Types:', data.encoder_types);

        this.rowData = (data.encoder_types ?? []).map((encoder: any) => ({
          id: encoder.id,
          name: encoder.name,
          description: encoder.description,
          active: encoder.active
        }));
      },

      error: (error) => {

        console.error(error);

        this.snackBar.open(
          'Failed to load encoder types.',
          'Close',
          {
            duration: 3000
          }
        );

      }

    });

  }

  onGridReady(
    params: GridReadyEvent<EncoderRow>
  ): void {

    this.gridApi = params.api;

    params.api.sizeColumnsToFit();

  }

  addEncoder(): void {

    const dialogRef = this.dialog.open(
      AddEncoderDialogComponent,
      {
        width: '520px'
      }
    );

    dialogRef.afterClosed().subscribe(result => {

      if (!result) {
        return;
      }

      // Check for duplicate encoder type names
      const duplicate = this.rowData.some(
        encoder =>
          encoder.name.trim().toLowerCase() ===
          result.name.trim().toLowerCase()
      );

      if (duplicate) {

        this.snackBar.open(
          'An encoder type with this name already exists.',
          'Close',
          {
            duration: 3500
          }
        );

        return;

      }

      const payload = {

        name: result.name.trim(),

        description: result.description.trim(),

        active: 0

      };

      this.uiOptionsService
        .addEncoderType(payload)
        .subscribe({

          next: () => {

            this.snackBar.open(
              'Encoder type added.',
              'Close',
              {
                duration: 3000
              }
            );

            this.loadEncoderTypes();

          },

          error: () => {

            this.snackBar.open(
              'Failed to add encoder type.',
              'Close',
              {
                duration: 3000
              }
            );

          }

        });

    });

  }

  onSelectionChanged(
    event: SelectionChangedEvent<EncoderRow>
  ): void {

    const rows = event.api.getSelectedRows();

    this.selectedEncoder =
      rows.length > 0
        ? rows[0]
        : undefined;

  }

  enableSelected(): void {

    if (!this.selectedEncoder) {
      return;
    }

    // Only Standard Encoder can be enabled
    if (this.selectedEncoder.name !== 'Standard Encoder') {

      this.snackBar.open(
        'Encoder not supported by Experiments Engine',
        'Close',
        {
          duration: 3500
        }
      );

      return;
    }

    this.uiOptionsService
      .toggleEncoderType(
        this.selectedEncoder.id,
        1
      )
      .subscribe({

        next: () => {

          this.loadEncoderTypes();

          this.snackBar.open(
            'Encoder activated.',
            'Close',
            {
              duration: 3000
            }
          );

        },

        error: () => {

          this.snackBar.open(
            'Unable to activate encoder.',
            'Close',
            {
              duration: 3000
            }
          );

        }

      });

  }

  disableSelected(): void {

    if (!this.selectedEncoder) {
      return;
    }

    // Prevent disabling the Standard Encoder because it's the only one
    // supported by the experiment engine.
    if (this.selectedEncoder.name === 'Standard Encoder') {

      this.snackBar.open(
        "Unable to deactivate Engine supported Standard Encoder",
        'Close',
        {
          duration: 5000
        }
      );

      return;

    }

    this.uiOptionsService
      .toggleEncoderType(
        this.selectedEncoder.id,
        0
      )
      .subscribe({

        next: () => {

          this.loadEncoderTypes();

          this.snackBar.open(
            'Encoder deactivated.',
            'Close',
            {
              duration: 3000
            }
          );

        },

        error: () => {

          this.snackBar.open(
            'Unable to deactivate encoder.',
            'Close',
            {
              duration: 3000
            }
          );

        }

      });

  }

}

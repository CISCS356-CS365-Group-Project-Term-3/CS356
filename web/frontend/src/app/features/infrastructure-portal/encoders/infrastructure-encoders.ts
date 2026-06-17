import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { AgGridAngular } from 'ag-grid-angular';
import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridReadyEvent,
  ModuleRegistry,
  SelectionChangedEvent,
} from 'ag-grid-community';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

import { UiOptionsService } from '../services/ui-options.service';
import { AddEncoderDialogComponent } from './add-encoder-dialog/add-encoder-dialog';

ModuleRegistry.registerModules([AllCommunityModule]);

interface EncoderRow {
  id: number;
  name: string;
  description: string | null;
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
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatDialogModule,
    MatSnackBarModule,
  ],
  templateUrl: './infrastructure-encoders.html',
  styleUrls: ['./infrastructure-encoders.scss'],
})
export class InfrastructureEncodersComponent implements OnInit {
  private gridApi?: GridApi<EncoderRow>;

  searchText = '';

  rowData: EncoderRow[] = [];

  selectedEncoder?: EncoderRow;

  columnDefs: ColDef<EncoderRow>[] = [
    {
      field: 'id',
      headerName: 'ID',
      width: 100,
    },
    {
      field: 'name',
      headerName: 'Encoder Type',
      flex: 1,
      minWidth: 200,
    },
    {
      field: 'description',
      headerName: 'Description',
      flex: 2,
      minWidth: 250,
      valueFormatter: (params) => params.value ?? 'No description',
    },
  ];

  defaultColDef: ColDef = {
    sortable: true,
    filter: true,
    resizable: true,
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

        this.rowData = [...(data.encoder_types ?? [])];

        if (this.gridApi) {
          this.gridApi.refreshCells();
        }
      },
      error: (error) => {
        console.error('Failed to load encoder types:', error);
      },
    });
  }

  onGridReady(params: GridReadyEvent<EncoderRow>): void {
    this.gridApi = params.api;
    params.api.sizeColumnsToFit();
  }

  onSearch(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.searchText = value;

    if (this.gridApi) {
      // Uncomment if using AG Grid quick filter
      // this.gridApi.setGridOption('quickFilterText', value);
    }
  }

  addEncoder(): void {
    const dialogRef = this.dialog.open(
      AddEncoderDialogComponent,
      {
        width: '500px',
      }
    );

    dialogRef.afterClosed().subscribe((result) => {
      if (!result) {
        return;
      }

      this.uiOptionsService
        .addEncoderType(result)
        .subscribe({
          next: () => {
            this.loadEncoderTypes();

            this.snackBar.open(
              'Encoder type added successfully',
              'Close',
              {
                duration: 3000,
              }
            );
          },

          error: (err) => {
            console.error(err);

            this.snackBar.open(
              'Failed to add encoder type',
              'Close',
              {
                duration: 3000,
              }
            );
          },
        });
    });
  }

  editSelected(): void {
    const selected = this.gridApi?.getSelectedRows();

    if (!selected?.length) {
      this.snackBar.open(
        'Please select a row first',
        'Close',
        {
          duration: 3000,
        }
      );
      return;
    }

    console.log('Edit encoder', selected[0]);
  }

  onSelectionChanged(event: SelectionChangedEvent<EncoderRow>): void {
    const selectedRows = event.api.getSelectedRows();

    this.selectedEncoder =
      selectedRows.length > 0
        ? selectedRows[0]
        : undefined;
  }

  deleteSelected(): void {
    if (!this.selectedEncoder) {
      this.snackBar.open(
        'Please select a row first',
        'Close',
        {
          duration: 3000,
        }
      );

      return;
    }

    const confirmed = confirm(
      `Delete ${this.selectedEncoder.name}?`
    );

    if (!confirmed) {
      return;
    }

    this.uiOptionsService
      .deleteEncoderType(this.selectedEncoder.id)
      .subscribe({
        next: () => {
          this.selectedEncoder = undefined;

          this.loadEncoderTypes();

          this.snackBar.open(
            'Encoder type deleted successfully',
            'Close',
            {
              duration: 3000,
            }
          );
        },

        error: (err) => {
          console.error(err);

          this.snackBar.open(
            'Failed to delete encoder type',
            'Close',
            {
              duration: 3000,
            }
          );
        },
      });
  }
}

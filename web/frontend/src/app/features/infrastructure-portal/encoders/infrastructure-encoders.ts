import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { AgGridAngular } from 'ag-grid-angular';
import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridReadyEvent,
  ModuleRegistry,
} from 'ag-grid-community';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';

ModuleRegistry.registerModules([AllCommunityModule]);

interface EncoderRow {
  name: string;
  version: string;
  status: 'Active' | 'Warning' | 'Offline';
  description: string;
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
  ],
  templateUrl: './infrastructure-encoders.html',
  styleUrls: ['./infrastructure-encoders.scss'],
})
export class InfrastructureEncodersComponent {
  private gridApi?: GridApi;

  searchText = '';

  columnDefs: ColDef<EncoderRow>[] = [
    { field: 'name', headerName: 'Encoder', minWidth: 140 },
    { field: 'version', headerName: 'Version', minWidth: 120 },
    {
      field: 'status',
      headerName: 'Status',
      minWidth: 120,
      cellClassRules: {
        'status-active': (p) => p.value === 'Active',
        'status-warning': (p) => p.value === 'Warning',
        'status-offline': (p) => p.value === 'Offline',
      },
    },
    { field: 'description', headerName: 'Description', flex: 1, minWidth: 220 },
  ];

  rowData: EncoderRow[] = [
    { name: 'HM', version: 'Reference', status: 'Active', description: 'HEVC reference software' },
    { name: 'SHM', version: 'Reference', status: 'Warning', description: 'Scalable HEVC reference software' },
    { name: 'JM', version: 'Reference', status: 'Active', description: 'H.264/AVC reference software' },
    { name: 'GEM', version: 'Reference', status: 'Active', description: 'Extra encoder option from the docs' },
    { name: 'x265', version: '3.x', status: 'Active', description: 'Alternative standard-compliant encoder' },
  ];

  defaultColDef: ColDef = {
    sortable: true,
    filter: true,
    resizable: true,
  };

  onGridReady(params: GridReadyEvent<EncoderRow>) {
    this.gridApi = params.api;
    params.api.sizeColumnsToFit();
  }

  onSearch(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.searchText = value;
    this.gridApi?.setGridOption('quickFilterText', value);
  }

  addEncoder() {
    console.log('Add encoder');
  }

  editSelected() {
    console.log('Edit encoder');
  }

  deleteSelected() {
    console.log('Delete encoder');
  }
}

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
} from 'ag-grid-community';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';

import { UiOptionsService } from '../services/ui-options.service';

ModuleRegistry.registerModules([AllCommunityModule]);

interface CodecRow {
  id: number;
  name: string;
  version: string | null;
  status: string | null;
}

@Component({
  selector: 'app-infrastructure-codecs',
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
  templateUrl: './infrastructure-codecs.html',
  styleUrls: ['./infrastructure-codecs.scss'],
})
export class InfrastructureCodecsComponent implements OnInit {

  private gridApi?: GridApi;

  searchText = '';

  rowData: CodecRow[] = [];

  columnDefs: ColDef<CodecRow>[] = [
    {
      field: 'id',
      headerName: 'ID',
      width: 100,
    },
    {
      field: 'name',
      headerName: 'Codec',
      flex: 1,
    },
    {
      field: 'version',
      headerName: 'Version',
      flex: 1,
      valueFormatter: (p) => p.value ?? 'Not set',
    },
    {
      field: 'status',
      headerName: 'Status',
      flex: 1,
      valueFormatter: (p) => p.value ?? 'Not set',
    },
  ];

  defaultColDef: ColDef = {
    sortable: true,
    filter: true,
    resizable: true,
  };

  constructor(
    private uiOptionsService: UiOptionsService
  ) {}

  ngOnInit(): void {
    this.loadCodecs();
  }

  loadCodecs(): void {

    this.uiOptionsService
      .getUiOptions()
      .subscribe({

        next: (data) => {

          this.rowData = [
            ...(data.codecs ?? [])
          ];

        },

        error: (err) => {
          console.error(err);
        }

      });

  }

  onGridReady(params: GridReadyEvent<CodecRow>) {
    this.gridApi = params.api;
    params.api.sizeColumnsToFit();
  }

  onSearch(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.searchText = value;

    this.gridApi?.setGridOption(
      'quickFilterText',
      value
    );
  }

  addCodec() {
    console.log('Add codec');
  }

  editSelected() {
    console.log('Edit codec');
  }

  deleteSelected() {
    console.log('Delete codec');
  }
}

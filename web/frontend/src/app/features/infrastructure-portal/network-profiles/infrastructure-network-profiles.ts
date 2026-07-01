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
  SelectionChangedEvent,
  RowClassParams
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
import { AddNetworkProfileDialogComponent } from './add-network-profile-dialog/add-network-profile-dialog';

ModuleRegistry.registerModules([AllCommunityModule]);

interface NetworkProfileRow {

  id: number;

  name: string;

  lower_bound: number;

  upper_bound: number;

  unit: string;

  active: number;

  supported: number;

}

@Component({
  selector: 'app-infrastructure-network-profiles',
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
    MatSnackBarModule
  ],
  templateUrl: './infrastructure-network-profiles.html',
  styleUrls: ['./infrastructure-network-profiles.scss']
})
export class InfrastructureNetworkProfilesComponent implements OnInit {

  private gridApi?: GridApi<NetworkProfileRow>;

  rowData: NetworkProfileRow[] = [];

  selectedProfile?: NetworkProfileRow;

  columnDefs: ColDef<NetworkProfileRow>[] = [

    {
      field: 'id',
      headerName: 'ID',
      width: 90
    },

    {
      field: 'name',
      headerName: 'Network Profile',
      flex: 1,
      minWidth: 220
    },

    {
      headerName: 'Range',
      flex: 1,
      valueGetter: params =>
        `${params.data?.lower_bound} - ${params.data?.upper_bound}`
    },

    {
      field: 'unit',
      headerName: 'Unit',
      width: 120
    },

    {
      field: 'supported',
      headerName: 'Supported',
      width: 150,

      valueFormatter: params =>
        params.value === 1 ? 'Yes' : 'No',

      cellClass: params =>
        params.value === 1
          ? 'status-active'
          : 'status-unsupported'
    },

    {
      field: 'active',
      headerName: 'Status',
      width: 150,

      valueFormatter: params =>
        params.value === 1
          ? 'Active'
          : 'Inactive',

      cellClass: params =>
        params.value === 1
          ? 'status-active'
          : 'status-disabled'
    }

  ];

  defaultColDef: ColDef = {

    sortable: true,

    filter: true,

    resizable: true

  };

  rowClassRules = {

    'row-active': (params: RowClassParams<NetworkProfileRow>) =>
      !!params.data &&
      params.data.supported === 1 &&
      params.data.active === 1,

    'row-disabled': (params: RowClassParams<NetworkProfileRow>) =>
      !!params.data &&
      params.data.supported === 1 &&
      params.data.active === 0,

    'row-unsupported': (params: RowClassParams<NetworkProfileRow>) =>
      !!params.data &&
      params.data.supported === 0

  };

  constructor(

    private uiOptionsService: UiOptionsService,

    private dialog: MatDialog,

    private snackBar: MatSnackBar

  ) {}

  ngOnInit(): void {

    this.loadNetworkProfiles();

  }

  loadNetworkProfiles(): void {

    this.uiOptionsService.getUiOptions().subscribe({

      next: data => {

        this.rowData = (data.transmission_conditions ?? []).map((profile: any) => ({
          
          id: profile.id,

          name: profile.name,

          lower_bound: profile.lower_bound,

          upper_bound: profile.upper_bound,

          unit: profile.unit,

          active: profile.active,

          supported: profile.supported

        }));

      },

      error: () => {

        this.snackBar.open(

          'Failed to load network profiles.',

          'Close',

          {

            duration: 3000

          }

        );

      }

    });

  }

  onGridReady(params: GridReadyEvent<NetworkProfileRow>): void {

    this.gridApi = params.api;

    params.api.sizeColumnsToFit();

  }

  onSelectionChanged(
    event: SelectionChangedEvent<NetworkProfileRow>
  ): void {

    const rows = event.api.getSelectedRows();

    this.selectedProfile =
      rows.length > 0
        ? rows[0]
        : undefined;

  }

  addNetworkProfile(): void {

    const dialogRef = this.dialog.open(

      AddNetworkProfileDialogComponent,

      {

        width: '520px'

      }

    );

    dialogRef.afterClosed().subscribe(result => {

      if (!result) {
        return;
      }

      this.uiOptionsService.addTransmissionCondition({

        ...result,

        active: 0,

        supported: 0

      }).subscribe({

        next: () => {

          this.loadNetworkProfiles();

          this.snackBar.open(

            'Network profile added.',

            'Close',

            {

              duration: 3000

            }

          );

        },

        error: () => {

          this.snackBar.open(

            'Unable to add network profile.',

            'Close',

            {

              duration: 3000

            }

          );

        }

      });

    });

  }

  enableSelected(): void {

    if (!this.selectedProfile) {

      this.snackBar.open(

        'Please select a network profile.',

        'Close',

        {

          duration: 3000

        }

      );

      return;

    }

    if (!this.selectedProfile.supported) {

      this.snackBar.open(

        'This condition is not currently supported by the Experiments Engine.',

        'Close',

        {

          duration: 4000

        }

      );

      return;

    }

    this.uiOptionsService.toggleTransmissionCondition({

      id: this.selectedProfile.id,

      active: 1

    }).subscribe({

      next: () => {

        this.loadNetworkProfiles();

        this.snackBar.open(

          'Network profile enabled.',

          'Close',

          {

            duration: 3000

          }

        );

      }

    });

  }

  disableSelected(): void {

    if (!this.selectedProfile) {

      this.snackBar.open(

        'Please select a network profile.',

        'Close',

        {

          duration: 3000

        }

      );

      return;

    }

    this.uiOptionsService.toggleTransmissionCondition({

      id: this.selectedProfile.id,

      active: 0

    }).subscribe({

      next: () => {

        this.loadNetworkProfiles();

        this.snackBar.open(

          'Network profile disabled.',

          'Close',

          {

            duration: 3000

          }

        );

      }

    });

  }

}

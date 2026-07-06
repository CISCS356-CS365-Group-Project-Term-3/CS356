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
import { UserManagementService } from '../../user_management/user-management-service';
import { UserManagementService } from '../../user_management/user-management-service';
import { forkJoin } from 'rxjs';
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
  pendingEdits: Map<number, Partial<NetworkProfileRow>> = new Map();
  isAdmin = false;
  isAdmin = false;
  // True while a cell is being edited (enables save immediately on edit start)
  isEditing = false;

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
      field: 'lower_bound',
      headerName: 'Lower Bound',
      width: 160,
      editable: (params: any) => !!params.data && params.data.supported === 1 && params.data.active === 1 && this.isAdmin,
      editable: (params: any) => !!params.data && params.data.supported === 1 && params.data.active === 1 && this.isAdmin,
      valueParser: (params: any) => Number(params.newValue)
    },

    {
      field: 'upper_bound',
      headerName: 'Upper Bound',
      width: 160,
      editable: (params: any) => !!params.data && params.data.supported === 1 && params.data.active === 1 && this.isAdmin,
      editable: (params: any) => !!params.data && params.data.supported === 1 && params.data.active === 1 && this.isAdmin,
      valueParser: (params: any) => Number(params.newValue)
    },

    {
      field: 'unit',
      headerName: 'Unit',
      width: 120
    },

    {
      field: 'supported',
      headerName: 'Supported',
      width: 120,
      cellRenderer: (params: any) => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.disabled = true;
        checkbox.checked = params.value === 1;
        const wrapper = document.createElement('div');
        wrapper.style.display = 'flex';
        wrapper.style.justifyContent = 'center';
        wrapper.appendChild(checkbox);
        return wrapper;
      }
    },

    {
      field: 'active',
      headerName: 'Status',
      width: 150,

      valueFormatter: (params: any) =>
        params.value === 1
          ? 'Active'
          : 'Inactive',

      cellClass: (params: any) =>
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
    private userService: UserManagementService,
    private userService: UserManagementService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar

  ) {}

  ngOnInit(): void {
    this.loadUserRole();
    this.loadUserRole();
    this.loadNetworkProfiles();
  }

  private loadUserRole(): void {
    try {
      this.userService.getUserInfo().subscribe({
        next: (user: any) => {
          this.isAdmin = user.user_role === 'admin';
        },
        error: () => {
          this.isAdmin = false;
        }
      });
    } catch {
      this.isAdmin = false;
    }
  }

  private loadUserRole(): void {
    try {
      this.userService.getUserInfo().subscribe({
        next: (user: any) => {
          this.isAdmin = user.user_role === 'admin';
        },
        error: () => {
          this.isAdmin = false;
        }
      });
    } catch {
      this.isAdmin = false;
    }
  }

  private isBoundValidationTarget(row: NetworkProfileRow | undefined): boolean {
    if (!row || row.supported !== 1 || row.active !== 1) {
      return false;
    }

    const normalizedName = (row.name ?? '').trim().toLowerCase();
    return normalizedName.includes('delay')
      || normalizedName.includes('jitter')
      || normalizedName.includes('packet loss')
      || normalizedName.includes('packet-loss');
  }

  private validateBoundEdit(
    row: NetworkProfileRow | undefined,
    field: 'lower_bound' | 'upper_bound',
    value: number,
    pendingChanges?: Partial<NetworkProfileRow>
  ): { valid: boolean; message?: string } {
    if (!this.isBoundValidationTarget(row)) {
      return { valid: true };
    }

    if (!Number.isFinite(value)) {
      return {
        valid: false,
        message: `${row?.name ?? 'This profile'} bound must be a valid number.`
      };
    }

    if (value < 0 || value > 999) {
      return {
        valid: false,
        message: `${row?.name ?? 'This profile'} ${field === 'lower_bound' ? 'lower' : 'upper'} bound must be between 0 and 999.`
      };
    }

    const draftRow = {
      ...row,
      ...pendingChanges,
      [field]: value
    } as NetworkProfileRow | undefined;

    const lowerBound = draftRow?.lower_bound ?? 0;
    const upperBound = draftRow?.upper_bound ?? 0;

    if (upperBound <= lowerBound) {
      return {
        valid: false,
        message: `${row?.name ?? 'This profile'} upper bound must be greater than lower bound.`
      };
    }

    return { valid: true };
  }

  private revertInvalidBoundEdit(event: any): void {
    const id = event.data?.id;
    const field = event.colDef?.field as 'lower_bound' | 'upper_bound' | undefined;

    if (!id || !field) {
      return;
    }

    const row = this.rowData.find(profile => profile.id === id);
    if (!row) {
      return;
    }

    row[field] = event.oldValue;
    this.gridApi?.refreshCells({ force: true });
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

  onCellValueChanged(event: any): void {
    const field = event.colDef?.field;
    if (field !== 'lower_bound' && field !== 'upper_bound') {
      return;
    }

    const id = event.data?.id;
    if (!id) {
      return;
    }

    const row = this.rowData.find(profile => profile.id === id);
    const pendingChanges = this.pendingEdits.get(id) || {};
    const parsedValue = Number(event.newValue);
    const validationResult = this.validateBoundEdit(
      row,
      field as 'lower_bound' | 'upper_bound',
      parsedValue,
      pendingChanges
    );

    if (!validationResult.valid) {
      this.revertInvalidBoundEdit(event);
      this.snackBar.open(validationResult.message ?? 'Invalid bound value.', 'Close', { duration: 4000 });
      return;
    }

    const existing = this.pendingEdits.get(id) || {};
    (existing as any)[field as keyof NetworkProfileRow] = parsedValue;
    this.pendingEdits.set(id, existing);
  }

  saveChanges(): void {
    if (this.pendingEdits.size === 0) {
      this.snackBar.open('No changes to save.', 'Close', { duration: 2000 });
      return;
    }

    const requests: any[] = [];
    const invalidEdits: string[] = [];

    this.pendingEdits.forEach((changes, id) => {
      const row = this.rowData.find(profile => profile.id === id);
      const lowerBound = changes.lower_bound ?? row?.lower_bound;
      const upperBound = changes.upper_bound ?? row?.upper_bound;

      if (typeof lowerBound === 'number' && this.validateBoundEdit(row, 'lower_bound', lowerBound, changes).valid === false) {
        invalidEdits.push(row?.name ?? `Profile ${id}`);
        return;
      }

      if (typeof upperBound === 'number' && this.validateBoundEdit(row, 'upper_bound', upperBound, changes).valid === false) {
        invalidEdits.push(row?.name ?? `Profile ${id}`);
        return;
      }

      requests.push(this.uiOptionsService.toggleTransmissionCondition({ id, ...changes }));
    });

    if (invalidEdits.length > 0) {
      this.snackBar.open(
        `Unable to save invalid bound values for ${invalidEdits[0]}.`,
        'Close',
        { duration: 4000 }
      );
      return;
    }

    forkJoin(requests).subscribe({
      next: () => {
        this.pendingEdits.clear();
        this.loadNetworkProfiles();
        this.snackBar.open('Saved changes to network profiles.', 'Close', { duration: 3000 });
      },
      error: () => {
        this.snackBar.open('Failed to save some changes.', 'Close', { duration: 4000 });
        this.loadNetworkProfiles();
      }
    });
  }

  onCellEditingStarted(event: any): void {
    const field = event.colDef?.field;
    if (field === 'lower_bound' || field === 'upper_bound') {
      this.isEditing = true;
    }
  }

  onCellEditingStopped(event: any): void {
    this.isEditing = false;
  }

  hasEdits(): boolean {
    return this.pendingEdits.size > 0 || this.isEditing;
  }

  onSelectionChanged(
    event: SelectionChangedEvent<NetworkProfileRow>
  ): void {

    const rows = event.api.getSelectedRows();

    this.selectedProfile =
      rows.length > 0? rows[0]: undefined;
  }

  addNetworkProfile(): void {

    const dialogRef = this.dialog.open(
      AddNetworkProfileDialogComponent,
      {
        width: '520px'
      });

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

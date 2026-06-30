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
  SelectionChangedEvent,
} from 'ag-grid-community';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';

ModuleRegistry.registerModules([AllCommunityModule]);

interface NetworkProfileRow {
  name: string;
  packetLoss: string;
  delay: string;
  jitter: string;
  bandwidth: string;
  notes: string;
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
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
  ],
  templateUrl: './infrastructure-network-profiles.html',
  styleUrls: ['./infrastructure-network-profiles.scss'],
})
export class InfrastructureNetworkProfilesComponent {
  private gridApi?: GridApi;

  searchText = '';
  selectedProfile?: NetworkProfileRow;

  columnDefs: ColDef<NetworkProfileRow>[] = [
    { field: 'name', headerName: 'Profile', minWidth: 170 },
    { field: 'packetLoss', headerName: 'Packet Loss', minWidth: 120 },
    { field: 'delay', headerName: 'Delay', minWidth: 120 },
    { field: 'jitter', headerName: 'Jitter', minWidth: 120 },
    { field: 'bandwidth', headerName: 'Bandwidth', minWidth: 140 },
    { field: 'notes', headerName: 'Notes', flex: 1, minWidth: 220 },
  ];

  rowData: NetworkProfileRow[] = [
    {
      name: 'Packet Loss',
      packetLoss: 'Yes',
      delay: 'Optional',
      jitter: 'Optional',
      bandwidth: 'Optional',
      notes: 'Simulates packet loss only',
    },
    {
      name: 'Delay',
      packetLoss: 'Optional',
      delay: 'Yes',
      jitter: 'Optional',
      bandwidth: 'Optional',
      notes: 'Adds fixed delay to traffic',
    },
    {
      name: 'Jitter',
      packetLoss: 'Optional',
      delay: 'Optional',
      jitter: 'Yes',
      bandwidth: 'Optional',
      notes: 'Varying delay pattern',
    },
    {
      name: 'Bandwidth Throttling',
      packetLoss: 'Optional',
      delay: 'Optional',
      jitter: 'Optional',
      bandwidth: 'Yes',
      notes: 'Limits available throughput',
    },
    {
      name: 'Consistent Delay',
      packetLoss: 'Optional',
      delay: 'Yes',
      jitter: 'No',
      bandwidth: 'Optional',
      notes: 'Stable fixed latency',
    },
  ];

  defaultColDef: ColDef = {
    sortable: true,
    filter: true,
    resizable: true,
  };

  onGridReady(params: GridReadyEvent<NetworkProfileRow>) {
    this.gridApi = params.api;
    params.api.sizeColumnsToFit();
  }

  onSearch(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.searchText = value;
    this.gridApi?.setGridOption('quickFilterText', value);
  }

  onSelectionChanged(event: SelectionChangedEvent) {
    const selected = event.api.getSelectedRows();
    this.selectedProfile = selected.length ? selected[0] : undefined;
  }

  addProfile() {
    console.log('Add profile');
  }

  editSelected() {
    console.log('Edit selected profile');
  }

  applySelected() {
    console.log('Apply selected profile');
  }
}

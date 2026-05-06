import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, ModuleRegistry } from 'ag-grid-community';
import { ExperimentsService } from '../services/experiments';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-dashboard',
  imports: [MatButtonModule, MatCardModule, AgGridAngular],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  experiments: any[] = [];
  isAdmin: boolean = false; // TODO: replace this with the real auth check, can do this when we know how the JWT is structured (from user mgmt team)

  colDefs: ColDef[] = [
    { field: 'id', headerName: 'Name', valueGetter: (p) => p.data.id + ' ' + p.data.name, flex: 2 },
    { field: 'codec', flex: 1 },
    { field: 'sequences', flex: 2 },
    { field: 'date', flex: 1 },
    { field: 'status', flex: 1 },
  ];

  constructor(private experimentsService: ExperimentsService) {}

  ngOnInit() {
    // this.isAdmin = this.authService.isAdmin(); // TODO: we would pass this value into the getExperiments fnc to determine whether we show ALL experiments (admin) or just the users
    this.experimentsService.getExperiments().subscribe((data) => {
      this.experiments = data;
    });
  }
}

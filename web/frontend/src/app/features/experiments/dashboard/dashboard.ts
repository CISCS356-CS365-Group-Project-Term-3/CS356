import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, ModuleRegistry } from 'ag-grid-community';
import { ExperimentsService } from '../services/experiments';
import { Experiment, ExperimentStatus } from '../models/experiment.model';
import { RouterLink } from '@angular/router';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-dashboard',
  imports: [MatButtonModule, MatCardModule, AgGridAngular, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  experiments: Experiment[] = [];
  isAdmin: boolean = false; // TODO: replace this with the real auth check, can do this when we know how the JWT is structured (from user mgmt team)

  colDefs: ColDef[] = [
    { field: 'id', headerName: 'Name', valueGetter: (p) => p.data.id + ' ' + p.data.name, flex: 2 },
    { field: 'codec', flex: 1 },
    { field: 'sequences', flex: 2 },
    { field: 'date', flex: 1 },
    {
      field: 'status',
      flex: 1,
      cellRenderer: (params: { value: ExperimentStatus }) => this.statusCellRenderer(params),
    },
  ];

  get totalCount() {
    return this.experiments.length;
  }
  get completedCount() {
    return this.experiments.filter((e) => e.status === 'Complete').length;
  }
  get runningCount() {
    return this.experiments.filter((e) => e.status === 'Running').length;
  }
  get failedCount() {
    return this.experiments.filter((e) => e.status === 'Failed').length;
  }

  constructor(private experimentsService: ExperimentsService) {}

  ngOnInit() {
    // this.isAdmin = this.authService.isAdmin(); // TODO: we would pass this value into the getExperiments fnc to determine whether we show ALL experiments (admin) or just the users
    this.experimentsService.getExperiments().subscribe((data) => {
      this.experiments = data;
    });
  }

  statusCellRenderer(params: { value: ExperimentStatus }) {
    const styles: Record<ExperimentStatus, string> = {
      Complete: 'background:#e8f5e9;color:#388e3c',
      Running: 'background:#fff3e0;color:#f57c00',
      Failed: 'background:#ffebee;color:#d32f2f',
    };
    const style = styles[params.value] ?? 'background:#f5f5f5;color:#888';
    return `<span style="${style};padding:2px 10px;border-radius:12px;font-size:12px;font-weight:500;">${params.value}</span>`;
  }
}

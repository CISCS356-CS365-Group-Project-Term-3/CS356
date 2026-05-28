import { Component, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { AgGridAngular } from 'ag-grid-angular';
import {
  AllCommunityModule,
  ColDef,
  ModuleRegistry,
  RowClickedEvent,
  SelectionChangedEvent,
} from 'ag-grid-community';
import { ExperimentsService } from '../services/experiments';
import { Experiment, ExperimentStatus } from '../models/experiment.model';
import { Router, RouterLink } from '@angular/router';
import { NewExperimentFormService } from '../new-experiment/new-experiment-form.service';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-dashboard',
  imports: [MatButtonModule, MatCardModule, MatSlideToggleModule, AgGridAngular, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  experiments: Experiment[] = [];
  selectedExperiment: Experiment | null = null;
  activeStatusFilter: ExperimentStatus | null = null;
  showAllExperiments = false;
  isLoading = true;
  isAdmin: boolean = false; // TODO: replace with real auth check once JWT structure is known

  colDefs: ColDef[] = [
    {
      field: 'id',
      headerName: 'Name',
      valueGetter: (p) => p.data.id + ' ' + p.data.name,
      flex: 2,
    },
    { field: 'codec', flex: 1 },
    { field: 'sequences', flex: 2 },
    { field: 'date', flex: 1 },
    {
      field: 'status',
      flex: 1,
      filter: true,
      cellRenderer: (params: { value: ExperimentStatus }) => this.statusCellRenderer(params),
    },
  ];

  getRowId = (params: { data: Experiment }) => String(params.data.id);

  get filteredExperiments(): Experiment[] {
    if (!this.activeStatusFilter) return this.experiments;
    return this.experiments.filter((e) => e.status === this.activeStatusFilter);
  }

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

  constructor(
    private experimentsService: ExperimentsService,
    private formService: NewExperimentFormService,
    private router: Router,
  ) {}

  ngOnInit() {
    // this.isAdmin = this.authService.isAdmin();
    this.loadExperiments();
  }

  loadExperiments(): void {
    // const scope = this.isAdmin && this.showAllExperiments ? 'all' : 'mine';
    // this.experimentsService.getExperiments(scope).subscribe(data => { this.experiments = data; });
    this.experimentsService.getExperiments().subscribe((data) => {
      this.experiments = data;
      this.isLoading = false;
    });
  }

  onScopeToggle(): void {
    this.showAllExperiments = !this.showAllExperiments;
    this.activeStatusFilter = null;
    this.loadExperiments();
  }

  setStatusFilter(status: ExperimentStatus | null): void {
    this.activeStatusFilter = this.activeStatusFilter === status ? null : status;
  }

  onSelectionChanged(event: SelectionChangedEvent): void {
    const rows = event.api.getSelectedRows();
    this.selectedExperiment = rows.length > 0 ? rows[0] : null;
  }

  onRowClicked(event: RowClickedEvent): void {
    if (this.selectedExperiment?.id === event.data.id) {
      event.node.setSelected(false);
    }
  }

  createFromTemplate(): void {
    if (!this.selectedExperiment) return;
    this.experimentsService.getExperimentById(this.selectedExperiment.id).subscribe((detail) => {
      this.formService.setTemplate(detail);
      this.router.navigate(['/experiments/new']);
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

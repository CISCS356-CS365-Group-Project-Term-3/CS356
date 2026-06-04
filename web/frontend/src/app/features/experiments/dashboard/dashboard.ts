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
import { InfrastructureService } from '../services/infrastructure';
import { InfrastructureConfig } from '../models/infrastructure-config.model';

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
  private config: InfrastructureConfig | null = null;

  colDefs: ColDef[] = [
    {
      headerName: 'Name',
      valueGetter: (p) => p.data.id + ' ' + p.data.name,
      flex: 1.5,
    },
    {
      headerName: 'Codec',
      valueGetter: (p) =>
        this.config?.codecs.find((c) => c.id === p.data.encoders[0]?.codecId)?.name ?? '—',
      flex: 1,
    },
    {
      headerName: 'Sequences',
      valueGetter: (p) =>
        p.data.sequences
          .map(
            (s: Experiment['sequences'][0]) =>
              this.config?.sequences.find((seq) => seq.videoFiles.some((f) => f.id === s.videoFileId))?.name ?? '—',
          )
          .join(', '),
      flex: 2,
    },
    {
      field: 'date',
      flex: 1,
      valueFormatter: (p) => {
        const d = new Date(p.value);
        return isNaN(d.getTime()) ? p.value : d.toLocaleString('en-GB', { dateStyle: 'short', timeStyle: 'short' });
      },
    },
    {
      headerName: 'Status',
      field: 'engineStatus',
      flex: 1,
      cellRenderer: (params: { value: ExperimentStatus | undefined }) => this.statusCellRenderer(params),
    },
  ];

  getRowId = (params: { data: Experiment }) => String(params.data.id);

  get filteredExperiments(): Experiment[] {
    if (!this.activeStatusFilter) return this.experiments;
    return this.experiments.filter((e) => e.engineStatus === this.activeStatusFilter);
  }

  get totalCount() {
    return this.experiments.length;
  }
  get completedCount() {
    return this.experiments.filter((e) => e.engineStatus === 'Complete').length;
  }
  get runningCount() {
    return this.experiments.filter((e) => e.engineStatus === 'Running').length;
  }
  get failedCount() {
    return this.experiments.filter((e) => e.engineStatus === 'Failed').length;
  }

  constructor(
    private experimentsService: ExperimentsService,
    private formService: NewExperimentFormService,
    private router: Router,
    private infrastructureService: InfrastructureService,
  ) {}

  ngOnInit() {
    // this.isAdmin = this.authService.isAdmin();
    this.infrastructureService.getConfig().subscribe((config) => {
      this.config = config;
      this.loadExperiments();
    });
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

  statusCellRenderer(params: { value: ExperimentStatus | undefined }) {
    if (!params.value) return `<span style="background:#f5f5f5;color:#888;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:500;">Pending</span>`;
    const styles: Record<ExperimentStatus, string> = {
      Complete: 'background:#e8f5e9;color:#388e3c',
      Running: 'background:#fff3e0;color:#f57c00',
      Failed: 'background:#ffebee;color:#d32f2f',
    };
    const style = styles[params.value] ?? 'background:#f5f5f5;color:#888';
    return `<span style="${style};padding:2px 10px;border-radius:12px;font-size:12px;font-weight:500;">${params.value}</span>`;
  }
}

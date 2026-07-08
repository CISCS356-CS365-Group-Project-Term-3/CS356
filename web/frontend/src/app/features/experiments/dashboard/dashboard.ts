import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AgGridAngular } from 'ag-grid-angular';
import {
  AllCommunityModule,
  ColDef,
  ModuleRegistry,
  RowClickedEvent,
  SelectionChangedEvent,
  RowSelectionOptions,
} from 'ag-grid-community';
import { ExperimentsService } from '../services/experiments';
import { Experiment, ExperimentRun, ExperimentStatus } from '../models/experiment.model';
import { Router, RouterLink } from '@angular/router';
import { NewExperimentFormService } from '../new-experiment/new-experiment-form.service';
import { InfrastructureService } from '../services/infrastructure';
import { InfrastructureConfig } from '../models/infrastructure-config.model';
import { UserManagementService } from '../../user_management/user-management-service';
import { CommonModule } from '@angular/common';
import { interval, Subscription, switchMap } from 'rxjs';

const POLL_INTERVAL_MS = 5000;

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-dashboard',
  imports: [
    MatButtonModule,
    MatCardModule,
    MatSlideToggleModule,
    MatProgressSpinnerModule,
    AgGridAngular,
    RouterLink,
    CommonModule,
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit, OnDestroy {
  experiments: Experiment[] = [];
  selectedExperiment: Experiment | null = null;
  activeStatusFilter: string | null = null;
  showAllExperiments = false;
  showDraftsOnly = false;
  isLoading = true;
  isAdmin: boolean = false;
  private userId: number | null = null;
  private config: InfrastructureConfig | null = null;
  private pollSub?: Subscription;

  constructor(
    private experimentsService: ExperimentsService,
    private formService: NewExperimentFormService,
    private router: Router,
    private infrastructureService: InfrastructureService,
    private userService: UserManagementService,
  ) {}

  ngOnInit() {
    this.infrastructureService.refreshConfig();
    this.infrastructureService.getConfig().subscribe({
      next: (config) => {
        this.config = config;
      },
      error: () => {},
    });
    try {
      this.userService.getUserInfo().subscribe({
        next: (user: any) => {
          this.userId = user.user_id;
          this.isAdmin = user.user_role === 'admin';
          this.loadExperiments();
        },
        error: () => {
          this.loadExperiments();
        },
      });
    } catch {
      this.loadExperiments();
    }
  }

  loadExperiments(): void {
    this.experimentsService.getExperiments(this.scopedUserId()).subscribe({
      next: (data) => {
        this.experiments = data;
        this.isLoading = false;
        this.updatePolling();
      },
      error: () => {
        this.isLoading = false;
      },
    });
  }

  ngOnDestroy(): void {
    this.stopPolling();
  }

  private scopedUserId(): number | undefined {
    return this.isAdmin && this.showAllExperiments ? undefined : (this.userId ?? undefined);
  }

  private hasActiveRuns(): boolean {
    return this.experiments.some((exp) => {
      const status = this.getGroupStatus(exp);
      return status === 'pending' || status === 'running';
    });
  }

  private updatePolling(): void {
    if (this.hasActiveRuns()) {
      this.startPolling();
    } else {
      this.stopPolling();
    }
  }

  private startPolling(): void {
    if (this.pollSub) return;
    this.pollSub = interval(POLL_INTERVAL_MS)
      .pipe(switchMap(() => this.experimentsService.getExperiments(this.scopedUserId())))
      .subscribe({
        next: (data) => {
          this.experiments = data;
          this.updatePolling();
        },
      });
  }

  private stopPolling(): void {
    this.pollSub?.unsubscribe();
    this.pollSub = undefined;
  }

  onScopeToggle(): void {
    this.showAllExperiments = !this.showAllExperiments;
    this.loadExperiments();
  }

  onSelectionChanged(event: SelectionChangedEvent): void {
    const rows = event.api.getSelectedRows();
    this.selectedExperiment = rows.length > 0 ? rows[0] : null;
  }

  onRowClicked(event: RowClickedEvent): void {
    if (this.selectedExperiment?.groupID === event.data.groupID) {
      event.node.setSelected(false);
      this.selectedExperiment = null;
    }
  }

  colDefs: ColDef[] = [
    {
      headerName: 'Experiment Name',
      valueGetter: (p) => p.data.groupID + ' - ' + p.data.name,
      flex: 2,
    },
    {
      headerName: 'Status',
      flex: 1,
      valueGetter: (p) => this.getGroupStatus(p.data),
      cellRenderer: (params: { value: string; data: Experiment | undefined }) =>
        this.renderExperimentStatusCell(params),
    },
    {
      field: 'date',
      flex: 1.2,
      sort: 'desc',
      valueFormatter: (p) => {
        const d = new Date(p.value);
        return isNaN(d.getTime())
          ? p.value
          : d.toLocaleString('en-GB', { dateStyle: 'short', timeStyle: 'short' });
      },
    },
  ];

  detailColDefs: ColDef[] = [
    {
      headerName: 'Run ID',
      field: 'id',
      flex: 0.6,
    },
    {
      headerName: 'Encoder Type',
      valueGetter: (p) => this.getEncoderTypeName(p.data?.encoderData?.encoderTypeId),
      flex: 0.8,
    },
    {
      headerName: 'Codec',
      valueGetter: (p) => this.getCodecName(p.data?.encoderData?.codecId),
      flex: 0.7,
    },
    {
      headerName: 'Video File',
      valueGetter: (p) => this.getVideoFileName(p.data?.sequenceData?.videoFileId),
      flex: 0.8,
    },
    {
      headerName: 'Packet Loss (%)',
      valueGetter: (p) => this.formatPacketLoss(p.data?.networkData?.packetLoss),
      flex: 0.7,
    },
    {
      headerName: 'Delay (ms)',
      valueGetter: (p) => this.formatMs(p.data?.networkData?.delay),
      flex: 0.6,
    },
    {
      headerName: 'Jitter (ms)',
      valueGetter: (p) => this.formatMs(p.data?.networkData?.jitter),
      flex: 0.6,
    },
    {
      headerName: 'Status',
      field: 'status',
      flex: 0.8,
      cellRenderer: (params: { value: string }) => this.renderRunStatusCell(params.value),
    },
    {
      headerName: 'Date',
      field: 'date',
      flex: 1,
      sort: 'desc',
      valueFormatter: (p) => {
        const d = new Date(p.value);
        return isNaN(d.getTime())
          ? p.value
          : d.toLocaleString('en-GB', { dateStyle: 'short', timeStyle: 'short' });
      },
    },
  ];

  getRowId = (params: { data: Experiment }) => String(params.data.groupID);

  rowSelection: RowSelectionOptions = {
    mode: 'singleRow',
  };

  get filteredExperiments(): Experiment[] {
    let experiments = this.showDraftsOnly
      ? this.experiments.filter((e) => e.status === 'draft')
      : this.experiments;
    if (this.activeStatusFilter) {
      experiments = experiments.filter(
        (exp) => this.getGroupStatus(exp) === this.activeStatusFilter,
      );
    }

    return experiments;
  }

  getGroupStatus(exp: Experiment): string {
    if (exp.status === 'draft') return 'draft';
    const runs = exp.runs ?? [];
    const hasFailed = runs.some((r) => r.status === 'failed');
    const hasRunning = runs.some((r) => r.status === 'running');
    const allComplete = runs.every((r) => r.status === 'complete');

    if (hasFailed) return 'failed';
    if (hasRunning) return 'running';
    if (allComplete) return 'complete';

    return 'pending';
  }

  get filteredRuns(): ExperimentRun[] {
    if (!this.selectedExperiment) return [];
    return this.selectedExperiment.runs;
  }

  toggleDrafts(): void {
    this.showDraftsOnly = !this.showDraftsOnly;
    this.activeStatusFilter = null;
    this.selectedExperiment = null;
  }

  get pendingRunsCount() {
    return this.experiments.filter((e) => this.getGroupStatus(e) === 'pending').length;
  }

  get runningRunsCount() {
    return this.experiments.filter((e) => this.getGroupStatus(e) === 'running').length;
  }

  get completedRunsCount() {
    return this.experiments.filter((e) => this.getGroupStatus(e) === 'complete').length;
  }

  get failedRunsCount() {
    return this.experiments.filter((e) => this.getGroupStatus(e) === 'failed').length;
  }

  setStatusFilter(status: string): void {
    this.activeStatusFilter = this.activeStatusFilter === status ? null : status;
  }

  createFromTemplate(): void {
    if (!this.selectedExperiment) return;
    this.formService.setTemplate(this.selectedExperiment);
    this.router.navigate(['/experiments/new']);
  }

  openDraft(): void {
    if (!this.selectedExperiment) return;
    this.formService.setDraft(this.selectedExperiment);
    this.router.navigate(['/experiments/new']);
  }

  private getEncoderTypeName(id: number | null | undefined): string {
    if (id == null) return 'N/A';
    return this.config?.encoderTypes.find((e) => e.id === id)?.name ?? 'N/A';
  }

  private getCodecName(id: number | null | undefined): string {
    if (id == null) return 'N/A';
    return this.config?.codecs.find((c) => c.id === id)?.name ?? 'N/A';
  }

  private getVideoFileName(id: number | null | undefined): string {
    if (id == null) return 'N/A';
    const videoFiles = this.config?.sequences.flatMap((s) => s.videoFiles) ?? [];
    return videoFiles.find((v) => v.id === id)?.name ?? 'N/A';
  }

  private formatPacketLoss(raw: string | null | undefined): string {
    if (raw == null) return 'N/A';
    const n = Number(raw);
    return isNaN(n) ? 'N/A' : (n / 10).toFixed(1); // 200 -> 20.0
  }

  private formatMs(raw: string | null | undefined): string {
    if (raw == null) return 'N/A';
    const n = Number(raw); // strips 0 padding, 005 -> 5
    return isNaN(n) ? 'N/A' : String(n);
  }

  private static readonly STATUS_STYLES: Record<string, string> = {
    complete: 'background:#e8f5e9;color:#388e3c',
    running: 'background:#fff3e0;color:#f57c00',
    failed: 'background:#ffebee;color:#d32f2f',
    pending: 'background:#f5f5f5;color:#888',
    draft: 'background:#e3f2fd;color:#1565c0',
  };

  private static readonly STATUS_LABELS: Record<string, string> = {
    complete: 'Complete',
    running: 'Running',
    failed: 'Failed',
    pending: 'Pending',
    draft: 'Draft',
  };

  renderExperimentStatusCell(params: { value: string | undefined; data: Experiment | undefined }) {
    if (!params.data) return '';

    const statusValue = params.value ?? (params.data.status === 'draft' ? 'draft' : 'pending');
    return this.renderStatusBadge(statusValue);
  }

  renderRunStatusCell(status: string | null | undefined) {
    if (!status) return '';
    return this.renderStatusBadge(status);
  }

  private renderStatusBadge(value: string): string {
    const style = Dashboard.STATUS_STYLES[value] ?? 'background:#f5f5f5;color:#888';
    const label = Dashboard.STATUS_LABELS[value] ?? value;
    return `<span style="${style};padding:2px 10px;border-radius:12px;font-size:12px;font-weight:500;">${label}</span>`;
  }
}

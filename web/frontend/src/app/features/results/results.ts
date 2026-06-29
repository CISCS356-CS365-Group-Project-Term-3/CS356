import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { catchError, combineLatest, of } from 'rxjs';
import { ResultsService } from './services/results-service';
import { MetricAverage, ResultSummary } from './models/result-summary.model';
import { InfrastructureService } from '../experiments/services/infrastructure';
import { InfrastructureConfig } from '../experiments/models/infrastructure-config.model';

interface MetricSummary {
  label: string;
  value: string;
  hint: string;
}

interface ExperimentResult {
  id: number;
  title: string;
  name: string;
  date: string;
  codec: string;
  sequence: string;
  frameCount: number;
  success: boolean;
  failureReason: string | null;
  psnrSummary: MetricSummary[];
  ssimSummary: MetricSummary[];
  // Synthetic per-frame trend, anchored to the real average — true per-frame
  // series from the engine isn't wired up yet.
  psnrSeries: number[];
  ssimSeries: number[];
}

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [MatCardModule, FormsModule],
  templateUrl: './results.html',
  styleUrl: './results.scss',
})
export class ResultsPage implements OnInit {
  readonly chartWidth = 500;
  readonly chartHeight = 200;
  readonly chartPadding = 24;

  loading = true;
  experimentHistory: ExperimentResult[] = [];

  sortOption: 'newest' | 'oldest' = 'newest';
  showFilters = false;

  selectedExperiment: ExperimentResult | undefined;

  constructor(
    private resultsService: ResultsService,
    private infrastructureService: InfrastructureService,
  ) {}

  ngOnInit(): void {
    combineLatest([
      this.resultsService.getResultSummaries().pipe(catchError(() => of([] as ResultSummary[]))),
      this.infrastructureService.getConfig().pipe(catchError(() => of(undefined))),
    ]).subscribe(([results, config]) => {
      this.experimentHistory = results.map((result) => this.toExperimentResult(result, config));
      this.selectedExperiment = this.visibleExperiments[0];
      this.loading = false;
    });
  }

  get visibleExperiments(): ExperimentResult[] {
    const sorted = [...this.experimentHistory];
    sorted.sort((left, right) => {
      switch (this.sortOption) {
        case 'oldest':
          return this.parseDate(left.date) - this.parseDate(right.date);
        case 'newest':
        default:
          return this.parseDate(right.date) - this.parseDate(left.date);
      }
    });

    return sorted;
  }

  get sortBadgeLabel(): string {
    return this.sortOption === 'oldest' ? 'Oldest first' : 'Newest first';
  }

  get emptyStateMessage(): string {
    return this.loading ? 'Loading experiment history…' : 'No experiments match that search.';
  }

  toggleSort(): void {
    this.sortOption = this.sortOption === 'newest' ? 'oldest' : 'newest';
  }

  selectExperiment(experiment: ExperimentResult): void {
    this.selectedExperiment = experiment;
  }

  get psnrPath(): string {
    // For PSNR, expect values generally between 30 and 45.
    // Setting a fixed window size of 10dB contextually scales tiny ripples perfectly.
    const series = this.selectedExperiment?.psnrSeries ?? [];
    const average = series.reduce((a, b) => a + b, 0) / (series.length || 1);
    return this.buildPath(series, average - 5, average + 5);
  }

  get ssimPath(): string {
    // For SSIM, max is 1.0. We give it a small visual window range of 0.1 total
    // to keep the line flat near the top half.
    const series = this.selectedExperiment?.ssimSeries ?? [];
    const average = series.reduce((a, b) => a + b, 0) / (series.length || 1);
    return this.buildPath(series, average - 0.05, average + 0.05);
  }

  private toExperimentResult(
    result: ResultSummary,
    config: InfrastructureConfig | undefined,
  ): ExperimentResult {
    const codecName = config?.codecs.find((codec) => codec.id === result.codecId)?.name;
    const videoFile = config?.sequences
      .flatMap((sequence) => sequence.videoFiles)
      .find((file) => file.id === result.videoFileId);
    const sequenceName = videoFile?.name ?? result.sequenceCode ?? 'Unknown sequence';

    return {
      id: result.experimentId,
      title: result.experimentName ?? `Experiment ${result.experimentId}`,
      name: sequenceName,
      date: this.formatDate(result.createdAt),
      codec: codecName ?? 'Unknown codec',
      sequence: sequenceName,
      frameCount: result.frameCount,
      success: result.success,
      failureReason: result.failureReason,
      psnrSummary: this.buildSummary(result.psnrAverage, (value) => `${value.toFixed(2)} dB`),
      ssimSummary: this.buildSummary(result.ssimAverage, (value) => value.toFixed(3)),
      psnrSeries: this.mockSeriesAround(result.psnrAverage.combined ?? 0, 0.15),
      ssimSeries: this.mockSeriesAround(result.ssimAverage.combined ?? 0, 0.01),
    };
  }

  private buildSummary(average: MetricAverage, format: (value: number) => string): MetricSummary[] {
    const fmt = (value: number | null) => (value == null ? '—' : format(value));

    return [
      { label: 'Y', value: fmt(average.y), hint: 'Luma' },
      { label: 'U', value: fmt(average.u), hint: 'Chrominance' },
      { label: 'V', value: fmt(average.v), hint: 'Chrominance' },
      { label: 'All', value: fmt(average.combined), hint: 'Overall' },
    ];
  }

  // Generates a deterministic wiggle around the real average so the trend chart
  // still reads naturally until per-frame data is exposed by the backend.
  private mockSeriesAround(average: number, spread: number, points = 12): number[] {
    return Array.from({ length: points }, (_, index) => average + spread * Math.sin(index * 1.3));
  }

  private formatDate(value: string | null): string {
    if (!value) {
      return 'Unknown date';
    }

    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return 'Unknown date';
    }

    const pad = (n: number) => n.toString().padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
  }

  private parseDate(value: string): number {
    return Date.parse(value.replace(' ', 'T'));
  }

  private buildPath(values: number[], explicitMin: number, explicitMax: number): string {
    const width = this.chartWidth;
    const height = this.chartHeight;
    const padding = this.chartPadding;
    const range = explicitMax - explicitMin || 1;

    if (values.length === 0) {
      return '';
    }

    return values
      .map((value, index) => {
        const x = padding + (index / (values.length - 1 || 1)) * (width - padding * 2);
        // Standardize Y mapping to the explicit data window bounds
        const y = height - padding - ((value - explicitMin) / range) * (height - padding * 2);
        return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
      })
      .join(' ');
  }
}

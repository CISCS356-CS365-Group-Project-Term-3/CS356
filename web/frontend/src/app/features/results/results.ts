import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { catchError, combineLatest, forkJoin, map, of, switchMap } from 'rxjs';
import { ResultsService } from './services/results-service';
import { ExperimentFrames, MetricAverage, ResultSummary } from './models/result-summary.model';
import { InfrastructureService } from '../experiments/services/infrastructure';
import { InfrastructureConfig } from '../experiments/models/infrastructure-config.model';

interface ResultWithFrames {
  result: ResultSummary;
  frames: ExperimentFrames | undefined;
}

const LINE_COLORS = ['#2563eb', '#0f766e', '#d97706', '#dc2626', '#7c3aed', '#059669', '#db2777', '#0891b2'];

interface MetricSummary {
  label: string;
  value: string;
  hint: string;
}

interface CodecRun {
  codecName: string;
  color: string;
  success: boolean;
  failureReason: string | null;
  frameCount: number;
  psnrSummary: MetricSummary[];
  ssimSummary: MetricSummary[];
  psnrSeries: number[];
  ssimSeries: number[];
}

interface ChartLine {
  codecName: string;
  color: string;
  path: string;
}

interface ExperimentResult {
  id: string;
  title: string;
  name: string;
  date: string;
  codecsLabel: string;
  codecRuns: CodecRun[];
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
    ])
      .pipe(
        switchMap(([results, config]) =>
          forkJoin(
            results.map((result) =>
              this.resultsService.getFrames(result.experimentId).pipe(
                catchError(() => of(undefined)),
                map((frames): ResultWithFrames => ({ result, frames })),
              ),
            ),
          ).pipe(map((resultsWithFrames) => ({ resultsWithFrames, config }))),
        ),
      )
      .subscribe(({ resultsWithFrames, config }) => {
        this.experimentHistory = this.groupIntoExperiments(resultsWithFrames, config);
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

  get psnrChartLines(): ChartLine[] {
    return this.buildChartLines((run) => run.psnrSeries);
  }

  get ssimChartLines(): ChartLine[] {
    return this.buildChartLines((run) => run.ssimSeries);
  }

  toggleSort(): void {
    this.sortOption = this.sortOption === 'newest' ? 'oldest' : 'newest';
  }

  selectExperiment(experiment: ExperimentResult): void {
    this.selectedExperiment = experiment;
  }

  hasFailures(experiment: ExperimentResult): boolean {
    return experiment.codecRuns.some((run) => !run.success);
  }

  private groupIntoExperiments(
    resultsWithFrames: ResultWithFrames[],
    config: InfrastructureConfig | undefined,
  ): ExperimentResult[] {
    const groups = new Map<string, ResultWithFrames[]>();

    for (const entry of resultsWithFrames) {
      const key = `${entry.result.batchId ?? entry.result.experimentId}::${entry.result.videoFileId ?? 'na'}`;
      const group = groups.get(key) ?? [];
      group.push(entry);
      groups.set(key, group);
    }

    return Array.from(groups.values()).map((group) => this.toExperimentResult(group, config));
  }

  private toExperimentResult(
    group: ResultWithFrames[],
    config: InfrastructureConfig | undefined,
  ): ExperimentResult {
    const first = group[0].result;
    const videoFile = config?.sequences
      .flatMap((sequence) => sequence.videoFiles)
      .find((file) => file.id === first.videoFileId);
    const sequenceName = videoFile?.name ?? first.sequenceCode ?? 'Unknown sequence';

    const codecRuns = group.map((entry, index) => this.toCodecRun(entry, config, index));

    return {
      id: `${first.batchId ?? first.experimentId}::${first.videoFileId ?? 'na'}`,
      title: first.experimentName ?? `Experiment ${first.experimentId}`,
      name: sequenceName,
      date: this.formatDate(first.createdAt),
      codecsLabel: codecRuns.map((run) => run.codecName).join(', '),
      codecRuns,
    };
  }

  private toCodecRun(entry: ResultWithFrames, config: InfrastructureConfig | undefined, index: number): CodecRun {
    const { result, frames } = entry;
    const codecName = config?.codecs.find((codec) => codec.id === result.codecId)?.name ?? 'Unknown codec';

    return {
      codecName,
      color: LINE_COLORS[index % LINE_COLORS.length],
      success: result.success,
      failureReason: result.failureReason,
      frameCount: result.frameCount,
      psnrSummary: this.buildSummary(result.psnrAverage, (value) => `${value.toFixed(2)} dB`),
      ssimSummary: this.buildSummary(result.ssimAverage, (value) => value.toFixed(3)),
      psnrSeries: frames?.psnr?.combined ?? [],
      ssimSeries: frames?.ssim?.combined ?? [],
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


  private buildChartLines(seriesOf: (run: CodecRun) => number[]): ChartLine[] {
    const runs = this.selectedExperiment?.codecRuns ?? [];
    const allValues = runs.flatMap(seriesOf);

    if (allValues.length === 0) {
      return [];
    }

    const min = Math.min(...allValues);
    const max = Math.max(...allValues);
    const padding = (max - min) * 0.15 || Math.abs(max) * 0.05 || 1;

    return runs.map((run) => ({
      codecName: run.codecName,
      color: run.color,
      path: this.buildPath(seriesOf(run), min - padding, max + padding),
    }));
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
        const y = height - padding - ((value - explicitMin) / range) * (height - padding * 2);
        return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
      })
      .join(' ');
  }
}

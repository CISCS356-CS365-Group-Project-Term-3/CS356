import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';

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
  psnrSummary: MetricSummary[];
  ssimSummary: MetricSummary[];
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
export class ResultsPage {
  readonly chartWidth = 500;
  readonly chartHeight = 200;
  readonly chartPadding = 24;

  readonly experimentHistory: ExperimentResult[] = [
    {
      id: 3,
      title: 'Experiment 3',
      name: 'foreman_cif.y4m',
      date: '2026-06-26 16:10',
      codec: 'H.264 / AVC',
      sequence: 'foreman_cif.y4m',
      frameCount: 120,
      psnrSummary: [
        { label: 'Y', value: '38.50 dB', hint: 'Luma' },
        { label: 'U', value: '40.10 dB', hint: 'Chrominance' },
        { label: 'V', value: '39.80 dB', hint: 'Chrominance' },
        { label: 'All', value: '39.45 dB', hint: 'Overall' },
      ],
      ssimSummary: [
        { label: 'Y', value: '0.962', hint: 'Luma' },
        { label: 'U', value: '0.948', hint: 'Chrominance' },
        { label: 'V', value: '0.951', hint: 'Chrominance' },
        { label: 'All', value: '0.957', hint: 'Overall' },
      ],
      // Micro-variations around 39.4
      psnrSeries: [39.4, 39.5, 39.4, 39.3, 39.4, 39.6, 39.5, 39.4, 39.3, 39.4, 39.5, 39.4],
      // Micro-variations around 0.95
      ssimSeries: [0.956, 0.957, 0.956, 0.955, 0.956, 0.958, 0.957, 0.956, 0.955, 0.957, 0.956, 0.956],
    },
    {
      id: 2,
      title: 'Experiment 2',
      name: 'coastguard_qcif_mono.y4m',
      date: '2026-06-25 11:05',
      codec: 'H.265 / HEVC',
      sequence: 'coastguard_qcif_mono.y4m',
      frameCount: 96,
      psnrSummary: [
        { label: 'Y', value: '36.21 dB', hint: 'Luma' },
        { label: 'U', value: '37.64 dB', hint: 'Chrominance' },
        { label: 'V', value: '36.98 dB', hint: 'Chrominance' },
        { label: 'All', value: '36.94 dB', hint: 'Overall' },
      ],
      ssimSummary: [
        { label: 'Y', value: '0.948', hint: 'Luma' },
        { label: 'U', value: '0.934', hint: 'Chrominance' },
        { label: 'V', value: '0.939', hint: 'Chrominance' },
        { label: 'All', value: '0.941', hint: 'Overall' },
      ],
      // Micro-variations around 36.9
      psnrSeries: [36.9, 37.0, 36.9, 36.8, 36.9, 37.1, 37.0, 36.9, 36.8, 37.0, 36.9, 36.9],
      // Micro-variations around 0.94
      ssimSeries: [0.941, 0.942, 0.941, 0.940, 0.941, 0.943, 0.942, 0.941, 0.940, 0.942, 0.941, 0.941],
    },
    {
      id: 1,
      title: 'Experiment 1',
      name: 'mobile_sif.y4m',
      date: '2026-06-23 09:40',
      codec: 'H.264 / AVC',
      sequence: 'mobile_sif.y4m',
      frameCount: 88,
      psnrSummary: [
        { label: 'Y', value: '34.76 dB', hint: 'Luma' },
        { label: 'U', value: '35.62 dB', hint: 'Chrominance' },
        { label: 'V', value: '35.18 dB', hint: 'Chrominance' },
        { label: 'All', value: '35.18 dB', hint: 'Overall' },
      ],
      ssimSummary: [
        { label: 'Y', value: '0.931', hint: 'Luma' },
        { label: 'U', value: '0.915', hint: 'Chrominance' },
        { label: 'V', value: '0.919', hint: 'Chrominance' },
        { label: 'All', value: '0.922', hint: 'Overall' },
      ],
      // Micro-variations around 35.1
      psnrSeries: [35.1, 35.2, 35.1, 35.0, 35.1, 35.3, 35.2, 35.1, 35.0, 35.2, 35.1, 35.1],
      // Micro-variations around 0.92
      ssimSeries: [0.922, 0.923, 0.922, 0.921, 0.922, 0.924, 0.923, 0.922, 0.921, 0.923, 0.922, 0.922],
    },
  ];

  sortOption: 'newest' | 'oldest' = 'newest';
  showFilters = false;

  selectedExperiment = this.experimentHistory[0];

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

  toggleSort(): void {
    this.sortOption = this.sortOption === 'newest' ? 'oldest' : 'newest';
  }

  selectExperiment(experiment: ExperimentResult): void {
    this.selectedExperiment = experiment;
  }

  get psnrPath(): string {
    // For PSNR, expect values generally between 30 and 45.
    // Setting a fixed window size of 10dB contextually scales tiny ripples perfectly.
    const average = this.selectedExperiment.psnrSeries.reduce((a, b) => a + b, 0) / this.selectedExperiment.psnrSeries.length;
    return this.buildPath(this.selectedExperiment.psnrSeries, average - 5, average + 5);
  }

  get ssimPath(): string {
    // For SSIM, max is 1.0. We give it a small visual window range of 0.1 total 
    // to keep the line flat near the top half.
    const average = this.selectedExperiment.ssimSeries.reduce((a, b) => a + b, 0) / this.selectedExperiment.ssimSeries.length;
    return this.buildPath(this.selectedExperiment.ssimSeries, average - 0.05, average + 0.05);
  }

  private parseDate(value: string): number {
    return Date.parse(value.replace(' ', 'T'));
  }

  private buildPath(values: number[], explicitMin: number, explicitMax: number): string {
    const width = this.chartWidth;
    const height = this.chartHeight;
    const padding = this.chartPadding;
    const range = explicitMax - explicitMin || 1;

    return values
      .map((value, index) => {
        const x = padding + (index / (values.length - 1)) * (width - padding * 2);
        // Standardize Y mapping to the explicit data window bounds
        const y = height - padding - ((value - explicitMin) / range) * (height - padding * 2);
        return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
      })
      .join(' ');
  }
}
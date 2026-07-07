import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

import { UiOptionsService } from '../services/ui-options.service';
import { AddDatasetDialogComponent } from './add-dataset-dialog/add-dataset-dialog.component';

interface DatasetCard {

  id: number;

  name: string;

  description: string;

  active: number;

  supported: number;
  thumbnail: string;
  videoName: string;
  filepath: string;
  width: number;
  height: number;
  fps: number;
  bitDepth: number;
  gamut: string;

}

@Component({
  selector: 'app-infrastructure-datasets',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatDialogModule,
    MatIconModule,
    MatInputModule,
    MatFormFieldModule,
    MatSnackBarModule
  ],
  templateUrl: './infrastructure-datasets.html',
  styleUrls: ['./infrastructure-datasets.scss']
})

export class InfrastructureDatasetsComponent implements OnInit {

  searchText = '';
  datasets: DatasetCard[] = [];
  filteredDatasets: DatasetCard[] = [];
  selectedDataset?: DatasetCard;
  private datasetOrder: number[] = [];

  constructor(

    private uiOptionsService: UiOptionsService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadDatasets();
  }

  onImageError(event: Event): void {
    const image = event.target as HTMLImageElement;
    image.src = 'assets/dataset-images/image.png';
  }

  loadDatasets(order?: number[]): void {

    const orderToApply = order && order.length ? order : this.datasetOrder;
    this.uiOptionsService.getUiOptions().subscribe({

      next: (data) => {
        this.datasets = (data.sequences ?? []).map((sequence: any) => {
          const video = sequence.video_files?.[0];
          return {
            id: sequence.id,
            name: sequence.name,
            description: sequence.description,
            active: sequence.active,
            supported: sequence.supported,
            thumbnail: `assets/dataset-images/${sequence.name}.png`,
            videoName: video?.name ?? '',
            filepath: video?.filepath ?? '',
            width: video?.spacial?.[0] ?? 0,
            height: video?.spacial?.[1] ?? 0,
            fps: video?.temporal ?? 0,
            bitDepth: video?.depth ?? 0,
            gamut: video?.gamut ?? ''
          };

        });

        if (orderToApply && orderToApply.length) {
          const orderIndex = new Map<number, number>();
          orderToApply.forEach((id, index) => orderIndex.set(id, index));
          this.datasets.sort((a, b) => {
            const aIndex = orderIndex.has(a.id) ? orderIndex.get(a.id)! : Number.MAX_SAFE_INTEGER;
            const bIndex = orderIndex.has(b.id) ? orderIndex.get(b.id)! : Number.MAX_SAFE_INTEGER;
            return aIndex - bIndex;
          });
        }
        this.datasetOrder = this.datasets.map(dataset => dataset.id);
        this.filteredDatasets = [...this.datasets];

      },

      error: () => {
        this.snackBar.open(
          'Failed to load datasets.',
          'Close',
          {
            duration: 3000
          }
        );
      }
    });
  }

  filterDatasets(): void {

    const search = this.searchText.toLowerCase().trim();
    this.filteredDatasets = this.datasets.filter(dataset =>
      dataset.name.toLowerCase().includes(search) ||
      dataset.description.toLowerCase().includes(search)
    );

  }
  selectDataset(dataset: DatasetCard): void {
    this.selectedDataset = dataset;
  }

  trackByDataset(_: number, dataset: DatasetCard): number {
    return dataset.id;
  }

  addDataset(): void {
    const dialogRef = this.dialog.open(
      AddDatasetDialogComponent,
      {
        width: '600px'
      }
    );

    dialogRef.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }

      this.uiOptionsService.addSequence({
        name: result.name,
        description: result.description
      }).subscribe({

        next: () => {
          this.uiOptionsService.getUiOptions().subscribe({
            next: data => {
              const matches = (data.sequences ?? []).filter((seq: any) =>
                seq.name === result.name && seq.description === result.description
              );

              const sequence = matches.sort((a: any, b: any) => b.id - a.id)[0];
              if (!sequence) {
                this.snackBar.open(
                  'Dataset created, but sequence not found for video file creation.',
                  'Close',
                  { duration: 4000 }
                );
                this.loadDatasets();
                return;
              }
              const videoPayload = {
                sequence_id: sequence.id.toString(),
                name: result.video_file.name,
                filepath: result.video_file.filepath,
                spacial: result.video_file.spacial,

                temporal: result.video_file.temporal,

                depth: result.video_file.depth,

                quality: result.video_file.quality,

                gamut: result.video_file.gamut

              };

              this.uiOptionsService.addVideoFile(videoPayload).subscribe({

                next: () => {
                  this.loadDatasets();
                  this.snackBar.open(
                    'Dataset added.',
                    'Close',
                    {
                      duration: 3000
                    }
                  );

                },

                error: () => {

                  this.snackBar.open(
                    'Dataset added, but failed to add video file.',
                    'Close',
                    {
                      duration: 4500
                    }

                  );
                  this.loadDatasets();
                }
              });

            },

            error: () => {
              this.snackBar.open(
                'Dataset added, but failed to verify sequence.',
                'Close',

                {
                  duration: 4000
                }

              );
              this.loadDatasets();
            }

          });

        },

        error: () => {
          this.snackBar.open(
            'Unable to add dataset.',
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

    if (!this.selectedDataset) {
      this.snackBar.open(
        'Please select a dataset.',
        'Close',

        {
          duration: 3000
        }

      );

      return;

    }
    if (!this.selectedDataset.supported) {
      this.snackBar.open(
        'This dataset is not currently supported by the Experiments Engine.',
        'Close',
        {
          duration: 4000
        }

      );

      return;

    }

    const currentOrder = this.datasets.map(dataset => dataset.id);

    this.uiOptionsService.toggleSequence({
      id: this.selectedDataset.id,
      active: 1

    }).subscribe({

      next: () => {

        this.loadDatasets(currentOrder);
        this.snackBar.open(
          'Dataset enabled.',
          'Close',
          {
            duration: 3000
          }

        );
      }
    });

  }

  disableSelected(): void {

    if (!this.selectedDataset) {
      this.snackBar.open(
        'Please select a dataset.',
        'Close',
        {
          duration: 3000
        }

      );

      return;

    }
    const currentOrder = this.datasets.map(dataset => dataset.id);

    this.uiOptionsService.toggleSequence({
      id: this.selectedDataset.id,
      active: 0

    }).subscribe({

      next: () => {

        this.loadDatasets(currentOrder);

        this.snackBar.open(
          'Dataset disabled.',
          'Close',

          {
            duration: 3000
          }

        );

      }

    });

  }

}

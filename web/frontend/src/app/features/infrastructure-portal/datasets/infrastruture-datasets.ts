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
//import { AddDatasetDialogComponent } from './add-dataset-dialog/add-dataset-dialog';

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

    image.src = 'assets/dataset-images/default.png';

  }

  loadDatasets(): void {

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

  // addDataset(): void {
  //
  //   const dialogRef = this.dialog.open(
  //
  //     AddDatasetDialogComponent,
  //
  //     {
  //
  //       width: '600px'
  //
  //     }
  //
  //   );
  //
  //   dialogRef.afterClosed().subscribe(result => {
  //
  //     if (!result) {
  //
  //       return;
  //
  //     }
  //
  //     this.uiOptionsService.addSequence({
  //
  //       ...result,
  //
  //       active: 0,
  //
  //       supported: 0
  //
  //     }).subscribe({
  //
  //       next: () => {
  //
  //         this.loadDatasets();
  //
  //         this.snackBar.open(
  //
  //           'Dataset added.',
  //
  //           'Close',
  //
  //           {
  //
  //             duration: 3000
  //
  //           }
  //
  //         );
  //
  //       },
  //
  //       error: () => {
  //
  //         this.snackBar.open(
  //
  //           'Unable to add dataset.',
  //
  //           'Close',
  //
  //           {
  //
  //             duration: 3000
  //
  //           }
  //
  //         );
  //
  //       }
  //
  //     });
  //
  //   });
  //
  // }

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

    this.uiOptionsService.toggleSequence({

      id: this.selectedDataset.id,

      active: 1

    }).subscribe({

      next: () => {

        this.loadDatasets();

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

    this.uiOptionsService.toggleSequence({

      id: this.selectedDataset.id,

      active: 0

    }).subscribe({

      next: () => {

        this.loadDatasets();

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

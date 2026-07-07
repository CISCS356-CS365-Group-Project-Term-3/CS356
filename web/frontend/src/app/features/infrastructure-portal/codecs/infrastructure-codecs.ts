import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { AgGridAngular } from 'ag-grid-angular';

import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridReadyEvent,
  ModuleRegistry,
  SelectionChangedEvent,
  RowClassParams
} from 'ag-grid-community';

import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSnackBarModule } from '@angular/material/snack-bar';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';

import { UiOptionsService } from '../services/ui-options.service';
import { AddCodecDialogComponent } from './add-codec-dialog/add-codec-dialog.component';

ModuleRegistry.registerModules([AllCommunityModule]);

interface CodecRow {

  id: number;

  name: string;

  version: string | null;

  active: number;

  encoder_type_id: number;

  supported: boolean;

}

@Component({
  selector: 'app-infrastructure-codecs',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    AgGridAngular,
    MatCardModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatSnackBarModule,
  ],
  templateUrl: './infrastructure-codecs.html',
  styleUrls: ['./infrastructure-codecs.scss'],
})
export class InfrastructureCodecsComponent implements OnInit {

  searchText = '';

  rowData: CodecRow[] = [];

  selectedCodec?: CodecRow;

  readonly supportedCodecs = [
    'h261',
    'h263',
    'h264',
    'h265'
  ];

  columnDefs: ColDef<CodecRow>[] = [

    {
      field: 'id',
      headerName: 'ID',
      width: 90
    },

    {
      field: 'name',
      headerName: 'Codec',
      flex: 1,
      minWidth: 260
    },

    {
      field: 'supported',
      headerName: 'Supported?',
      width: 150,

      valueFormatter: params =>
        params.value ? 'Yes' : 'No'
    },

    {
      field: 'active',
      headerName: 'Status',
      width: 150,

      valueFormatter: params =>
        params.value === 1
          ? 'Active'
          : 'Inactive'
    }

  ];

  defaultColDef: ColDef = {

    sortable: true,
    filter: true,
    resizable: true

  };

  rowClassRules = {

    'row-active': (params: RowClassParams<CodecRow>) =>
      !!params.data &&
      params.data.supported &&
      params.data.active === 1,

    'row-inactive': (params: RowClassParams<CodecRow>) =>
      !!params.data &&
      params.data.supported &&
      params.data.active === 0,

    'row-unsupported': (params: RowClassParams<CodecRow>) =>
      !!params.data &&
      !params.data.supported

  };

  constructor(

    private uiOptionsService: UiOptionsService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar

  ) {}

  ngOnInit(): void {

    this.loadCodecs();

  }

  loadCodecs(): void {

    this.uiOptionsService.getUiOptions().subscribe({

      next: data => {
        this.rowData = (data.codecs ?? []).map((codec: any) => ({
          id: codec.id,
          name: codec.name,
          active: codec.active,
          encoder_type_id: codec.encoder_type_id,
          supported: this.supportedCodecs.includes(codec.name)

        }));

      },

      error: () => {

        this.snackBar.open(
          'Failed to load codecs.',
          'Close',
          {
            duration: 3000
          }

        );
      }
    });

  }

  onGridReady(params: GridReadyEvent<CodecRow>): void {

    params.api.sizeColumnsToFit();

  }

  onSelectionChanged(

    event: SelectionChangedEvent<CodecRow>

  ): void {
    const rows = event.api.getSelectedRows();

    this.selectedCodec = rows.length? rows[0]: undefined;
  }

  addCodec(): void {

    const dialogRef = this.dialog.open(
      AddCodecDialogComponent,

      {
        width: '520px'
      }

    );

    dialogRef.afterClosed().subscribe(result => {

      if (!result) {
        return;

      }

      const duplicate = this.rowData.some(codec =>

        codec.name.trim().toLowerCase() ===
        result.name.trim().toLowerCase()

      );

      if (duplicate) {

        this.snackBar.open(

          'A codec with this name already exists.',

          'Close',

          {
            duration: 3500
          }

        );
        return;
      }


      // Need to provide an encoder_type_id to the backend. Prefer the
      // "Standard Encoder" type if present, otherwise fall back to the
      // first available encoder type. This keeps the change frontend-only.
      this.uiOptionsService.getUiOptions().subscribe({

        next: (data) => {

          const encoderTypes = data.encoder_types ?? [];

          let encoderTypeId: number | undefined;

          const standard = encoderTypes.find((e: any) => e.name === 'Standard Encoder');

          if (standard) {
            encoderTypeId = standard.id;
          } else if (encoderTypes.length > 0) {
            encoderTypeId = encoderTypes[0].id;
          }

          if (!encoderTypeId) {
            this.snackBar.open(
              'No encoder types available. Add an encoder type first.',
              'Close',
              { duration: 4000 }
            );

            return;
          }

          const payload: any = {
            name: result.name.trim(),
            version: result.version,
            active: 0,
            encoder_type_id: encoderTypeId
          };

          this.uiOptionsService.addCodec(payload).subscribe({

        next: () => {

          this.snackBar.open(

            'Codec added.',

            'Close',

            {
              duration: 3000
            }
          );

          this.loadCodecs();

        },


            error: () => {

              this.snackBar.open(

                'Failed to add codec.',

                'Close',

                {

                  duration: 3000

                }

              );

            }

          });

        },

        error: () => {

          this.snackBar.open(

            'Failed to fetch encoder types required to add codec.',

            'Close',

            {

              duration: 3500

            }

          );

        }

      });

    });

  }

  enableSelected(): void {

    if (!this.selectedCodec) {

      this.snackBar.open(
        'Please select a codec.',
        'Close',
        {
          duration: 3000
        }
      );

      return;

    }

    // Only engine-supported codecs can be enabled
    if (!this.selectedCodec.supported) {

      this.snackBar.open(
        'This codec is not currently supported by the Experiments Engine.',
        'Close',
        {
          duration: 4000
        }
      );

      return;

    }

    this.uiOptionsService
      .toggleCodec(
        this.selectedCodec.id,
        1
      )
      .subscribe({

        next: () => {

          this.loadCodecs();

          this.snackBar.open(
            'Codec enabled.',
            'Close',
            {
              duration: 3000
            }
          );

        },

        error: () => {

          this.snackBar.open(
            'Unable to enable codec.',
            'Close',
            {
              duration: 3000
            }
          );

        }

      });

  }

  disableSelected(): void {

    if (!this.selectedCodec) {

      this.snackBar.open(
        'Please select a codec.',
        'Close',
        {
          duration: 3000
        }
      );

      return;

    }

    this.uiOptionsService
      .toggleCodec(
        this.selectedCodec.id,
        0
      )
      .subscribe({

        next: () => {

          this.loadCodecs();

          this.snackBar.open(
            'Codec disabled.',
            'Close',
            {
              duration: 3000
            }
          );

        },

        error: () => {

          this.snackBar.open(
            'Unable to disable codec.',
            'Close',
            {
              duration: 3000
            }
          );

        }

      });

  }

}

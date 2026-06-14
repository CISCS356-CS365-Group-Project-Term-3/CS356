import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { Sequence, VideoFile } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-sequences',
  imports: [MatCardModule, MatFormFieldModule, MatSelectModule, FormsModule],
  templateUrl: './sequences.html',
  styleUrl: './sequences.scss',
})
export class SequencesStep implements OnInit {
  sequences: Sequence[] = [];
  selectedFileIds: number[] = [];

  constructor(
    private infrastructureService: InfrastructureService,
    public formService: NewExperimentFormService,
  ) {}

  ngOnInit(): void {
    this.infrastructureService.getConfig().subscribe((data) => {
      this.sequences = data.sequences;
      this.selectedFileIds = this.formService.form.sequences.map((s) => s.videoFileId);
    });
  }

  onFileSelectionChange(selectedIds: number[]): void {
    for (const id of selectedIds) {
      if (!this.formService.form.sequences.some((s) => s.videoFileId === id)) {
        this.formService.form.sequences.push({ videoFileId: id });
      }
    }
    this.formService.form.sequences = this.formService.form.sequences.filter((s) =>
      selectedIds.includes(s.videoFileId),
    );
  }

  getFile(fileId: number): VideoFile | undefined {
    for (const seq of this.sequences) {
      const file = seq.videoFiles.find((f) => f.id === fileId);
      if (file) return file;
    }
    return undefined;
  }

  getSequenceName(fileId: number): string {
    return this.sequences.find((s) => s.videoFiles.some((f) => f.id === fileId))?.name ?? '—';
  }

  getFileLabel(file: VideoFile): string {
    return `${file.spacial[0]}x${file.spacial[1]} · ${file.temporal}fps · ${file.depth}bit`;
  }
}

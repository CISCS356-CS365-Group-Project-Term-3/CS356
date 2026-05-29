import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import {
  DepthOption,
  FrameRate,
  GamutOption,
  QualityOption,
  Resolution,
  VideoFile,
} from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { NewExperimentFormService, SequenceConfig } from '../../new-experiment-form.service';

@Component({
  selector: 'app-sequences',
  imports: [MatCardModule, MatFormFieldModule, MatSelectModule, FormsModule],
  templateUrl: './sequences.html',
  styleUrl: './sequences.scss',
})
export class SequencesStep implements OnInit {
  videoFiles: VideoFile[] = [];
  resolutions: Resolution[] = [];
  frameRates: FrameRate[] = [];
  quality: QualityOption[] = [];
  depth: DepthOption[] = [];
  gamut: GamutOption[] = [];

  constructor(
    private infrastructureService: InfrastructureService,
    public formService: NewExperimentFormService,
  ) {}

  ngOnInit(): void {
    this.infrastructureService.getConfig().subscribe((data) => {
      this.videoFiles = data.videoFiles;
      this.resolutions = data.resolutions;
      this.frameRates = data.frameRates;
      this.quality = data.quality;
      this.depth = data.depth;
      this.gamut = data.gamut;
      this.selectedFileIds = this.formService.form.sequences.map((s) => s.videoFileId);
    });
  }

  get hasIncompleteSequences(): boolean {
    return this.formService.form.sequences.some(
      (s) => s.resolutionId === null || s.frameRateId === null || s.qualityId === null,
    );
  }

  selectedFileIds: number[] = [];

  onFileSelectionChange(selectedIds: number[]): void {
    for (const id of selectedIds) {
      if (!this.formService.form.sequences.some((s) => s.videoFileId === id)) {
        const file = this.videoFiles.find((f) => f.id === id)!;
        this.formService.form.sequences.push({
          videoFileId: id,
          resolutionId: file.availableSpatials.length === 1 ? file.availableSpatials[0] : null,
          frameRateId: file.availableTemporals.length === 1 ? file.availableTemporals[0] : null,
          qualityId: null,
          depthId: file.availableDepths[0] ?? null,
          gamutId: this.gamut[0]?.id ?? null,
        });
      }
    }
    this.formService.form.sequences = this.formService.form.sequences.filter((s) =>
      selectedIds.includes(s.videoFileId),
    );
  }

  getFile(fileId: number): VideoFile | undefined {
    return this.videoFiles.find((f) => f.id === fileId);
  }

  getResolutionOptions(fileId: number): Resolution[] {
    const file = this.getFile(fileId);
    if (!file) return [];
    return this.resolutions.filter((r) => file.availableSpatials.includes(r.id));
  }

  getFrameRateOptions(fileId: number): FrameRate[] {
    const file = this.getFile(fileId);
    if (!file) return [];
    return this.frameRates.filter((fr) => file.availableTemporals.includes(fr.id));
  }

  getDepthOptions(fileId: number): DepthOption[] {
    const file = this.getFile(fileId);
    if (!file) return [];
    return this.depth.filter((d) => file.availableDepths.includes(d.id));
  }
}

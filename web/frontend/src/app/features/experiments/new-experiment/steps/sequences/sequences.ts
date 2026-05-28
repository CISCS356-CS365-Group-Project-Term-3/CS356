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
      this.videoFiles = data.video_files;
      this.resolutions = data.resolutions;
      this.frameRates = data.frame_rates;
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
          resolutionId: file.available_spatials.length === 1 ? file.available_spatials[0] : null,
          frameRateId: file.available_temporals.length === 1 ? file.available_temporals[0] : null,
          qualityId: null,
          depthId: file.available_depths[0] ?? null,
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
    return this.resolutions.filter((r) => file.available_spatials.includes(r.id));
  }

  getFrameRateOptions(fileId: number): FrameRate[] {
    const file = this.getFile(fileId);
    if (!file) return [];
    return this.frameRates.filter((fr) => file.available_temporals.includes(fr.id));
  }

  getDepthOptions(fileId: number): DepthOption[] {
    const file = this.getFile(fileId);
    if (!file) return [];
    return this.depth.filter((d) => file.available_depths.includes(d.id));
  }
}

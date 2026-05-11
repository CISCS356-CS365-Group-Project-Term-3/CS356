import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { InfrastructureConfig } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { NewExperimentFormService, SequenceConfig } from '../../new-experiment-form.service';

@Component({
  selector: 'app-review',
  imports: [MatCardModule],
  templateUrl: './review.html',
  styleUrl: './review.scss',
})
export class ReviewStep implements OnInit {
  config: InfrastructureConfig | null = null;

  constructor(
    private infrastructureService: InfrastructureService,
    public formService: NewExperimentFormService,
  ) {}

  ngOnInit(): void {
    this.infrastructureService.getConfig().subscribe((data) => {
      this.config = data;
    });
  }

  get projectTypeName(): string {
    return this.config?.project_types.find((p) => p.id === this.formService.form.projectTypeId)?.name ?? '—';
  }

  get encoderTypeName(): string {
    return this.config?.encoder_types.find((e) => e.id === this.formService.form.encoderTypeId)?.name ?? '—';
  }

  get codecName(): string {
    return this.config?.codecs.find((c) => c.id === this.formService.form.codecId)?.name ?? '—';
  }

  get encoderModeName(): string {
    return this.config?.encoder_modes.find((m) => m.id === this.formService.form.encoderModeId)?.name ?? '—';
  }

  getSequenceDisplay(seq: SequenceConfig): { videoFile: string; resolution: string; frameRate: string; quality: string } {
    return {
      videoFile:  this.config?.video_files.find((f) => f.id === seq.videoFileId)?.name ?? '—',
      resolution: this.config?.resolutions.find((r) => r.id === seq.resolutionId)?.name ?? '—',
      frameRate:  this.config?.frame_rates.find((fr) => fr.id === seq.frameRateId)?.name ?? '—',
      quality:    this.config?.quality.find((q) => q.id === seq.qualityId)?.name ?? '—',
    };
  }
}

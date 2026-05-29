import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { InfrastructureConfig } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { EncoderConfig, NewExperimentFormService, SequenceConfig } from '../../new-experiment-form.service';

interface EncoderDisplay {
  type: string;
  codec: string;
  mode: string;
}

interface SequenceDisplay {
  videoFile: string;
  resolution: string;
  frameRate: string;
  quality: string;
  depth: string;
  gamut: string;
}

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
    return this.config?.projectTypes.find((p) => p.id === this.formService.form.projectTypeId)?.name ?? '—';
  }

  getEncoderDisplay(encoder: EncoderConfig): EncoderDisplay {
    return {
      type:  this.config?.encoderTypes.find((e) => e.id === encoder.encoderTypeId)?.name ?? '—',
      codec: this.config?.codecs.find((c) => c.id === encoder.codecId)?.name ?? '—',
      mode:  this.config?.encoderModes.find((m) => m.id === encoder.encoderModeId)?.name ?? '—',
    };
  }

  getSequenceDisplay(seq: SequenceConfig): SequenceDisplay {
    return {
      videoFile:  this.config?.videoFiles.find((f) => f.id === seq.videoFileId)?.name ?? '—',
      resolution: this.config?.resolutions.find((r) => r.id === seq.resolutionId)?.name ?? '—',
      frameRate:  this.config?.frameRates.find((fr) => fr.id === seq.frameRateId)?.name ?? '—',
      quality:    this.config?.quality.find((q) => q.id === seq.qualityId)?.name ?? '—',
      depth:      this.config?.depth.find((d) => d.id === seq.depthId)?.name ?? '—',
      gamut:      this.config?.gamut.find((g) => g.id === seq.gamutId)?.name ?? '—',
    };
  }
}

import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { InfrastructureConfig } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { EncoderConfig, NewExperimentFormService, SequenceConfig } from '../../new-experiment-form.service';

interface EncoderDisplay {
  type: string;
  codec: string;
}

interface SequenceDisplay {
  videoFile: string;
  resolution: string;
  frameRate: string;
  depth: string;
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
    };
  }

  get hasNetworkEmulation(): boolean {
    const net = this.formService.form.networkEmulation;
    return net.packetLoss.length > 0 || net.delay.length > 0 || net.jitter.length > 0;
  }

  get packetLossDisplay(): string {
    const vals = this.formService.form.networkEmulation.packetLoss;
    return vals.length > 0 ? vals.map((v) => v + '%').join(', ') : '—';
  }

  get delayDisplay(): string {
    const vals = this.formService.form.networkEmulation.delay;
    return vals.length > 0 ? vals.map((v) => v + 'ms').join(', ') : '—';
  }

  get jitterDisplay(): string {
    const vals = this.formService.form.networkEmulation.jitter;
    return vals.length > 0 ? vals.map((v) => v + 'ms').join(', ') : '—';
  }

  getSequenceDisplay(seq: SequenceConfig): SequenceDisplay {
    const file = this.config?.sequences.flatMap((s) => s.videoFiles).find((f) => f.id === seq.videoFileId);
    const seqName = this.config?.sequences.find((s) => s.videoFiles.some((f) => f.id === seq.videoFileId))?.name ?? '—';
    return {
      videoFile:  file ? `${seqName} — ${file.spacial[0]}x${file.spacial[1]} · ${file.temporal}fps · ${file.depth}bit` : seqName,
      resolution: file ? `${file.spacial[0]}x${file.spacial[1]}` : '—',
      frameRate:  file ? `${file.temporal}fps` : '—',
      depth:      file ? `${file.depth}bit` : '—',
    };
  }
}

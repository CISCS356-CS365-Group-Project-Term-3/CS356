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
  standalone: true,
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
    return net.packetLoss != null || net.delay != null || net.jitter != null;
  }

  get packetLossDisplay(): string {
    const val = this.formService.form.networkEmulation.packetLoss;
    return val != null ? val + '%' : '—';
  }

  get delayDisplay(): string {
    const val = this.formService.form.networkEmulation.delay;
    return val != null ? val + 'ms' : '—';
  }

  get jitterDisplay(): string {
    const val = this.formService.form.networkEmulation.jitter;
    return val != null ? val + 'ms' : '—';
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

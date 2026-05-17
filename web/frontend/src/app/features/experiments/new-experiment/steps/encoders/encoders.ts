import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Codec, EncoderMode, EncoderType } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { EncoderConfig, NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-encoders',
  imports: [MatCardModule, MatButtonModule, MatIconModule],
  templateUrl: './encoders.html',
  styleUrl: './encoders.scss',
})
export class EncodersStep implements OnInit {
  encoderTypes: EncoderType[] = [];
  allCodecs: Codec[] = [];
  allModes: EncoderMode[] = [];

  constructor(
    private infrastructureService: InfrastructureService,
    public formService: NewExperimentFormService,
  ) {}

  ngOnInit(): void {
    this.infrastructureService.getConfig().subscribe((data) => {
      this.encoderTypes = data.encoder_types;
      this.allCodecs = data.codecs;
      this.allModes = data.encoder_modes;
    });
  }

  availableCodecs(encoder: EncoderConfig): Codec[] {
    const et = this.encoderTypes.find((e) => e.id === encoder.encoderTypeId);
    if (!et) return [];
    return this.allCodecs.filter((c) => et.active_codecs.includes(c.id));
  }

  selectEncoderType(encoder: EncoderConfig, encoderType: EncoderType): void {
    if (encoder.encoderTypeId !== encoderType.id) {
      encoder.encoderTypeId = encoderType.id;
      encoder.codecId = null;
      encoder.encoderModeId = null;
    }
  }

  selectCodec(encoder: EncoderConfig, codec: Codec): void {
    if (encoder.codecId !== codec.id) {
      encoder.codecId = codec.id;
      encoder.encoderModeId = null;
    }
  }

  selectMode(encoder: EncoderConfig, mode: EncoderMode): void {
    encoder.encoderModeId = mode.id;
  }

  addEncoder(): void {
    this.formService.form.encoders.push({ encoderTypeId: null, codecId: null, encoderModeId: null });
  }

  removeEncoder(index: number): void {
    this.formService.form.encoders.splice(index, 1);
  }
}

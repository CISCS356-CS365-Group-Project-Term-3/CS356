import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { Codec, EncoderMode, EncoderType } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { EncoderConfig, NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-encoders',
  imports: [FormsModule, MatCardModule, MatButtonModule, MatIconModule, MatFormFieldModule, MatSelectModule],
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

  onEncoderTypeChange(encoder: EncoderConfig): void {
    encoder.codecId = null;
    encoder.encoderModeId = null;
  }

  onCodecChange(encoder: EncoderConfig): void {
    encoder.encoderModeId = null;
  }

  addEncoder(): void {
    this.formService.form.encoders.push({ encoderTypeId: null, codecId: null, encoderModeId: null });
  }

  removeEncoder(index: number): void {
    this.formService.form.encoders.splice(index, 1);
  }
}

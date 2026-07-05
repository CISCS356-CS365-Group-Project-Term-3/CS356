import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { Codec, EncoderType } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { EncoderConfig, NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-encoders',
  standalone: true,
  imports: [FormsModule, MatCardModule, MatButtonModule, MatIconModule, MatFormFieldModule, MatSelectModule],
  templateUrl: './encoders.html',
  styleUrl: './encoders.scss',
})
export class EncodersStep implements OnInit {
  encoderTypes: EncoderType[] = [];
  allCodecs: Codec[] = [];
  constructor(
    private infrastructureService: InfrastructureService,
    public formService: NewExperimentFormService,
  ) {}

  ngOnInit(): void {
    this.infrastructureService.getConfig().subscribe((data) => {
      this.encoderTypes = data.encoderTypes;
      this.allCodecs = data.codecs;
    });
  }

  availableCodecs(encoder: EncoderConfig, index: number): Codec[] {
    const et = this.encoderTypes.find((e) => e.id === encoder.encoderTypeId);
    if (!et) return [];
    const base = !et.activeCodecs?.length
      ? this.allCodecs
      : this.allCodecs.filter((c) => et.activeCodecs.includes(c.id));
    const usedCodecIds = this.formService.form.encoders
      .filter((e, i) => i !== index && e.encoderTypeId === encoder.encoderTypeId && e.codecId !== null)
      .map((e) => e.codecId);
    return base.filter((c) => !usedCodecIds.includes(c.id));
  }

  onEncoderTypeChange(encoder: EncoderConfig): void {
    encoder.codecId = null;
  }

  addEncoder(): void {
    this.formService.form.encoders.push({ encoderTypeId: null, codecId: null });
  }

  removeEncoder(index: number): void {
    this.formService.form.encoders.splice(index, 1);
  }
}

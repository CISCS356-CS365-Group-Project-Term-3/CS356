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

  availableCodecs(encoder: EncoderConfig): Codec[] {
    const et = this.encoderTypes.find((e) => e.id === encoder.encoderTypeId);
    if (!et) return [];
    if (!et.activeCodecs?.length) return this.allCodecs;
    return this.allCodecs.filter((c) => et.activeCodecs.includes(c.id));
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

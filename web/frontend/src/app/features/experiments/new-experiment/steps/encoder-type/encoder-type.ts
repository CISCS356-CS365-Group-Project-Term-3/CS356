import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { EncoderType } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-encoder-type',
  imports: [MatCardModule],
  templateUrl: './encoder-type.html',
  styleUrl: './encoder-type.scss',
})
export class EncoderTypeStep implements OnInit {
  encoderTypes: EncoderType[] = [];

  encoderTypeDescriptions: Record<number, string> = {
    1: 'Single-layer encoding using traditional codecs (H.264, H.265)',
    2: 'Multi-layer scalable video coding for adaptive streaming',
  };

  constructor(
    private infrastructureService: InfrastructureService,
    public formService: NewExperimentFormService,
  ) {}

  ngOnInit(): void {
    this.infrastructureService.getConfig().subscribe((data) => {
      this.encoderTypes = data.encoder_types;
    });
  }

  select(encoderType: EncoderType): void {
    if (this.formService.form.encoderTypeId !== encoderType.id) {
      this.formService.form.encoderTypeId = encoderType.id;
      this.formService.form.codecId = null;
      this.formService.form.encoderModeId = null;
    }
  }
}

import { Component, OnInit } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { Codec, EncoderMode, EncoderType } from '../../../models/infrastructure-config.model';
import { InfrastructureService } from '../../../services/infrastructure';
import { NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-codec-mode',
  imports: [MatCardModule],
  templateUrl: './codec-mode.html',
  styleUrl: './codec-mode.scss',
})
export class CodecModeStep implements OnInit {
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

  get availableCodecs(): Codec[] {
    const encoderType = this.encoderTypes.find(
      (et) => et.id === this.formService.form.encoderTypeId,
    );
    if (!encoderType) return [];
    return this.allCodecs.filter((c) => encoderType.active_codecs.includes(c.id));
  }

  get availableModes(): EncoderMode[] {
    if (this.formService.form.codecId === null) return [];
    return this.allModes;
  }

  selectCodec(codec: Codec): void {
    if (this.formService.form.codecId !== codec.id) {
      this.formService.form.codecId = codec.id;
      this.formService.form.encoderModeId = null;
    }
  }

  selectMode(mode: EncoderMode): void {
    this.formService.form.encoderModeId = mode.id;
  }
}

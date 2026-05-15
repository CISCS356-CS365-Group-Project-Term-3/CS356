import { Component } from '@angular/core';
import { MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule } from '@angular/material/button';
import { Router, RouterLink } from '@angular/router';
import { NewExperimentFormService } from './new-experiment-form.service';
import { ProjectSetup } from './steps/project-setup/project-setup';
import { EncoderTypeStep } from './steps/encoder-type/encoder-type';
import { CodecModeStep } from './steps/codec-mode/codec-mode';
import { SequencesStep } from './steps/sequences/sequences';
import { ReviewStep } from './steps/review/review';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-new-experiment',
  imports: [
    MatStepperModule,
    MatButtonModule,
    RouterLink,
    ProjectSetup,
    EncoderTypeStep,
    CodecModeStep,
    SequencesStep,
    ReviewStep,
    MatCardModule,
    MatIconModule,
  ],
  templateUrl: './new-experiment.html',
  styleUrl: './new-experiment.scss',
})
export class NewExperiment {
  constructor(
    public formService: NewExperimentFormService,
    private router: Router,
  ) {}

  isProjectSetupComplete(): boolean {
    const form = this.formService.form;
    return form.name.trim().length > 0 && form.projectTypeId !== null;
  }

  isEncoderTypeComplete(): boolean {
    return this.formService.form.encoderTypeId !== null;
  }

  isCodecModeComplete(): boolean {
    const form = this.formService.form;
    return form.codecId !== null && form.encoderModeId !== null;
  }

  isSequencesComplete(): boolean {
    const seqs = this.formService.form.sequences;
    return (
      seqs.length > 0 &&
      seqs.every((s) => s.resolutionId !== null && s.frameRateId !== null && s.qualityId !== null)
    );
  }

  submit(): void {
    const form = this.formService.form;
    const payload = {
      name: form.name,
      project_type_id: form.projectTypeId,
      encoder_type_id: form.encoderTypeId,
      codec_id: form.codecId,
      encoder_mode_id: form.encoderModeId,
      sequences: form.sequences.map((s) => ({
        video_file_id: s.videoFileId,
        resolution_id: s.resolutionId,
        frame_rate_id: s.frameRateId,
        quality_id: s.qualityId,
        depth_id: s.depthId,
        gamut_id: s.gamutId,
      })),
    };
    console.log('Submitting experiment:', payload);
    this.router.navigate(['/experiments']);
  }

  canProceed(stepIndex: number): boolean {
    switch (stepIndex) {
      case 0:
        return this.isProjectSetupComplete();
      case 1:
        return this.isEncoderTypeComplete();
      case 2:
        return this.isCodecModeComplete();
      case 3:
        return this.isSequencesComplete();
      default:
        return true;
    }
  }
}

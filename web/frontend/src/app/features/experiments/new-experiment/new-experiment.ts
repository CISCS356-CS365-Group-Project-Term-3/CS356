import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { NewExperimentFormService } from './new-experiment-form.service';
import { ProjectSetup } from './steps/project-setup/project-setup';
import { EncodersStep } from './steps/encoders/encoders';
import { SequencesStep } from './steps/sequences/sequences';
import { ReviewStep } from './steps/review/review';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-new-experiment',
  imports: [
    MatStepperModule,
    MatButtonModule,
    ProjectSetup,
    EncodersStep,
    SequencesStep,
    ReviewStep,
    MatCardModule,
    MatIconModule,
  ],
  templateUrl: './new-experiment.html',
  styleUrl: './new-experiment.scss',
})
export class NewExperiment implements OnInit {
  @ViewChild('stepper') stepper!: MatStepper;

  constructor(
    public formService: NewExperimentFormService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.formService.applyPendingTemplate();
  }

  get isFirstStep(): boolean {
    return this.stepper?.selectedIndex === 0;
  }

  get isLastStep(): boolean {
    return this.stepper?.selectedIndex === this.stepper?.steps.length - 1;
  }

  onBack(): void {
    if (this.isFirstStep) {
      this.router.navigate(['/experiments']);
    } else {
      this.stepper.previous();
    }
  }

  onNext(): void {
    if (this.isLastStep) {
      this.submit();
    } else {
      this.stepper.next();
    }
  }

  isProjectSetupComplete(): boolean {
    const form = this.formService.form;
    return form.name.trim().length > 0 && form.projectTypeId !== null;
  }

  isEncodersComplete(): boolean {
    const encoders = this.formService.form.encoders;
    return (
      encoders.length > 0 &&
      encoders.every((e) => e.encoderTypeId !== null && e.codecId !== null && e.encoderModeId !== null)
    );
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
      status: 'draft', // change to 'finalized' when the finalize button is implemented
      project_type_id: form.projectTypeId,
      encoders: form.encoders.map((e) => ({
        encoder_type_id: e.encoderTypeId,
        codec_id: e.codecId,
        encoder_mode_id: e.encoderModeId,
      })),
      sequences: form.sequences.map((s) => ({
        video_file_id: s.videoFileId,
        resolution_id: s.resolutionId,
        frame_rate_id: s.frameRateId,
        quality_id: s.qualityId,
        depth_id: s.depthId,
        gamut_id: s.gamutId,
      })),
    };
    // this.experimentsService.createExperiment(payload).subscribe(() => {
    //   this.router.navigate(['/experiments']);
    // });
    this.router.navigate(['/experiments']);
  }

  canProceed(stepIndex: number): boolean {
    switch (stepIndex) {
      case 0:
        return this.isProjectSetupComplete();
      case 1:
        return this.isEncodersComplete();
      case 2:
        return this.isSequencesComplete();
      default:
        return true;
    }
  }
}

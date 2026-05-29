import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { NewExperimentFormService } from './new-experiment-form.service';
import { ExperimentsService } from '../services/experiments';
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
  submitError: string | null = null;
  showDraftModal = false;
  visitedSteps = new Set<number>();

  constructor(
    public formService: NewExperimentFormService,
    public router: Router,
    private experimentsService: ExperimentsService,
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
      if (this.isFormComplete()) {
        this.doSubmit('finalised');
      } else {
        this.showDraftModal = true;
      }
    } else {
      this.visitedSteps.add(this.stepper.selectedIndex);
      this.stepper.next();
    }
  }

  confirmDraft(): void {
    this.showDraftModal = false;
    this.doSubmit('draft');
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

  isFormComplete(): boolean {
    return this.isProjectSetupComplete() && this.isEncodersComplete() && this.isSequencesComplete();
  }

  isStepError(stepIndex: number): boolean {
    return this.visitedSteps.has(stepIndex) && !this.canProceed(stepIndex);
  }

  private doSubmit(status: string): void {
    const form = this.formService.form;
    const payload = {
      userId: 1, // TODO: replace with real user ID from JWT
      name: form.name,
      status,
      projectTypeId: form.projectTypeId,
      encoders: form.encoders.map((e) => ({
        encoderTypeId: e.encoderTypeId,
        codecId: e.codecId,
        encoderModeId: e.encoderModeId,
      })),
      sequences: form.sequences.map((s) => ({
        videoFileId: s.videoFileId,
        resolutionId: s.resolutionId,
        frameRateId: s.frameRateId,
        qualityId: s.qualityId,
        depthId: s.depthId,
        gamutId: s.gamutId,
      })),
    };
    console.log('createExperiment payload', payload);
    this.submitError = null;
    this.experimentsService.createExperiment(payload).subscribe({
      next: () => this.router.navigate(['/experiments']),
      error: () => (this.submitError = 'Failed to create experiment. Please try again.'),
    });
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

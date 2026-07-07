import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { NewExperimentFormService } from './new-experiment-form.service';
import { ExperimentsService } from '../services/experiments';
import { InfrastructureService } from '../services/infrastructure';
import { ProjectSetup } from './steps/project-setup/project-setup';
import { EncodersStep } from './steps/encoders/encoders';
import { SequencesStep } from './steps/sequences/sequences';
import { ReviewStep } from './steps/review/review';
import { NetworkEmulationStep } from './steps/network-emulation/network-emulation';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { UserManagementService } from '../../user_management/user-management-service';
import { InfrastructureConfig } from '../models/infrastructure-config.model';

@Component({
  selector: 'app-new-experiment',
  imports: [
    MatStepperModule,
    MatButtonModule,
    ProjectSetup,
    EncodersStep,
    SequencesStep,
    NetworkEmulationStep,
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
  isSubmitting = false;
  visitedSteps = new Set<number>();
  private userId: number | null = null;
  private config: InfrastructureConfig | null = null;

  constructor(
    public formService: NewExperimentFormService,
    public router: Router,
    private experimentsService: ExperimentsService,
    private userService: UserManagementService,
    private infrastructureService: InfrastructureService,
  ) {}

  ngOnInit(): void {
    this.formService.applyPendingTemplate();
    try {
      this.userService.getUserInfo().subscribe({
        next: (user: any) => { this.userId = user.user_id; },
        error: () => {},
      });
    } catch {}
    this.infrastructureService.getConfig().subscribe({
      next: (config) => { this.config = config; },
      error: () => {},
    });
  }

  needsNetworkConfig(): boolean {
    const projectTypeId = this.formService.form.projectTypeId;
    return !!this.config?.projectTypes.find((pt) => pt.id === projectTypeId)?.networkEnabled;
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
      this.doSubmit('finalised');
    } else {
      this.visitedSteps.add(this.stepper.selectedIndex);
      this.stepper.next();
    }
  }

  canSaveDraft(): boolean {
    return this.isProjectSetupComplete();
  }

  onSaveDraft(): void {
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
      encoders.every((e) => e.encoderTypeId !== null && e.codecId !== null)
    );
  }

  isSequencesComplete(): boolean {
    return this.formService.form.sequences.length > 0;
  }

  isFormComplete(): boolean {
    return this.isProjectSetupComplete() && this.isEncodersComplete() && this.isSequencesComplete();
  }

  isStepError(stepIndex: number): boolean {
    return this.visitedSteps.has(stepIndex) && !this.canProceed(stepIndex);
  }

  doSubmit(status: string): void {
    if (this.isSubmitting) return;
    this.isSubmitting = true;
    const form = this.formService.form;
    const editingId = this.formService.editingId;
    const net = form.networkEmulation;
    const encodePacketLoss = (v: number) => String(Math.round(v * 10)).padStart(3, '0');
    const encodeMs = (v: number) => String(Math.round(v)).padStart(3, '0');
    const networkEmulation = {
      packetLoss: net.packetLoss.length > 0 ? net.packetLoss.map(encodePacketLoss) : ['000'],
      delay: net.delay.length > 0 ? net.delay.map(encodeMs) : ['000'],
      jitter: net.jitter.length > 0 ? net.jitter.map(encodeMs) : ['000'],
    };

    const basePayload = {
      name: form.name,
      status,
      projectTypeId: form.projectTypeId,
      encoders: form.encoders.map((e) => ({
        encoderTypeId: e.encoderTypeId,
        codecId: e.codecId,
      })),
      sequences: form.sequences.map((s) => ({ videoFileId: s.videoFileId })),
      networkEmulation,
    };
    this.submitError = null;
    const request$ = editingId
      ? this.experimentsService.patchExperiment(editingId, basePayload)
      : this.experimentsService.createExperiment({ userId: this.userId, ...basePayload });
    request$.subscribe({
      next: () => this.router.navigate(['/experiments']),
      error: () => {
        this.isSubmitting = false;
        this.submitError = 'Failed to save experiment. Please try again.';
      },
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
      case 3:
        return true; // network emulation is optional
      default:
        return true;
    }
  }
}

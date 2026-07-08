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
  userInfoLoaded = false;
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
    // picks up whatever dashboard.ts stashed via setTemplate/setDraft before routing here,
    // does nothing if you just came in via "New Experiment" with nothing pending
    this.formService.applyPendingTemplate();
    try {
      this.userService.getUserInfo().subscribe({
        next: (user: any) => {
          this.userId = user.user_id;
          this.userInfoLoaded = true;
        },
        error: () => {
          this.userInfoLoaded = true;
        },
      });
    } catch {
      this.userInfoLoaded = true;
    }
    this.infrastructureService.getConfig().subscribe({
      next: (config) => {
        this.config = config;
      },
      error: () => {},
    });
  }

  // whether the current project type even shows the network emulation step,
  // driven by infra config rather than hardcoded here
  needsNetworkConfig(): boolean {
    const projectTypeId = this.formService.form.projectTypeId;
    return !!this.config?.projectTypes.find((pt) => pt.id === projectTypeId)?.networkEnabled;
  }

  get isFirstStep(): boolean {
    return this.stepper?.selectedIndex === 0;
  }

  // step count isn't fixed, network emulation only shows up for some project types
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
      // remembers which steps youve actually been on, isStepError below only
      // shows the warning triangle for steps youve visited and left incomplete
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
      encoders.length > 0 && encoders.every((e) => e.encoderTypeId !== null && e.codecId !== null)
    );
  }

  isSequencesComplete(): boolean {
    return this.formService.form.sequences.length > 0;
  }

  hasNetworkConfig(): boolean {
    const net = this.formService.form.networkEmulation;
    return net.packetLoss != null || net.delay != null || net.jitter != null;
  }

  isNetworkConfigComplete(): boolean {
    return !this.needsNetworkConfig() || this.hasNetworkConfig();
  }

  isFormComplete(): boolean {
    return (
      this.isProjectSetupComplete() &&
      this.isEncodersComplete() &&
      this.isSequencesComplete() &&
      this.isNetworkConfigComplete()
    );
  }

  // only flags a step red once yove actually been on it and left it incomplete,
  // so a fresh wizard doesnt open already covered in warning triangles
  isStepError(stepIndex: number): boolean {
    return this.visitedSteps.has(stepIndex) && !this.canProceed(stepIndex);
  }

  doSubmit(status: string): void {
    if (this.isSubmitting) return;
    this.isSubmitting = true;
    const form = this.formService.form;
    const editingId = this.formService.editingId;
    const net = form.networkEmulation;
    // packet loss goes out as tenths of a percent so it fits the engines 3 digit
    // field (22.5% -> 225), delay/jitter just get rounded and padded the same way
    const encodePacketLoss = (v: number) => String(Math.round(v * 10)).padStart(3, '0');
    const encodeMs = (v: number) => String(Math.round(v)).padStart(3, '0');
    // drafts keep the raw values so the wizard can load them back in and let you
    // keep editing, only a real submit encodes them for the backend/engine
    // still wrapped in single element arrays since thats the format the
    // backend expects, it just never gets more than one value per field now
    const networkEmulation =
      status === 'draft'
        ? {
            packetLoss: net.packetLoss != null ? [net.packetLoss] : [],
            delay: net.delay != null ? [net.delay] : [],
            jitter: net.jitter != null ? [net.jitter] : [],
          }
        : {
            packetLoss: net.packetLoss != null ? [encodePacketLoss(net.packetLoss)] : ['000'],
            delay: net.delay != null ? [encodeMs(net.delay)] : ['000'],
            jitter: net.jitter != null ? [encodeMs(net.jitter)] : ['000'],
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

  // indices line up with the steps in new-experiment.html, review step has
  // nothing of its own to validate so it just falls through to true
  canProceed(stepIndex: number): boolean {
    switch (stepIndex) {
      case 0:
        return this.isProjectSetupComplete();
      case 1:
        return this.isEncodersComplete();
      case 2:
        return this.isSequencesComplete();
      case 3:
        return this.isNetworkConfigComplete();
      default:
        return true;
    }
  }
}

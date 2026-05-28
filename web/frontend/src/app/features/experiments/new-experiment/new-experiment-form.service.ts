import { Injectable } from '@angular/core';
import { ExperimentDetail } from '../models/experiment.model';

export interface SequenceConfig {
  videoFileId: number;
  resolutionId: number | null;
  frameRateId: number | null;
  qualityId: number | null;
  depthId: number | null;
  gamutId: number | null;
}

export interface EncoderConfig {
  encoderTypeId: number | null;
  codecId: number | null;
  encoderModeId: number | null;
}

export interface NewExperimentForm {
  name: string;
  projectTypeId: number | null;
  encoders: EncoderConfig[];
  sequences: SequenceConfig[];
}

@Injectable({ providedIn: 'root' })
export class NewExperimentFormService {
  form: NewExperimentForm = this.blankForm();
  private pendingTemplate: ExperimentDetail | null = null;

  setTemplate(detail: ExperimentDetail): void {
    this.pendingTemplate = detail;
  }

  applyPendingTemplate(): void {
    if (this.pendingTemplate) {
      const template = this.pendingTemplate;
      this.form = {
        name: template.name + ' (copy)',
        projectTypeId: template.projectTypeId,
        encoders: template.encoders.map((e) => ({ ...e })),
        sequences: template.sequences.map((s) => ({ ...s })),
      };
      this.pendingTemplate = null;
    } else {
      this.form = this.blankForm();
    }
  }

  private blankForm(): NewExperimentForm {
    return {
      name: '',
      projectTypeId: null,
      encoders: [{ encoderTypeId: null, codecId: null, encoderModeId: null }],
      sequences: [],
    };
  }
}

import { Injectable } from '@angular/core';
import { Experiment } from '../models/experiment.model';

export interface SequenceConfig {
  videoFileId: number;
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
  private pendingTemplate: Experiment | null = null;

  setTemplate(detail: Experiment): void {
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

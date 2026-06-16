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

export interface NetworkEmulationConfig {
  packetLoss: number | null;
  delay: number | null;
  jitter: number | null;
}

export interface NewExperimentForm {
  name: string;
  projectTypeId: number | null;
  encoders: EncoderConfig[];
  sequences: SequenceConfig[];
  networkEmulation: NetworkEmulationConfig;
}

@Injectable({ providedIn: 'root' })
export class NewExperimentFormService {
  form: NewExperimentForm = this.blankForm();
  editingId: string | null = null;
  private pendingTemplate: Experiment | null = null;
  private pendingDraft: Experiment | null = null;

  setTemplate(detail: Experiment): void {
    this.pendingTemplate = detail;
  }

  setDraft(detail: Experiment): void {
    this.pendingDraft = detail;
  }

  applyPendingTemplate(): void {
    if (this.pendingDraft) {
      const draft = this.pendingDraft;
      this.editingId = draft.id;
      this.form = {
        name: draft.name,
        projectTypeId: draft.projectTypeId,
        encoders: draft.encoders.map((e) => ({ ...e })),
        sequences: draft.sequences.map((s) => ({ ...s })),
        networkEmulation: draft.networkEmulation
          ? { ...draft.networkEmulation }
          : { packetLoss: null, delay: null, jitter: null },
      };
      this.pendingDraft = null;
    } else if (this.pendingTemplate) {
      const template = this.pendingTemplate;
      this.editingId = null;
      this.form = {
        name: template.name + ' (copy)',
        projectTypeId: template.projectTypeId,
        encoders: template.encoders.map((e) => ({ ...e })),
        sequences: template.sequences.map((s) => ({ ...s })),
        networkEmulation: template.networkEmulation
          ? { ...template.networkEmulation }
          : { packetLoss: null, delay: null, jitter: null },
      };
      this.pendingTemplate = null;
    } else {
      this.editingId = null;
      this.form = this.blankForm();
    }
  }

  private blankForm(): NewExperimentForm {
    return {
      name: '',
      projectTypeId: null,
      encoders: [{ encoderTypeId: null, codecId: null, encoderModeId: null }],
      sequences: [],
      networkEmulation: { packetLoss: null, delay: null, jitter: null },
    };
  }
}

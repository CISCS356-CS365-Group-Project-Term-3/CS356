import { Injectable } from '@angular/core';
import { Experiment } from '../models/experiment.model';

function firstValueOrNull(values: number[]): number | null {
  return values.length > 0 ? Number(values[0]) : null;
}

function mapFirstValue(values: number[], transform: (v: number) => number): number | null {
  return values.length > 0 ? transform(Number(values[0])) : null;
}

export interface SequenceConfig {
  videoFileId: number;
}

export interface EncoderConfig {
  encoderTypeId: number | null;
  codecId: number | null;
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
      const draftData = draft.draftData ?? {
        encoders: [],
        sequences: [],
        networkEmulation: { packetLoss: [], delay: [], jitter: [] },
      };
      this.editingId = String(draft.groupID);
      this.form = {
        name: draft.name,
        projectTypeId: draft.projectTypeId,
        encoders: draftData.encoders.map((e) => ({ ...e })),
        sequences: draftData.sequences.map((s) => ({ ...s })),
        networkEmulation: draftData.networkEmulation
          ? {
              packetLoss: firstValueOrNull(draftData.networkEmulation.packetLoss),
              delay: firstValueOrNull(draftData.networkEmulation.delay),
              jitter: firstValueOrNull(draftData.networkEmulation.jitter),
            }
          : { packetLoss: null, delay: null, jitter: null },
      };
      this.pendingDraft = null;
    } else if (this.pendingTemplate) {
      const template = this.pendingTemplate;
      const draftData = template.draftData ?? {
        encoders: [],
        sequences: [],
        networkEmulation: { packetLoss: [], delay: [], jitter: [] },
      };

      const isFromFinalised = template.status !== 'draft';
      const decodePacketLoss = (v: number) => Number(v) / 10;
      const decodeMs = (v: number) => Number(v);
      this.editingId = null;
      this.form = {
        name: template.name + ' (copy)',
        projectTypeId: template.projectTypeId,
        encoders: draftData.encoders.map((e) => ({ ...e })),
        sequences: draftData.sequences.map((s) => ({ ...s })),
        networkEmulation: draftData.networkEmulation
          ? {
              packetLoss: mapFirstValue(draftData.networkEmulation.packetLoss, (v) =>
                isFromFinalised ? decodePacketLoss(v) : v,
              ),
              delay: mapFirstValue(draftData.networkEmulation.delay, (v) =>
                isFromFinalised ? decodeMs(v) : v,
              ),
              jitter: mapFirstValue(draftData.networkEmulation.jitter, (v) =>
                isFromFinalised ? decodeMs(v) : v,
              ),
            }
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
      encoders: [{ encoderTypeId: null, codecId: null }],
      sequences: [],
      networkEmulation: { packetLoss: null, delay: null, jitter: null },
    };
  }
}

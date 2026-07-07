import { Injectable } from '@angular/core';
import { Experiment, ExperimentRun } from '../models/experiment.model';

export interface SequenceConfig {
  videoFileId: number;
}

export interface EncoderConfig {
  encoderTypeId: number | null;
  codecId: number | null;
}

export interface NetworkEmulationConfig {
  packetLoss: number[];
  delay: number[];
  jitter: number[];
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
      const draftData = draft.draftData ?? { encoders: [], sequences: [], networkEmulation: { packetLoss: [], delay: [], jitter: [] } };
      this.editingId = String(draft.groupID);
      this.form = {
        name: draft.name,
        projectTypeId: draft.projectTypeId,
        encoders: draftData.encoders.map((e) => ({ ...e })),
        sequences: draftData.sequences.map((s) => ({ ...s })),
        networkEmulation: draftData.networkEmulation
          ? { packetLoss: [...draftData.networkEmulation.packetLoss], delay: [...draftData.networkEmulation.delay], jitter: [...draftData.networkEmulation.jitter] }
          : { packetLoss: [], delay: [], jitter: [] },
      };
      this.pendingDraft = null;
    } else if (this.pendingTemplate) {
      const template = this.pendingTemplate;
      const draftData = template.draftData ?? this.deriveFromRuns(template.runs ?? []);
      this.editingId = null;
      this.form = {
        name: template.name + ' (copy)',
        projectTypeId: template.projectTypeId,
        encoders: draftData.encoders.map((e) => ({ ...e })),
        sequences: draftData.sequences.map((s) => ({ ...s })),
        networkEmulation: draftData.networkEmulation
          ? { packetLoss: [...draftData.networkEmulation.packetLoss], delay: [...draftData.networkEmulation.delay], jitter: [...draftData.networkEmulation.jitter] }
          : { packetLoss: [], delay: [], jitter: [] },
      };
      this.pendingTemplate = null;
    } else {
      this.editingId = null;
      this.form = this.blankForm();
    }
  }

  private deriveFromRuns(runs: ExperimentRun[]): {
    encoders: EncoderConfig[];
    sequences: SequenceConfig[];
    networkEmulation: NetworkEmulationConfig;
  } {
    const encoders: EncoderConfig[] = [];
    const seenEncoders = new Set<string>();
    const sequences: SequenceConfig[] = [];
    const seenSequences = new Set<number>();
    const packetLoss = new Set<number>();
    const delay = new Set<number>();
    const jitter = new Set<number>();

    for (const run of runs) {
      const e = run.encoderData;
      if (e?.encoderTypeId != null && e?.codecId != null) {
        const key = `${e.encoderTypeId}-${e.codecId}`;
        if (!seenEncoders.has(key)) {
          seenEncoders.add(key);
          encoders.push({ encoderTypeId: e.encoderTypeId, codecId: e.codecId });
        }
      }

      const videoFileId = run.sequenceData?.videoFileId;
      if (videoFileId != null && !seenSequences.has(videoFileId)) {
        seenSequences.add(videoFileId);
        sequences.push({ videoFileId });
      }

      const n = run.networkData;
      if (n?.packetLoss != null) packetLoss.add(Number(n.packetLoss) / 10);
      if (n?.delay != null) delay.add(Number(n.delay));
      if (n?.jitter != null) jitter.add(Number(n.jitter));
    }

    return {
      encoders,
      sequences,
      networkEmulation: {
        packetLoss: [...packetLoss],
        delay: [...delay],
        jitter: [...jitter],
      },
    };
  }

  private blankForm(): NewExperimentForm {
    return {
      name: '',
      projectTypeId: null,
      encoders: [{ encoderTypeId: null, codecId: null }],
      sequences: [],
      networkEmulation: { packetLoss: [], delay: [], jitter: [] },
    };
  }
}

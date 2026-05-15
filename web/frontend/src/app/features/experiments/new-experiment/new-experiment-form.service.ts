import { Injectable } from '@angular/core';

export interface SequenceConfig {
  videoFileId: number;
  resolutionId: number | null;
  frameRateId: number | null;
  qualityId: number | null;
  depthId: number | null;
  gamutId: number | null;
}

export interface NewExperimentForm {
  name: string;
  projectTypeId: number | null;
  encoderTypeId: number | null;
  codecId: number | null;
  encoderModeId: number | null;
  sequences: SequenceConfig[];
}

@Injectable({ providedIn: 'root' })
export class NewExperimentFormService {
  form: NewExperimentForm = {
    name: '',
    projectTypeId: null,
    encoderTypeId: null,
    codecId: null,
    encoderModeId: null,
    sequences: [],
  };
}

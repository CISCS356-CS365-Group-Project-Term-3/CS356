export type ExperimentStatus = 'Complete' | 'Running' | 'Failed';

export interface Experiment {
  id: string;
  name: string;
  codec: string;
  sequences: string;
  date: string;
  status: ExperimentStatus;
}

export interface ExperimentDetail {
  id: string;
  name: string;
  projectTypeId: number;
  encoders: { encoderTypeId: number; codecId: number; encoderModeId: number }[];
  sequences: {
    videoFileId: number;
    resolutionId: number | null;
    frameRateId: number | null;
    qualityId: number | null;
    depthId: number | null;
    gamutId: number | null;
  }[];
}

export type ExperimentStatus = 'Complete' | 'Running' | 'Failed';

export interface Experiment {
  id: string;
  name: string;
  status: 'draft' | 'finalised';
  engineStatus?: ExperimentStatus;
  date: string;
  projectTypeId: number;
  encoders: { encoderTypeId: number; codecId: number; encoderModeId: number }[];
  sequences: { videoFileId: number }[];
  networkEmulation?: { packetLoss: number[]; delay: number[]; jitter: number[] };
}

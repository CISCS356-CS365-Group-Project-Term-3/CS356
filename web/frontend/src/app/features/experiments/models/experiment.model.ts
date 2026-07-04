export type ExperimentStatus = 'draft' | 'pending' | 'running' | 'complete' | 'failed';

export interface Experiment {
  id: string;
  name: string;
  status: 'draft' | 'finalised';
  engineStatus?: ExperimentStatus;
  date: string;
  projectTypeId: number;
  draftData?: {
    encoders: { encoderTypeId: number; codecId: number; encoderModeId: number }[];
    sequences: { videoFileId: number }[];
    networkEmulation?: { packetLoss: number[]; delay: number[]; jitter: number[] };
  };
  runs: ExperimentRun[];
}

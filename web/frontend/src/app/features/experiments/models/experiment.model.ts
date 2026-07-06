export type ExperimentStatus = 'draft' | 'pending' | 'running' | 'complete' | 'failed';

export interface ExperimentRun {
  id: number;
  groupId: number;
  sequenceCode: string;
  status: string;
  date: string;
  encoderData?: { encoderTypeId: number | null; codecId: number | null; encoderModeId: number | null };
  sequenceData?: { videoFileId: number };
  networkData?: { packetLoss: string; delay: string; jitter: string };
}

export interface Experiment {
  groupID: number;
  userId: number;
  name: string;
  status: 'draft' | 'pending';
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

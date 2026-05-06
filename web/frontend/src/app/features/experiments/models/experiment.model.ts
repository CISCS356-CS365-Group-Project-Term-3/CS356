export type ExperimentStatus = 'Complete' | 'Running' | 'Failed';

export interface Experiment {
  id: string;
  name: string;
  codec: string;
  sequences: string;
  date: string;
  status: ExperimentStatus;
}

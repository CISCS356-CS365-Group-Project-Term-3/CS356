export interface MetricAverage {
  y: number | null;
  u: number | null;
  v: number | null;
  combined: number | null;
}

export interface ResultSummary {
  experimentId: number;
  experimentName: string | null;
  batchId: string | null;
  groupId: number | null;
  userId: number | null;
  createdAt: string | null;
  sequenceCode: string | null;
  videoFileId: number | null;
  codecId: number | null;
  success: boolean;
  failureReason: string | null;
  frameCount: number;
  psnrAverage: MetricAverage;
  ssimAverage: MetricAverage;
}

export interface MetricSeries {
  y: number[];
  u: number[];
  v: number[];
  combined: number[];
}

export interface ExperimentFrames {
  psnr: Partial<MetricSeries>;
  ssim: Partial<MetricSeries>;
}

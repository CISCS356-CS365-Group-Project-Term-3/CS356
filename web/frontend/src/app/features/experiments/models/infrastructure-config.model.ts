export interface ProjectType {
  id: number;
  name: string;
}

export interface EncoderType {
  id: number;
  name: string;
  activeCodecs: number[];
}

export interface Codec {
  id: number;
  name: string;
}

export interface EncoderMode {
  id: number;
  name: string;
}

export interface VideoFile {
  id: number;
  name: string;
  availableSpatials: number[];
  availableTemporals: number[];
  availableDepths: number[];
}

export interface Resolution {
  id: number;
  name: string;
  value: string;
}

export interface FrameRate {
  id: number;
  name: string;
  value: string;
}

export interface QualityOption {
  id: number;
  name: string;
}

export interface DepthOption {
  id: number;
  name: string;
}

export interface GamutOption {
  id: number;
  name: string;
}

export interface Topology {
  id: number;
  name: string;
}

export interface TransmissionCondition {
  id: number;
  name: string;
  lowerBound: string;
  upperBound: string;
}

export interface InfrastructureConfig {
  projectTypes: ProjectType[];
  encoderTypes: EncoderType[];
  codecs: Codec[];
  encoderModes: EncoderMode[];
  videoFiles: VideoFile[];
  resolutions: Resolution[];
  frameRates: FrameRate[];
  quality: QualityOption[];
  depth: DepthOption[];
  gamut: GamutOption[];
  topologies: Topology[];
  transmissionConditions: TransmissionCondition[];
}

export interface ProjectType {
  id: number;
  name: string;
}

export interface EncoderType {
  id: number;
  name: string;
  active_codecs: number[];
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
  available_spatials: number[];
  available_temporals: number[];
  available_depths: number[];
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
  lower_bound: string;
  upper_bound: string;
}

export interface InfrastructureConfig {
  project_types: ProjectType[];
  encoder_types: EncoderType[];
  codecs: Codec[];
  encoder_modes: EncoderMode[];
  video_files: VideoFile[];
  resolutions: Resolution[];
  frame_rates: FrameRate[];
  quality: QualityOption[];
  depth: DepthOption[];
  gamut: GamutOption[];
  topologies: Topology[];
  transmission_conditions: TransmissionCondition[];
}

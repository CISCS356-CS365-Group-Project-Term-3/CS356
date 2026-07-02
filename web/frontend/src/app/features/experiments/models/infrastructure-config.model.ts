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
  spacial: [number, number]; // [width, height] — Fraser's spelling, must match JSON key
  temporal: number;
  depth: number;
  filepath?: string;
}

export interface Sequence {
  id: number;
  name: string;
  description?: string;
  videoFiles: VideoFile[];
}

export interface Topology {
  id: number;
  name: string;
}

export interface TransmissionCondition {
  id: number;
  name: string;
  lowerBound: number;
  upperBound: number;
}

export interface InfrastructureConfig {
  projectTypes: ProjectType[];
  encoderTypes: EncoderType[];
  codecs: Codec[];
  encoderModes: EncoderMode[];
  sequences: Sequence[];
  topologies: Topology[];
  transmissionConditions: TransmissionCondition[];
}

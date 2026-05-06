export interface InfrastructureConfig {
  project_types: ProjectType[];
  encoder_types: EncoderType[];
  codecs: Codec[];
  encoder_modes: EncoderMode[];
  scalability_types: ScalabilityType[];
  raw_files: RawFile[];
  pre_encoded_files: PreEncodedFile[];
}

export interface EncoderType {
  id: number;
  name: string;
  code: string;
  active: boolean;
  active_codecs: number[];
}

export interface Codec {
  id: number;
  name: string;
  code: string;
  max_layers: number;
  active_encoder_modes: number[];
  active_scalability: number[] | null;
}

export interface EncoderMode {
  id: number;
  name: string;
  code: string;
}

export interface ScalabilityOption {
  id: number;
  name: string;
  order: number;
  code: string;
  value: string;
}

export interface ScalabilityType {
  id: number;
  name: string;
  types: ScalabilityOption[]; // the actual selectable values
}

export interface PreEncodedFile {
  id: number;
  code: string;
  duration: string;
}

export interface RawFile {
  id: number;
  name: string;
  code: string;
  duration: string;
}

export interface ProjectType {
  id: number;
  name: string;
  code: string;
}

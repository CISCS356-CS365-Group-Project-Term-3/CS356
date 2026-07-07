import { InfrastructureConfig } from '../../experiments/models/infrastructure-config.model';

export const MOCK_INFRASTRUCTURE_CONFIG: InfrastructureConfig = {
  projectTypes: [{ id: 1, name: 'Encoder Only', networkEnabled: 0 }],
  encoderTypes: [{ id: 1, name: 'Standard Encoder', activeCodecs: [1, 2, 3] }],
  codecs: [
    { id: 1, name: 'AVC (H.264)' },
    { id: 2, name: 'HEVC (H.265)' },
    { id: 3, name: 'SVC (H.264)' },
  ],
  sequences: [
    {
      id: 1,
      name: 'Foreman',
      description: 'Talking head with camera pan.',
      videoFiles: [{ id: 1, name: 'foreman_cif.y4m', spacial: [352, 288], temporal: 30, depth: 8 }],
    },
    {
      id: 2,
      name: 'Coastguard',
      description: 'Boat moving across water.',
      videoFiles: [{ id: 2, name: 'coastguard_qcif_mono.y4m', spacial: [176, 144], temporal: 30, depth: 8 }],
    },
    {
      id: 3,
      name: 'Mobile',
      description: 'Static scene with fine detail and colour patterns.',
      videoFiles: [{ id: 3, name: 'mobile_sif.y4m', spacial: [352, 240], temporal: 30, depth: 8 }],
    },
  ],
  topologies: [{ id: 1, name: 'IP to IP' }],
  transmissionConditions: [],
};

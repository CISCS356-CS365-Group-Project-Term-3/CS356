import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { InfrastructureConfig } from '../models/infrastructure-config.model';

@Injectable({
  providedIn: 'root',
})
export class InfrastructureService {
  getConfig(): Observable<InfrastructureConfig> {
    return of(MOCK_CONFIG);
  }
}

const MOCK_CONFIG: InfrastructureConfig = {
  project_types: [
    { id: 1, name: 'Encoder Only', code: '000' },
    { id: 2, name: 'Live Streaming', code: '001' },
    { id: 3, name: 'Stream & Record', code: '002' },
  ],
  encoder_types: [
    { id: 1, name: 'Standard Encoder', code: '000', active: true, active_codecs: [1, 3, 5] },
    { id: 2, name: 'Scalable Encoder', code: '001', active: true, active_codecs: [2, 4] },
    { id: 3, name: '3D/Multiview Encoder', code: '002', active: false, active_codecs: [] },
  ],
  codecs: [
    {
      id: 1,
      name: 'AVC (H.264)',
      code: '000',
      max_layers: 1,
      active_encoder_modes: [1, 2, 3],
      active_scalability: null,
    },
    {
      id: 2,
      name: 'SVC (H.264)',
      code: '001',
      max_layers: 10,
      active_encoder_modes: [1, 2, 3],
      active_scalability: [1, 2],
    },
    {
      id: 3,
      name: 'HEVC (H.265)',
      code: '002',
      max_layers: 1,
      active_encoder_modes: [1, 2, 3],
      active_scalability: null,
    },
    {
      id: 4,
      name: 'SHVC (H.265)',
      code: '003',
      max_layers: 2,
      active_encoder_modes: [1, 2, 3],
      active_scalability: [1, 2, 3],
    },
    {
      id: 5,
      name: 'FVC - Future Video Coding',
      code: '004',
      max_layers: 1,
      active_encoder_modes: [1, 2, 3],
      active_scalability: null,
    },
  ],
  encoder_modes: [
    { id: 1, name: 'Random Access', code: '000' },
    { id: 2, name: 'Low Delay', code: '001' },
    { id: 3, name: 'Intra Only', code: '002' },
  ],
  scalability_types: [
    {
      id: 1,
      name: 'Spatial',
      types: [
        { id: 100, name: 'QCIF', order: 1, code: '000', value: '176x144' },
        { id: 101, name: 'QVGA', order: 2, code: '001', value: '320x240' },
        { id: 102, name: 'VGA', order: 3, code: '002', value: '640x480' },
        { id: 103, name: 'HD 720p', order: 4, code: '003', value: '1280x720' },
        { id: 104, name: 'FHD 1080p', order: 5, code: '004', value: '1920x1080' },
        { id: 105, name: '4K UHD', order: 6, code: '005', value: '3840x2160' },
      ],
    },
    {
      id: 2,
      name: 'Temporal',
      types: [
        { id: 200, name: '15fps', order: 1, code: '000', value: '15' },
        { id: 201, name: '24fps', order: 2, code: '001', value: '24' },
        { id: 202, name: '25fps', order: 3, code: '002', value: '25' },
        { id: 203, name: '30fps', order: 4, code: '003', value: '30' },
        { id: 204, name: '60fps', order: 5, code: '004', value: '60' },
        { id: 205, name: '120fps', order: 6, code: '005', value: '120' },
      ],
    },
    {
      id: 3,
      name: 'Quality',
      types: [
        { id: 300, name: 'Q20', order: 1, code: '000', value: '20' },
        { id: 301, name: 'Q22', order: 2, code: '001', value: '22' },
        { id: 302, name: 'Q24', order: 3, code: '002', value: '24' },
        { id: 303, name: 'Q26', order: 4, code: '003', value: '26' },
        { id: 304, name: 'Q28', order: 5, code: '004', value: '28' },
        { id: 305, name: 'Q30', order: 6, code: '005', value: '30' },
        { id: 306, name: 'Q32', order: 7, code: '006', value: '32' },
        { id: 307, name: 'Q34', order: 8, code: '007', value: '34' },
        { id: 308, name: 'Q36', order: 9, code: '008', value: '36' },
        { id: 309, name: 'Q38', order: 10, code: '009', value: '38' },
        { id: 310, name: 'Q40', order: 11, code: '010', value: '40' },
      ],
    },
    {
      id: 4,
      name: 'Depth',
      types: [
        { id: 400, name: '8 bit', order: 1, code: '000', value: '8' },
        { id: 401, name: '10 bit', order: 2, code: '001', value: '10' },
        { id: 402, name: '12 bit', order: 3, code: '002', value: '12' },
        { id: 403, name: '14 bit', order: 4, code: '003', value: '14' },
        { id: 404, name: '16 bit', order: 5, code: '004', value: '16' },
      ],
    },
  ],
  raw_files: [
    { id: 1, name: 'Beauty', code: '000', duration: '00:00:05:10' },
    { id: 2, name: 'Bosphorus', code: '001', duration: '00:00:05:10' },
    { id: 3, name: 'HoneyBee', code: '002', duration: '00:00:05:10' },
    { id: 4, name: 'Jockey', code: '003', duration: '00:00:05:10' },
    { id: 5, name: 'ReadySetGo', code: '004', duration: '00:00:05:10' },
    { id: 6, name: 'ShakeNDry', code: '005', duration: '00:00:05:10' },
    { id: 7, name: 'YachtRide', code: '006', duration: '00:00:05:10' },
  ],
  pre_encoded_files: [
    { id: 1, code: '001003000012005007000000000', duration: '00:00:05:10' },
    { id: 2, code: '001003000012005007000000001', duration: '00:00:05:10' },
    { id: 3, code: '001003000012005007000000002', duration: '00:00:05:10' },
    {
      id: 4,
      code: '001003000012005007000000000_001003000014005007000000000',
      duration: '00:00:05:10',
    },
  ],
};

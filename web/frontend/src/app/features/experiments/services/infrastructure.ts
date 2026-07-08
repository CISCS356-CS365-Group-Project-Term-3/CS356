import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, shareReplay, map } from 'rxjs';
import { InfrastructureConfig } from '../models/infrastructure-config.model';
import { camelizeKeys } from 'humps';

const API_BASE = '/infra';

@Injectable({
  providedIn: 'root',
})
export class InfrastructureService {
  private config$: Observable<InfrastructureConfig>;

  constructor(private http: HttpClient) {
    this.config$ = this.fetchConfig();
  }

  private fetchConfig(): Observable<InfrastructureConfig> {
    return this.http.get(`${API_BASE}/rest/get_active_ui_options`).pipe(
      map((data) => {
        const config = camelizeKeys(data) as InfrastructureConfig;
        config.encoderTypes = config.encoderTypes?.map((et) => ({
          ...et,
          activeCodecs: et.activeCodecs ?? [],
        }));
        return config;
      }),
      shareReplay(1),
    );
  }

  getConfig(): Observable<InfrastructureConfig> {
    return this.config$;
  }

  refreshConfig(): void {
    this.config$ = this.fetchConfig();
  }
}

const MOCK_CONFIG: InfrastructureConfig = {
  projectTypes: [
    { id: 1, name: 'Encoder Only', networkEnabled: 0 },
    { id: 2, name: 'Live Streaming', networkEnabled: 1 },
    { id: 3, name: 'Stream & Record', networkEnabled: 1 },
  ],

  encoderTypes: [
    { id: 1, name: 'Standard Encoder', activeCodecs: [1, 3] },
    { id: 2, name: 'Scalable Encoder', activeCodecs: [2] },
  ],

  codecs: [
    { id: 1, name: 'AVC (H.264)' },
    { id: 2, name: 'SVC (H.264)' },
    { id: 3, name: 'HEVC (H.265)' },
  ],

  sequences: [
    {
      id: 1,
      name: 'Beauty',
      description: 'Close-up of a woman applying makeup.',
      videoFiles: [
        { id: 1, name: 'beauty_832x480_24hz_10bit', spacial: [832, 480], temporal: 24, depth: 10 },
        {
          id: 2,
          name: 'beauty_1280x720_30hz_10bit',
          spacial: [1280, 720],
          temporal: 30,
          depth: 10,
        },
        {
          id: 3,
          name: 'beauty_1920x1080_60hz_10bit',
          spacial: [1920, 1080],
          temporal: 60,
          depth: 10,
        },
      ],
    },
    {
      id: 2,
      name: 'Honeybee',
      description: 'Macro footage of a honeybee in flight.',
      videoFiles: [
        {
          id: 4,
          name: 'honeybee_832x480_24hz_10bit',
          spacial: [832, 480],
          temporal: 24,
          depth: 10,
        },
        {
          id: 5,
          name: 'honeybee_1920x1080_30hz_10bit',
          spacial: [1920, 1080],
          temporal: 30,
          depth: 10,
        },
      ],
    },
    {
      id: 3,
      name: 'Bosphorous',
      description: 'Outdoor scene with complex motion and depth.',
      videoFiles: [
        {
          id: 6,
          name: 'bosphorous_832x480_24hz_10bit',
          spacial: [832, 480],
          temporal: 24,
          depth: 10,
        },
        {
          id: 7,
          name: 'bosphorous_1280x720_24hz_10bit',
          spacial: [1280, 720],
          temporal: 24,
          depth: 10,
        },
        {
          id: 8,
          name: 'bosphorous_1920x1080_24hz_12bit',
          spacial: [1920, 1080],
          temporal: 24,
          depth: 12,
        },
      ],
    },
  ],

  topologies: [
    { id: 1, name: 'IP to IP' },
    { id: 2, name: 'Selfnet' },
  ],

  transmissionConditions: [
    { id: 1, name: 'Delay', lowerBound: 0, upperBound: 999 },
    { id: 2, name: 'Jitter', lowerBound: 0, upperBound: 200 },
    { id: 3, name: 'Packet Loss', lowerBound: 0, upperBound: 20 },
  ],
};

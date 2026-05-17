import { Injectable } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
import { Observable, of, shareReplay } from 'rxjs';
import { InfrastructureConfig } from '../models/infrastructure-config.model';

@Injectable({
  providedIn: 'root',
})
export class InfrastructureService {
  // constructor(private http: HttpClient) {}

  // private config$ = this.http.get<InfrastructureConfig>('/api/config').pipe(shareReplay(1));
  private config$ = of(MOCK_CONFIG).pipe(shareReplay(1));

  getConfig(): Observable<InfrastructureConfig> {
    return this.config$;
  }
}

const MOCK_CONFIG: InfrastructureConfig = {
  project_types: [
    { id: 1, name: 'Encoder Only' },
    { id: 2, name: 'Live Streaming' },
    { id: 3, name: 'Stream & Record' },
  ],

  encoder_types: [
    { id: 1, name: 'Standard Encoder', active_codecs: [1, 3] },
    { id: 2, name: 'Scalable Encoder', active_codecs: [2] },
  ],

  codecs: [
    { id: 1, name: 'AVC (H.264)' },
    { id: 2, name: 'SVC (H.264)' },
    { id: 3, name: 'HEVC (H.265)' },
  ],

  encoder_modes: [
    { id: 1, name: 'Random Access' },
    { id: 2, name: 'Low Delay' },
    { id: 3, name: 'Intra Only' },
  ],

  video_files: [
    {
      id: 1,
      name: 'Beauty',
      available_spatials: [1, 2, 3],
      available_temporals: [1, 2],
      available_depths: [1],
    },
    {
      id: 2,
      name: 'Honeybee',
      available_spatials: [1, 2, 3],
      available_temporals: [1, 2],
      available_depths: [1],
    },
    {
      id: 3,
      name: 'Bosphorous',
      available_spatials: [1, 2, 3],
      available_temporals: [1, 2],
      available_depths: [1, 2],
    },
  ],

  resolutions: [
    { id: 1, name: 'WVGA', value: '832x480' },
    { id: 2, name: 'XGA', value: '1024x768' },
    { id: 3, name: 'HD720', value: '1280x720' },
  ],

  frame_rates: [
    { id: 1, name: '20fps', value: '20' },
    { id: 2, name: '24fps', value: '24' },
  ],

  quality: [
    { id: 1, name: 'Q20' },
    { id: 2, name: 'Q21' },
  ],

  depth: [
    { id: 1, name: '10 bit' },
    { id: 2, name: '12 bit' },
  ],

  gamut: [{ id: 1, name: 'Gamut 1' }],

  topologies: [
    { id: 1, name: 'IP to IP' },
    { id: 2, name: 'Selfnet' },
  ],

  transmission_conditions: [
    { id: 1, name: 'Delay', lower_bound: '0ms', upper_bound: '1000ms' },
    { id: 2, name: 'Jitter', lower_bound: '0ms', upper_bound: '1000ms' },
  ],
};

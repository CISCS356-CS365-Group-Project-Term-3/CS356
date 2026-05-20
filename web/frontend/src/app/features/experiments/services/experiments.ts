import { Injectable } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { Experiment, ExperimentDetail } from '../models/experiment.model';

@Injectable({
  providedIn: 'root',
})
export class ExperimentsService {
  // constructor(private http: HttpClient) {}

  getExperiments() {
    // return this.http.get<Experiment[]>('/api/experiments');
    return of(this.mockExperiments);
  }

  getExperimentById(id: string) {
    // return this.http.get<ExperimentDetail>(`/api/experiments/${id}`);
    const detail = this.mockExperimentDetails[id] ?? this.mockExperimentDetails['#01'];
    return of(detail);
  }

  createExperiment(payload: object) {
    // return this.http.post<{ id: string }>('/api/experiments', payload);
  }
  private mockExperiments: Experiment[] = [
    {
      id: '1',
      name: 'Experiment',
      codec: 'HEVC',
      sequences: 'Beauty, Bosphorus',
      date: 'Today 14:32',
      status: 'Complete',
    },
    {
      id: '2',
      name: 'Experiment',
      codec: 'AVC',
      sequences: 'HoneyBee, Jockey',
      date: 'Today 13:10',
      status: 'Running',
    },
    {
      id: '3',
      name: 'Experiment',
      codec: 'SHVC',
      sequences: 'ReadySetGo',
      date: 'Today 11:45',
      status: 'Running',
    },
    {
      id: '4',
      name: 'Experiment',
      codec: 'HEVC',
      sequences: 'Beauty, ShakeNDry',
      date: 'Yesterday',
      status: 'Complete',
    },
    {
      id: '5',
      name: 'Experiment',
      codec: 'AVC',
      sequences: 'YachtRide',
      date: '03/05/2026',
      status: 'Failed',
    },
  ];

  private mockExperimentDetails: Record<string, ExperimentDetail> = {
    '#01': {
      id: '#01',
      name: 'Experiment 1',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 3, encoderModeId: 1 }],
      sequences: [
        { videoFileId: 1, resolutionId: 3, frameRateId: 1, qualityId: 1, depthId: 1, gamutId: 1 },
        { videoFileId: 2, resolutionId: 2, frameRateId: 2, qualityId: 2, depthId: 1, gamutId: 1 },
      ],
    },
    '#02': {
      id: '#02',
      name: 'Experiment 2',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 1, encoderModeId: 2 }],
      sequences: [
        { videoFileId: 1, resolutionId: 1, frameRateId: 1, qualityId: 1, depthId: 1, gamutId: 1 },
        { videoFileId: 3, resolutionId: 3, frameRateId: 2, qualityId: 2, depthId: 2, gamutId: 1 },
      ],
    },
  };
}

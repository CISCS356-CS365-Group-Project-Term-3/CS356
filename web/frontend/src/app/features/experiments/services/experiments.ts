import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { Experiment } from '../models/experiment.model';

const API_BASE = 'http://localhost:5000';

@Injectable({
  providedIn: 'root',
})
export class ExperimentsService {
  constructor(private http: HttpClient) {}

  getExperiments() {
    // TODO: swap when abdur GET /experiments is ready
    // return this.http.get<Experiment[]>(`${API_BASE}/experiments?user_id=1`);
    return of(this.mockExperiments);
  }

  getExperimentById(id: string) {
    return this.http.get<Experiment>(`${API_BASE}/experiments/${id}`);
    // return of(this.mockExperiments.find((e) => e.id === id) ?? this.mockExperiments[0]);
  }

  createExperiment(payload: object) {
    return this.http.post<{ id: number }>(`${API_BASE}/experiments`, payload);
  }

  private mockExperiments: Experiment[] = [
    {
      id: '1',
      name: 'Experiment 1',
      status: 'Complete',
      date: 'Today 14:32',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 3, encoderModeId: 1 }],
      sequences: [
        { videoFileId: 1, resolutionId: 3, frameRateId: 1, qualityId: 1, depthId: 1, gamutId: 1 },
        { videoFileId: 2, resolutionId: 2, frameRateId: 2, qualityId: 2, depthId: 1, gamutId: 1 },
      ],
    },
    {
      id: '2',
      name: 'Experiment 2',
      status: 'Running',
      date: 'Today 13:10',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 1, encoderModeId: 2 }],
      sequences: [
        { videoFileId: 2, resolutionId: 1, frameRateId: 1, qualityId: 1, depthId: 1, gamutId: 1 },
        { videoFileId: 3, resolutionId: 2, frameRateId: 2, qualityId: 2, depthId: 1, gamutId: 1 },
      ],
    },
    {
      id: '3',
      name: 'Experiment 3',
      status: 'Running',
      date: 'Today 11:45',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 2, encoderModeId: 1 }],
      sequences: [
        { videoFileId: 3, resolutionId: 3, frameRateId: 1, qualityId: 1, depthId: 2, gamutId: 1 },
      ],
    },
    {
      id: '4',
      name: 'Experiment 4',
      status: 'Complete',
      date: 'Yesterday',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 3, encoderModeId: 2 }],
      sequences: [
        { videoFileId: 1, resolutionId: 2, frameRateId: 2, qualityId: 2, depthId: 1, gamutId: 1 },
        { videoFileId: 3, resolutionId: 1, frameRateId: 1, qualityId: 1, depthId: 1, gamutId: 1 },
      ],
    },
    {
      id: '5',
      name: 'Experiment 5',
      status: 'Failed',
      date: '03/05/2026',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 1, encoderModeId: 1 }],
      sequences: [
        { videoFileId: 2, resolutionId: 3, frameRateId: 2, qualityId: 2, depthId: 1, gamutId: 1 },
      ],
    },
  ];
}

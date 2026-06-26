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
    // TODO: replace hardcoded userId=1 once auth is wired up
    return this.http.get<Experiment[]>(`${API_BASE}/experiments?userId=1`);
    // return of(this.mockExperiments);
  }

  getExperimentById(id: string) {
    return this.http.get<Experiment>(`${API_BASE}/experiments/${id}`);
  }

  createExperiment(payload: object) {
    return this.http.post<{ id: number }>(`${API_BASE}/experiments`, payload);
  }

  patchExperiment(id: string, payload: object) {
    return this.http.patch<{ id: number }>(`${API_BASE}/experiments/${id}`, payload);
  }

  private mockExperiments: Experiment[] = [
    {
      id: '1',
      name: 'Experiment 1',
      status: 'finalised',
      engineStatus: 'Complete',
      date: '2026-06-04T14:32:00',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 3 }],
      sequences: [{ videoFileId: 1 }, { videoFileId: 4 }],
    },
    {
      id: '2',
      name: 'Experiment 2',
      status: 'finalised',
      engineStatus: 'Running',
      date: '2026-06-04T13:10:00',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 1 }],
      sequences: [{ videoFileId: 2 }, { videoFileId: 6 }],
    },
    {
      id: '3',
      name: 'Experiment 3',
      status: 'finalised',
      engineStatus: 'Running',
      date: '2026-06-04T11:45:00',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 2 }],
      sequences: [{ videoFileId: 8 }],
    },
    {
      id: '4',
      name: 'Experiment 4',
      status: 'draft',
      date: '2026-06-03T09:20:00',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 3 }],
      sequences: [{ videoFileId: 3 }, { videoFileId: 7 }],
    },
    {
      id: '5',
      name: 'Experiment 5',
      status: 'finalised',
      engineStatus: 'Failed',
      date: '2026-05-03T16:00:00',
      projectTypeId: 1,
      encoders: [{ encoderTypeId: 1, codecId: 1 }],
      sequences: [{ videoFileId: 5 }],
    },
  ];
}

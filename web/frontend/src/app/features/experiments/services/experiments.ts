import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Experiment } from '../models/experiment.model';

const API_BASE = '/experiment-management';

@Injectable({
  providedIn: 'root',
})
export class ExperimentsService {
  constructor(private http: HttpClient) {}

  getExperiments(userId?: number) {
    const url =
      userId != null ? `${API_BASE}/experiments?userId=${userId}` : `${API_BASE}/experiments`;
    return this.http.get<Experiment[]>(url);
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
}

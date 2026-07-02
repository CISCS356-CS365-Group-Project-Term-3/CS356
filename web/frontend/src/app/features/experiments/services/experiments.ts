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

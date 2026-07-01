import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ResultSummary, ExperimentFrames } from '../models/result-summary.model';

const API_BASE = '/experiment-management';

@Injectable({
  providedIn: 'root',
})
export class ResultsService {
  constructor(private http: HttpClient) {}

  getResultSummaries() {
    return this.http.get<ResultSummary[]>(`${API_BASE}/experiments-results`);
  }

  getFrames(experimentId: number) {
    return this.http.get<ExperimentFrames>(`${API_BASE}/experiments-results/${experimentId}/frames`);
  }
}

import { Injectable } from '@angular/core';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ExperimentsService {
  getExperiments() {
    return of(this.mockExperiments);
  }
  private mockExperiments = [
    {
      id: '#01',
      name: 'Experiment 1',
      codec: 'HEVC',
      sequences: 'Beauty, Bosphorus',
      date: 'Today 14:32',
      status: 'Complete',
    },
    {
      id: '#02',
      name: 'Experiment 2',
      codec: 'AVC',
      sequences: 'HoneyBee, Jockey',
      date: 'Today 13:10',
      status: 'Running',
    },
    {
      id: '#03',
      name: 'Experiment 3',
      codec: 'SHVC',
      sequences: 'ReadySetGo',
      date: 'Today 11:45',
      status: 'Running',
    },
    {
      id: '#04',
      name: 'Experiment 4',
      codec: 'HEVC',
      sequences: 'Beauty, ShakeNDry',
      date: 'Yesterday',
      status: 'Complete',
    },
    {
      id: '#05',
      name: 'Experiment 5',
      codec: 'AVC',
      sequences: 'YachtRide',
      date: '03/05/2026',
      status: 'Failed',
    },
  ];
}

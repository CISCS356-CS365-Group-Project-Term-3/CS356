import { Injectable } from '@angular/core';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ExperimentsService {
  private mockExperiments = [
    {
      id: '#042',
      name: 'HEVC comparison',
      codec: 'HEVC',
      sequences: 'Beauty, Bosphorus',
      date: 'Today 14:32',
      status: 'Complete',
    },
    {
      id: '#041',
      name: 'AVC low delay test',
      codec: 'AVC',
      sequences: 'HoneyBee, Jockey',
      date: 'Today 13:10',
      status: 'Running',
    },
    {
      id: '#040',
      name: 'SHVC scalability',
      codec: 'SHVC',
      sequences: 'ReadySetGo',
      date: 'Today 11:45',
      status: 'Running',
    },
    {
      id: '#039',
      name: 'H.265 quality test',
      codec: 'HEVC',
      sequences: 'Beauty, ShakeNDry',
      date: 'Yesterday',
      status: 'Complete',
    },
    {
      id: '#038',
      name: 'Baseline AVC',
      codec: 'AVC',
      sequences: 'YachtRide',
      date: 'Yesterday',
      status: 'Failed',
    },
  ];

  getExperiments() {
    return of(this.mockExperiments);
  }
}

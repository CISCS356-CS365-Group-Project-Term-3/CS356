import { Injectable } from '@angular/core';

export interface NewExperimentForm {
  name: string;
  projectTypeId: number | null;
  encoderTypeId: number | null;
  codecId: number | null;
  encoderModeId: number | null;
  sequenceIds: number[];
}

@Injectable({ providedIn: 'root' })
export class NewExperimentFormService {
  form: NewExperimentForm = {
    name: '',
    projectTypeId: null,
    encoderTypeId: null,
    codecId: null,
    encoderModeId: null,
    sequenceIds: [],
  };
}

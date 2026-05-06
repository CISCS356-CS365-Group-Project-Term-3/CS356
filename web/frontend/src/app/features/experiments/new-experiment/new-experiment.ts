import { Component } from '@angular/core';
import { MatStepperModule } from '@angular/material/stepper';
import { MatButtonModule } from '@angular/material/button';
import { RouterLink } from '@angular/router';
import { NewExperimentFormService } from './new-experiment-form.service';
import { ProjectSetup } from './steps/project-setup/project-setup';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-new-experiment',
  imports: [MatStepperModule, MatButtonModule, RouterLink, ProjectSetup, MatCardModule],
  templateUrl: './new-experiment.html',
  styleUrl: './new-experiment.scss',
})
export class NewExperiment {
  constructor(public formService: NewExperimentFormService) {}

  isProjectSetupComplete(): boolean {
    const form = this.formService.form;
    return form.name.trim().length > 0 && form.projectTypeId !== null;
  }

  canProceed(stepIndex: number): boolean {
    switch (stepIndex) {
      case 0:
        return this.isProjectSetupComplete();
      default:
        return true;
    }
  }
}

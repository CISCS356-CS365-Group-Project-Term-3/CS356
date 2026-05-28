import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { InfrastructureService } from '../../../services/infrastructure';
import { ProjectType } from '../../../models/infrastructure-config.model';
import { NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-project-setup',
  imports: [FormsModule, MatCardModule, MatFormFieldModule, MatInputModule, MatSelectModule],
  templateUrl: './project-setup.html',
  styleUrl: './project-setup.scss',
})
export class ProjectSetup implements OnInit {
  projectTypes: ProjectType[] = [];

  projectTypeDescriptions: Record<string, string> = {
    'Encoder Only':    'Run encoding experiments without any streaming output',
    'Live Streaming':  'Encode and stream video output in real time',
    'Stream & Record': 'Encode, stream, and save output simultaneously',
  };

  constructor(
    private infrastructureService: InfrastructureService,
    public formService: NewExperimentFormService,
  ) {}

  ngOnInit(): void {
    this.infrastructureService.getConfig().subscribe((data) => {
      this.projectTypes = data.project_types;
    });
  }
}

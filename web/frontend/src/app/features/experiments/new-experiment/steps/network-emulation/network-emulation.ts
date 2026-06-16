import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-network-emulation',
  imports: [FormsModule, MatFormFieldModule, MatInputModule],
  templateUrl: './network-emulation.html',
  styleUrl: './network-emulation.scss',
})
export class NetworkEmulationStep {
  constructor(public formService: NewExperimentFormService) {}
}

import { Component } from '@angular/core';
import { MatChipsModule, MatChipInputEvent } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { NewExperimentFormService } from '../../new-experiment-form.service';

@Component({
  selector: 'app-network-emulation',
  imports: [MatChipsModule, MatFormFieldModule, MatIconModule],
  templateUrl: './network-emulation.html',
  styleUrl: './network-emulation.scss',
})
export class NetworkEmulationStep {
  readonly separatorKeysCodes = [ENTER, COMMA] as const;

  constructor(public formService: NewExperimentFormService) {}

  addValue(field: 'packetLoss' | 'delay' | 'jitter', event: MatChipInputEvent): void {
    const num = parseFloat(event.value.trim());
    if (!isNaN(num) && num >= 0) {
      this.formService.form.networkEmulation[field].push(num);
    }
    event.chipInput.clear();
  }

  removeValue(field: 'packetLoss' | 'delay' | 'jitter', index: number): void {
    this.formService.form.networkEmulation[field].splice(index, 1);
  }
}

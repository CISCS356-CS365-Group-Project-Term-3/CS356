import { Component, OnInit } from '@angular/core';
import { MatChipsModule, MatChipInputEvent } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { NewExperimentFormService } from '../../new-experiment-form.service';
import { InfrastructureService } from '../../../services/infrastructure.service';
import { TransmissionCondition } from '../../../models/infrastructure-config.model';

type NetworkField = 'packetLoss' | 'delay' | 'jitter';

const FIELD_CONDITION_NAME: Record<NetworkField, string> = {
  packetLoss: 'packet loss',
  delay: 'delay',
  jitter: 'jitter',
};

@Component({
  selector: 'app-network-emulation',
  imports: [MatChipsModule, MatFormFieldModule, MatIconModule],
  templateUrl: './network-emulation.html',
  styleUrl: './network-emulation.scss',
})
export class NetworkEmulationStep implements OnInit {
  readonly separatorKeysCodes = [ENTER, COMMA] as const;
  readonly fields: NetworkField[] = ['packetLoss', 'delay', 'jitter'];

  conditions: Record<NetworkField, TransmissionCondition | undefined> = {
    packetLoss: undefined,
    delay: undefined,
    jitter: undefined,
  };

  constructor(
    public formService: NewExperimentFormService,
    private infraService: InfrastructureService,
  ) {}

  ngOnInit(): void {
    this.infraService.getConfig().subscribe((config) => {
      for (const field of this.fields) {
        this.conditions[field] = config.transmissionConditions?.find(
          (c) => c.name.toLowerCase() === FIELD_CONDITION_NAME[field],
        );
      }
    });
  }

  getLabel(field: NetworkField): string {
    const c = this.conditions[field];
    if (!c) return field;
    return c.unit ? `${c.name} (${c.unit})` : c.name;
  }

  getUnit(field: NetworkField): string {
    return this.conditions[field]?.unit ?? '';
  }

  getBoundsHint(field: NetworkField): string {
    const c = this.conditions[field];
    if (!c) return 'Enter a value';
    const u = c.unit ?? '';
    return `${c.lowerBound}${u} – ${c.upperBound}${u}`;
  }

  addValue(field: NetworkField, event: MatChipInputEvent): void {
    const num = parseFloat(event.value.trim());
    const c = this.conditions[field];
    const min = c?.lowerBound ?? 0;
    const max = c?.upperBound ?? Infinity;
    if (!isNaN(num) && num >= min && num <= max) {
      this.formService.form.networkEmulation[field].push(num);
    }
    event.chipInput.clear();
  }

  removeValue(field: NetworkField, index: number): void {
    this.formService.form.networkEmulation[field].splice(index, 1);
  }
}

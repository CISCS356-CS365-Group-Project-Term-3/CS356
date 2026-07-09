import { Component, OnInit } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { NewExperimentFormService } from '../../new-experiment-form.service';
import { InfrastructureService } from '../../../services/infrastructure';
import { TransmissionCondition } from '../../../models/infrastructure-config.model';

type NetworkField = 'packetLoss' | 'delay' | 'jitter';

const FIELD_CONDITION_NAME: Record<NetworkField, string> = {
  packetLoss: 'packet loss',
  delay: 'delay',
  jitter: 'jitter',
};

@Component({
  selector: 'app-network-emulation',
  imports: [MatFormFieldModule, MatInputModule],
  templateUrl: './network-emulation.html',
  styleUrl: './network-emulation.scss',
})
export class NetworkEmulationStep implements OnInit {
  readonly fields: NetworkField[] = ['packetLoss', 'delay', 'jitter'];

  conditions: Record<NetworkField, TransmissionCondition | undefined> = {
    packetLoss: undefined,
    delay: undefined,
    jitter: undefined,
  };

  errors: Record<NetworkField, string | null> = {
    packetLoss: null,
    delay: null,
    jitter: null,
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
    return `${this.getMin(field, c)}${u} – ${c.upperBound}${u}`;
  }

  private getMin(field: NetworkField, c: TransmissionCondition | undefined): number {
    const lowerBound = c?.lowerBound ?? 0;
    return field === 'packetLoss' ? Math.max(lowerBound, 0.1) : lowerBound;
  }

  onBlur(field: NetworkField, input: HTMLInputElement): void {
    this.updateValue(field, input.value);
    const stored = this.formService.form.networkEmulation[field];
    input.value = stored != null ? String(stored) : '';
  }

  clearError(field: NetworkField): void {
    this.errors[field] = null;
  }

  private updateValue(field: NetworkField, rawValue: string): void {
    const raw = rawValue.trim();
    this.errors[field] = null;

    if (raw === '') {
      this.formService.form.networkEmulation[field] = null;
      return;
    }

    const c = this.conditions[field];
    const max = c?.upperBound ?? Infinity;
    const unit = this.getUnit(field);
    let num: number;

    const min = this.getMin(field, c);

    if (field === 'packetLoss') {
      num = Math.round(parseFloat(raw) * 10) / 10;
      if (isNaN(num) || num < min || num > max) {
        this.formService.form.networkEmulation[field] = null;
        this.errors[field] = `Enter a value between ${min}${unit} and ${max}${unit}`;
        return;
      }
    } else {
      const parsed = parseFloat(raw);
      if (isNaN(parsed) || !Number.isInteger(parsed) || parsed < min || parsed > max) {
        this.formService.form.networkEmulation[field] = null;
        this.errors[field] = `Enter a whole number between ${min}${unit} and ${max}${unit}`;
        return;
      }
      num = parsed;
    }

    this.formService.form.networkEmulation[field] = num;
  }
}

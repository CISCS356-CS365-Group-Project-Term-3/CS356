import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';
import { describe, it, beforeEach, expect, vi } from 'vitest';
import { Dashboard } from './dashboard';
import { ExperimentsService } from '../services/experiments';
import { NewExperimentFormService } from '../new-experiment/new-experiment-form.service';
import { InfrastructureService } from '../services/infrastructure';
import { UserManagementService } from '../../user_management/user-management-service';
import { Experiment } from '../models/experiment.model';

const experiments: Experiment[] = [
  {
    id: '1',
    name: 'Exp A',
    status: 'finalised',
    engineStatus: 'Complete',
    date: '2026-01-01',
    projectTypeId: 1,
    encoders: [],
    sequences: [],
  },
  {
    id: '2',
    name: 'Exp B',
    status: 'finalised',
    engineStatus: 'Running',
    date: '2026-01-02',
    projectTypeId: 1,
    encoders: [],
    sequences: [],
  },
  {
    id: '3',
    name: 'Expe C',
    status: 'finalised',
    engineStatus: 'Failed',
    date: '2026-01-03',
    projectTypeId: 1,
    encoders: [],
    sequences: [],
  },
  {
    id: '4',
    name: 'Draft',
    status: 'draft',
    date: '2026-01-04',
    projectTypeId: 1,
    encoders: [],
    sequences: [],
  },
];

describe('Dashboard', () => {
  let component: Dashboard;
  let fixture: ComponentFixture<Dashboard>;
  let experimentsService: any;
  let formService: any;

  beforeEach(async () => {
    experimentsService = {
      getExperiments: vi.fn().mockReturnValue(of(experiments)),
      getExperimentById: vi.fn().mockReturnValue(of(experiments[0])),
    };
    formService = { setTemplate: vi.fn(), setDraft: vi.fn() };

    await TestBed.configureTestingModule({
      imports: [Dashboard],
      providers: [
        provideRouter([]),
        { provide: ExperimentsService, useValue: experimentsService },
        { provide: NewExperimentFormService, useValue: formService },
        {
          provide: InfrastructureService,
          useValue: {
            getConfig: vi.fn().mockReturnValue(
              of({
                projectTypes: [],
                encoderTypes: [],
                codecs: [],
                sequences: [],
                topologies: [],
                transmissionConditions: [],
              }),
            ),
          },
        },
        {
          provide: UserManagementService,
          useValue: {
            getUserInfo: vi.fn().mockReturnValue(of({ user_id: 1, user_role: 'user' })),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(Dashboard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('creates the compoent', () => {
    expect(component).toBeTruthy();
  });

  it('loads experiments on init', () => {
    expect(component.experiments).toEqual(experiments);
    expect(component.isLoading).toBe(false);
  });

  it('clears isLoading if the request fails', () => {
    experimentsService.getExperiments.mockReturnValue(throwError(() => new Error()));
    component.loadExperiments();
    expect(component.isLoading).toBe(false);
  });

  it('stat counts are correct', () => {
    expect(component.totalCount).toBe(4);
    expect(component.completedCount).toBe(1);
    expect(component.runningCount).toBe(1);
    expect(component.failedCount).toBe(1);
  });

  it('filteredExperiments respects showDraftsOnly and status filter', () => {
    expect(component.filteredExperiments).toEqual(experiments);

    component.showDraftsOnly = true;
    expect(component.filteredExperiments).toEqual([experiments[3]]);

    component.showDraftsOnly = false;
    component.activeStatusFilter = 'Complete';
    expect(component.filteredExperiments).toEqual([experiments[0]]);
  });

  it('toggleDrafts clears the status filter and selection', () => {
    component.activeStatusFilter = 'Complete';
    component.selectedExperiment = experiments[0];
    component.toggleDrafts();
    expect(component.showDraftsOnly).toBe(true);
    expect(component.activeStatusFilter).toBeNull();
    expect(component.selectedExperiment).toBeNull();
  });

  it('setStatusFilter toggles off when the same status is clicked twice', () => {
    component.setStatusFilter('Running');
    expect(component.activeStatusFilter).toBe('Running');
    component.setStatusFilter('Running');
    expect(component.activeStatusFilter).toBeNull();
  });

  it('clicking a selected row deselects it', () => {
    component.selectedExperiment = experiments[0];
    const setSelected = vi.fn();
    component.onRowClicked({ data: experiments[0], node: { setSelected } } as any);
    expect(setSelected).toHaveBeenCalledWith(false);
  });

  it('createFromTemplate does nothing if nothing is selected', () => {
    component.selectedExperiment = null;
    component.createFromTemplate();
    expect(experimentsService.getExperimentById).not.toHaveBeenCalled();
  });

  it('statusCellRenderer returns the right badge for each state', () => {
    expect(
      component.statusCellRenderer({
        value: undefined,
        data: { ...experiments[3], status: 'draft' },
      }),
    ).toContain('Draft');
    expect(
      component.statusCellRenderer({
        value: undefined,
        data: { ...experiments[0], status: 'finalised' },
      }),
    ).toContain('Pending');
    expect(component.statusCellRenderer({ value: 'Complete', data: experiments[0] })).toContain(
      'Complete',
    );
    expect(component.statusCellRenderer({ value: 'Running', data: experiments[1] })).toContain(
      'Running',
    );
    expect(component.statusCellRenderer({ value: 'Failed', data: experiments[2] })).toContain(
      'Failed',
    );
  });
});

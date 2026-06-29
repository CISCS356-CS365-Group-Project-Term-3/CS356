import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ResultsPage } from './results';

describe('ResultsPage', () => {
  let component: ResultsPage;
  let fixture: ComponentFixture<ResultsPage>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResultsPage],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();

    fixture = TestBed.createComponent(ResultsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();

    httpMock = TestBed.inject(HttpTestingController);
    httpMock.expectOne('/experiment-management/experiments-results').flush([
      {
        experimentId: 1,
        experimentName: 'Experiment 1',
        batchId: 'batch-1',
        groupId: null,
        userId: null,
        createdAt: '2026-06-23T09:40:00',
        sequenceCode: '001002000000000000',
        videoFileId: 1,
        codecId: 1,
        success: true,
        failureReason: null,
        frameCount: 88,
        psnrAverage: { y: 34.76, u: 35.62, v: 35.18, combined: 35.18 },
        ssimAverage: { y: 0.931, u: 0.915, v: 0.919, combined: 0.922 },
      },
      {
        experimentId: 2,
        experimentName: 'Experiment 1',
        batchId: 'batch-1',
        groupId: null,
        userId: null,
        createdAt: '2026-06-23T09:40:00',
        sequenceCode: '001003000000000000',
        videoFileId: 1,
        codecId: 2,
        success: true,
        failureReason: null,
        frameCount: 88,
        psnrAverage: { y: 36.1, u: 37.0, v: 36.5, combined: 36.6 },
        ssimAverage: { y: 0.94, u: 0.93, v: 0.935, combined: 0.938 },
      },
    ]);
    httpMock.expectOne('/infra/rest/get_active_ui_options').flush({
      codecs: [
        { id: 1, name: 'AVC (H.264)' },
        { id: 2, name: 'HEVC (H.265)' },
      ],
      sequences: [],
    });

    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('groups same-batch codec runs into a single comparison entry', () => {
    expect(component.experimentHistory.length).toBe(1);
    expect(component.experimentHistory[0].codecRuns.length).toBe(2);
  });

  it('should render the fetched results sections with both codecs compared', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Results Portal');
    expect(compiled.textContent).toContain('PSNR overview');
    expect(compiled.textContent).toContain('SSIM overview');
    expect(compiled.textContent).toContain('Experiment 1');
    expect(compiled.textContent).toContain('AVC (H.264)');
    expect(compiled.textContent).toContain('HEVC (H.265)');
  });
});

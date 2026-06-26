import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ResultsPage } from './results';

describe('ResultsPage', () => {
  let component: ResultsPage;
  let fixture: ComponentFixture<ResultsPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResultsPage],
    }).compileComponents();

    fixture = TestBed.createComponent(ResultsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render the placeholder results sections', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Results Portal');
    expect(compiled.textContent).toContain('PSNR overview');
    expect(compiled.textContent).toContain('SSIM overview');
  });
});

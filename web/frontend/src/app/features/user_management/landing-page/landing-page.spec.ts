import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LandingPage } from './landing-page';
import { ConfirmLogoutDialog } from '../confirm-logout-dialog/confirm-logout-dialog';
import { provideRouter } from '@angular/router';
import { RouterLink } from '@angular/router';
import { MatDialogModule } from '@angular/material/dialog';

describe('LandingPage', () => {
  let component: LandingPage;
  let fixture: ComponentFixture<LandingPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LandingPage, ConfirmLogoutDialog, RouterLink, MatDialogModule],
      providers: [
        provideRouter([])
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(LandingPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should render page header', () => {
    const compiled = fixture.nativeElement;
    const header = compiled.querySelector('.page-header h1');
    expect(header).toBeTruthy();
    expect(header.textContent).toContain('Welcome');
  });

  it('should render three portal cards', () => {
    const compiled = fixture.nativeElement;
    const cards = compiled.querySelectorAll('mat-card');
    expect(cards.length).toBe(3);
  });

  it('should render card headings', () => {
    const compiled = fixture.nativeElement;
    const headings = compiled.querySelectorAll('.portal-cards h2');
    expect(headings.length).toBe(3);
    expect(headings[0].textContent).toContain('Infrastructure');
    expect(headings[1].textContent).toContain('Experiments');
    expect(headings[2].textContent).toContain('Results');
  });

  it('should render card images', () => {
    const compiled = fixture.nativeElement;
    const images = compiled.querySelectorAll('img[mat-card-image]');
    expect(images.length).toBe(3);
  });

  it('should render logout button', () => {
    const compiled = fixture.nativeElement;
    const logoutButton = compiled.querySelector('.log-out-button');
    expect(logoutButton).toBeTruthy();
    expect(logoutButton.textContent).toContain('Log out');
  });
});

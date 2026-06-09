import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Navbar } from './navbar';
import { provideRouter } from '@angular/router';
import { MatDialogModule } from '@angular/material/dialog';

describe('Navbar', () => {
  let component: Navbar;
  let fixture: ComponentFixture<Navbar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Navbar, MatDialogModule],
      providers: [
        provideRouter([])
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(Navbar);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render navbar with logo', () => {
    const compiled = fixture.nativeElement;
    const logo = compiled.querySelector('.navbar-logo img');
    expect(logo).toBeTruthy();
  });

  it('should render navigation links', () => {
    const compiled = fixture.nativeElement;
    const links = compiled.querySelectorAll('.navbar-links a');
    expect(links.length).toBeGreaterThan(0);
  });

  it('should render logout button', () => {
    const compiled = fixture.nativeElement;
    const logoutButton = compiled.querySelector('.log-out-button');
    expect(logoutButton).toBeTruthy();
    expect(logoutButton.textContent).toContain('Log out');
  });

  it('should render Infrastructure link', () => {
    const compiled = fixture.nativeElement;
    const infrastructureLink = compiled.querySelector('a[routerLink="/infrastructure"]');
    expect(infrastructureLink).toBeTruthy();
  });

  it('should render Experiments link', () => {
    const compiled = fixture.nativeElement;
    const experimentsLink = compiled.querySelector('a[routerLink="/experiments"]');
    expect(experimentsLink).toBeTruthy();
  });

  it('should render Results link', () => {
    const compiled = fixture.nativeElement;
    const resultsLink = compiled.querySelector('a[routerLink="/results"]');
    expect(resultsLink).toBeTruthy();
  });
});

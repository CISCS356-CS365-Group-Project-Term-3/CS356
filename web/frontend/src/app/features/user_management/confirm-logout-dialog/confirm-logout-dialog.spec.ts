import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatDialogRef} from '@angular/material/dialog';
import { ConfirmLogoutDialog } from './confirm-logout-dialog';

describe('ConfirmLogoutDialog', () => {
  let component: ConfirmLogoutDialog;
  let fixture: ComponentFixture<ConfirmLogoutDialog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConfirmLogoutDialog],
      providers: [
        { provide: MatDialogRef, useValue: MatDialogRef }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ConfirmLogoutDialog);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

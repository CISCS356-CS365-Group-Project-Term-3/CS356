import {ComponentFixture, TestBed} from '@angular/core/testing';
import { ResetPassword} from './reset-password';
import { expect, describe, it, beforeEach } from "vitest";


describe('ResetPassword', () => {
  let component: ResetPassword;
  let fixture: ComponentFixture<ResetPassword>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResetPassword],
    }).compileComponents();


    fixture = TestBed.createComponent(ResetPassword);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create the component', () => {
    const fixture = TestBed.createComponent(ResetPassword);
    const app = fixture.componentInstance;
    expect(component).toBeTruthy();
  });

  it('should create reset password form with password fields', () => {
    expect(component.resetPasswordForm.contains('password')).toBe(true);
    expect(component.resetPasswordForm.contains('reenteredPassword')).toBe(true);
  });

  it('should mark form invalid when fields are empty', () => {
    component.resetPasswordForm.setValue({
      password: '',
      reenteredPassword: '',
    });

    expect(component.resetPasswordForm.valid).toBe(false);
  });

  it('should be valid when all fields are provided correctly', () => {
    component.resetPasswordForm.setValue({
      password: 'test1234*',
      reenteredPassword: 'test1234*',
    });

    expect(component.resetPasswordForm.valid).toBe(true);
  });

  it('should be invalid when fields are not filled in correctly', () => {
    component.resetPasswordForm.setValue({
      password: 'test123',
      reenteredPassword: 'test1234*',
    });

    expect(component.resetPasswordForm.valid).toBe(false);
  });

});

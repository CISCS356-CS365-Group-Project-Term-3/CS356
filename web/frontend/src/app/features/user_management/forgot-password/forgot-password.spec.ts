import {ComponentFixture, TestBed} from '@angular/core/testing';
import { ForgotPassword} from './forgot-password';
import { expect, describe, it, beforeEach } from "vitest";


describe('ForgotPassword', () => {
  let component: ForgotPassword;
  let fixture: ComponentFixture<ForgotPassword>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ForgotPassword],
    }).compileComponents();


    fixture = TestBed.createComponent(ForgotPassword);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create the component', () => {
    const fixture = TestBed.createComponent(ForgotPassword);
    const app = fixture.componentInstance;
    expect(component).toBeTruthy();
  });

  it('should create sign up form with username, email, and password fields', () => {
    expect(component.emailForm.contains('email')).toBe(true);
  });

  it('should mark form invalid when fields are empty', () => {
    component.emailForm.setValue({
      email: '',
    });

    expect(component.emailForm.valid).toBe(false);
  });

  it('should be valid when an email is provided correctly', () => {
    component.emailForm.setValue({
      email: 'john@gmail.com',
    });

    expect(component.emailForm.valid).toBe(true);
  });

  it('should be invalid when email is invalid', () => {
    component.emailForm.setValue({
      email: 'john.com',
    });

    expect(component.emailForm.valid).toBe(false);
  });

});

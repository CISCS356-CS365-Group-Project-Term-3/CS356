import {ComponentFixture, TestBed} from '@angular/core/testing';
import { SignUp} from "./sign-up";
import { expect, describe, it, beforeEach } from "vitest";


describe('SignUp', () => {
  let component: SignUp;
  let fixture: ComponentFixture<SignUp>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SignUp],
    }).compileComponents();


    fixture = TestBed.createComponent(SignUp);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create the component', () => {
    const fixture = TestBed.createComponent(SignUp);
    const app = fixture.componentInstance;
    expect(component).toBeTruthy();
  });

  it('should create sign up form with username, email, and password fields', () => {
    expect(component.accountForm.contains('username')).toBe(true);
    expect(component.accountForm.contains('password')).toBe(true);
    expect(component.accountForm.contains('email')).toBe(true);
  });

  it('should mark form invalid when fields are empty', () => {
    component.accountForm.setValue({
      username: '',
      password: '',
      email: '',
      reenteredPassword: '',
      accountType: ''
    });

    expect(component.accountForm.valid).toBe(false);
  });

  it('should be valid when all fields are provided correctly', () => {
    component.accountForm.setValue({
      username: 'john123',
      email: 'john@gmail.com',
      password: 'test1234*',
      reenteredPassword: 'test1234*',
      accountType: 'admin'
    });

    expect(component.accountForm.valid).toBe(true);
  });

  it('should be invalid when fields are not filled in correctly', () => {
    component.accountForm.setValue({
      username: 'john123',
      email: 'john',
      password: 'test123',
      reenteredPassword: 'test1234*',
      accountType: 'admin'
    });

    expect(component.accountForm.valid).toBe(false);
  });

});

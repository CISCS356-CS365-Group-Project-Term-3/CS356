import {ComponentFixture, TestBed} from '@angular/core/testing';
import { Login } from './login';
import { expect, describe, it, beforeEach } from "vitest";
import { provideRouter } from '@angular/router';


describe('Login', () => {
    let component: Login;
    let fixture: ComponentFixture<Login>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [Login],
            providers: [provideRouter([])]
        }).compileComponents();


        fixture = TestBed.createComponent(Login);
        component = fixture.componentInstance;

        fixture.detectChanges();
    });

    it('should create the component', () => {
        const fixture = TestBed.createComponent(Login);
        const app = fixture.componentInstance;
        expect(component).toBeTruthy();
    });

    it('should create login form with username and password fields', () => {
        expect(component.loginForm.contains('username')).toBe(true);
        expect(component.loginForm.contains('password')).toBe(true);
    });

    it('should mark form invalid when fields are empty', () => {
        component.loginForm.setValue({
            username: '',
            password: ''
        });

        expect(component.loginForm.valid).toBe(false);
    });

    it('should be valid when username and password are provided', () => {
        component.loginForm.setValue({
            username: 'john123',
            password: 'test1234*'
        });

        expect(component.loginForm.valid).toBe(true);
    });

    it('should show error when fields are blank', () => {
        const control1 = component.loginForm.get('username');
        const control2 = component.loginForm.get('password');

        control1?.setValue('');
        control2?.setValue('');
        control1?.markAsTouched();
        control2?.markAsTouched();

        expect(control1?.hasError('required')).toBe(true);
        expect(control2?.hasError('required')).toBe(true);
    });

});

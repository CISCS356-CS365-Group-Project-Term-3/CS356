import {ComponentFixture, TestBed} from '@angular/core/testing';
import { LandingPage } from "./landing-page";
import { ConfirmLogoutDialog } from '../confirm-logout-dialog/confirm-logout-dialog';
import { provideRouter } from '@angular/router';
import { RouterLink} from '@angular/router';
import { expect, describe, it, beforeEach } from "vitest";


describe('LandingPage', () => {
    let component: LandingPage;
    let fixture: ComponentFixture<LandingPage>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [LandingPage,
            ConfirmLogoutDialog, RouterLink],
          providers: [
            provideRouter([])
          ]
        }).compileComponents();


        fixture = TestBed.createComponent(LandingPage);
        component = fixture.componentInstance;

        fixture.detectChanges();
    });

    it('should create the component', () => {
        const fixture = TestBed.createComponent(LandingPage);
        const app = fixture.componentInstance;
        expect(component).toBeTruthy();
    });
});

import {ComponentFixture, TestBed} from '@angular/core/testing';
import { Home} from "./home";
import { RouterLink} from '@angular/router';
import { provideRouter } from '@angular/router';
 import { expect, describe, it, beforeEach } from "vitest";


describe('Home', () => {
    let component: Home;
    let fixture: ComponentFixture<Home>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [Home, RouterLink],
          providers: [
            provideRouter([])
          ]
        }).compileComponents();
        fixture = TestBed.createComponent(Home);
        component = fixture.componentInstance;

        fixture.detectChanges();
    });

    it('should create the component', () => {
        const fixture = TestBed.createComponent(Home);
        const app = fixture.componentInstance;
        expect(component).toBeTruthy();
    });
});

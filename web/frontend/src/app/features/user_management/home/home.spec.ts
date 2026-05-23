import {ComponentFixture, TestBed} from '@angular/core/testing';
import { Home} from "./home";
 import { expect, describe, it, beforeEach } from "vitest";


describe('Home', () => {
    let component: Home;
    let fixture: ComponentFixture<Home>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [Home],
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

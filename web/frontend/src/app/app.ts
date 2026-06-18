import { Component, signal } from '@angular/core';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';
import { Navbar } from './shared/navbar/navbar';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatCardModule } from '@angular/material/card';
import { filter } from 'rxjs';

const NO_NAVBAR_ROUTES = ['/login', '/sign-up', '/forgot-password', '/reset-password', '/home'];

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    Navbar,
    MatToolbarModule,
    MatButtonModule,
    MatExpansionModule,
    MatCardModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('CS356 UI Dashboard');
  showNavbar = true;

  constructor(private router: Router) {
    // on each completed navigation, hide the navbar if the route is in the no-navbar list
    router.events.pipe(filter((e) => e instanceof NavigationEnd)).subscribe((e: any) => {
      this.showNavbar = !NO_NAVBAR_ROUTES.includes(e.urlAfterRedirects);
    });
  }
}

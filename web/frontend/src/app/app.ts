import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Navbar } from './shared/navbar/navbar';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatCardModule } from '@angular/material/card';
import { HttpClientModule } from '@angular/common/http';
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
    HttpClientModule,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss'

})
export class App {
  protected readonly title = signal('CS356 UI Dashboard');
}

import { Component } from '@angular/core';
import { Navbar } from '../../../shared/navbar/navbar';

interface ProfileDetail {
  label: string;
  value: string;
}

/** @title Profile page */
@Component({
  selector: 'app-profile',
  imports: [Navbar],
  templateUrl: 'profile.html',
  styleUrl: 'profile.scss',
  standalone: true
})
export class Profile {
  readonly profileDetails: ProfileDetail[] = [
    { label: 'Username', value: 'test' },
    { label: 'Email address', value: 'test@gmail.com' },
    { label: 'Account type', value: 'General user' }
  ];
}

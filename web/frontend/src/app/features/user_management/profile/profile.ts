import {ChangeDetectorRef, Component} from '@angular/core';
import {UserManagementService} from '../user-management-service';

interface ProfileDetail {
  label: string;
  value: string;
}

/** @title Profile page */
@Component({
  selector: 'app-profile',
  templateUrl: 'profile.html',
  styleUrl: 'profile.scss',
  standalone: true
})
export class Profile {

  username: string = '';
  email: string = '';
  accountType: string = '';
  user_role: string = '';
  user_email: string = '';

  get profileDetails(): ProfileDetail[] {
    return [
      { label: 'Username', value: this.username },
      { label: 'Email address', value: this.email },
      { label: 'Account type', value: this.user_role || this.accountType }
    ];
  }

  constructor(
    private userManagementService: UserManagementService,
    private cdr: ChangeDetectorRef
  ) {}


  ngOnInit() {
    this.getUserDetails()
  }

  getUserDetails() {
    this.userManagementService.getUserInfo().subscribe({
      next: (data: any) => {
        this.username = data.user_name;
        this.accountType = data.user_role;
        this.user_role = data.user_role;
        this.email = data.user_email;
        this.user_email = data.user_email;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error(err);
      }
    });
  }

}

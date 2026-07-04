import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Injectable} from '@angular/core';

const API_BASE_URL = '/user-management';

@Injectable({
    providedIn: "root"
})

export class UserManagementService {
  constructor(private  http: HttpClient) {}

    loginUser(user_name: string, password: string) {
    const url = `${API_BASE_URL}/auth/login`;
    const body = {
        user_name: user_name,
        password: password,
      };
      return this.http.post<string | boolean>(url, body);
    }

    verifyUser() {
    const url = `${API_BASE_URL}/auth/verify`;
    const token = localStorage.getItem('access_token');
      if (!token) throw new Error('Missing token');

        const headers = new HttpHeaders({
          Authorization: `Bearer ${token}`
        });
        return this.http.get(url, { headers });
      }


    getAllUsers() {
    const url = `${API_BASE_URL}/auth/users`;
    return this.http.get(url);
    }

    deleteUser(user_id: string) {
      const url = `${API_BASE_URL}/auth/users/delete/${user_id}`;
      return this.http.post(url, {});
    }

    resetPassword(email: string) {
      const url = `${API_BASE_URL}/auth/reset_password`;
      const body = {
        email: email,
      };
      return this.http.post(url, body)
    }

    resetPasswordConfirm(token: any, new_password: string) {
      const url = `${API_BASE_URL}/auth/reset_password/confirm`;
      if (!token) throw new Error('Missing token');
      const body = {
        token,
        new_password: new_password,
      };
      return this.http.post(url, body)
    }

    getUserInfo() {
      const url = `${API_BASE_URL}/users/me`;
      const token = localStorage.getItem('access_token');
      if (!token) throw new Error('Missing token');

      const headers = new HttpHeaders({
        Authorization: `Bearer ${token}`
      });
      return this.http.get(url, { headers });
    }

    registerUser( username: string, password: string, confirmedPassword: string, email: string, role: string) {
      const url = `${API_BASE_URL}/auth/register`;

      const body = {
        user_name: username,
        password: password,
        confirm_password: confirmedPassword,
        user_email: email,
        user_role: role,
      };

      return this.http.post(url, body)
    }
}

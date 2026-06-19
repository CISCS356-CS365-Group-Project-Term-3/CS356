import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

const VERIFY_URL = 'http://localhost:8000/auth/verify';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private storageKey = 'access_token';

  constructor(private http: HttpClient) {}

  getToken(): string | null {
    return localStorage.getItem(this.storageKey);
  }

  setToken(token: string) {
    localStorage.setItem(this.storageKey, token);
  }

  clearToken() {
    localStorage.removeItem(this.storageKey);
  }

  /**
   * Calls the backend /auth/verify endpoint with the stored token.
   * Returns an observable that resolves to true if token is valid, false otherwise.
   */
  verifyToken(): Observable<boolean> {
    const token = this.getToken();
    if (!token) return of(false);

    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
    return this.http.get<{ user_id: number, user_role: string }>(VERIFY_URL, { headers })
      .pipe(
        map(() => true),
        catchError(() => of(false))
      );
  }

  getUserInfo(): Observable<{ user_id: number, user_role: string } | null> {
    const token = this.getToken();
    if (!token) return of(null);
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
    return this.http.get<{ user_id: number, user_role: string }>(VERIFY_URL, { headers }).pipe(catchError(() => of(null)));
  }
}


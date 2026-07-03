import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

const API_BASE_URL = '/user-management';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private storageKey = 'access_token';

  constructor(private http: HttpClient) {}

  /**
   * retrieves the current token from local storage.
   */
  getToken(): string | null {
    return localStorage.getItem(this.storageKey);
  }

  /**
   * clears the invalid or expired token from local storage.
   */
  clearToken(): void {
    localStorage.removeItem(this.storageKey);
  }

  /**
   * calls the backend /auth/verify endpoint with the stored token.
   * Returns an observable that resolves to true if token is valid, false otherwise.
   */
  verifyToken(): Observable<boolean> {
    const token = this.getToken();
    if (!token) {
      return of(false);
    }

    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
    return this.http.get<{ user_id: number, user_role: string }>(`${API_BASE_URL}/auth/verify`, { headers })
      .pipe(
        map(() => {
          return true;
        }),
        catchError(() => {
          return of(false);
        })
      );
  }
}

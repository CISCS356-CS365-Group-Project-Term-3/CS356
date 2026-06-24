import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { inject } from '@angular/core';
import { map } from 'rxjs/operators';

/**
 * Functional guard that verifies JWT using the backend verify API.
 */
export const AuthGuard: CanActivateFn = (_route, _state) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  const token = auth.getToken();
  if (!token) {
    console.log('[AuthGuard] ✗ Route guard blocked: No token in localStorage');
    return router.createUrlTree(['/login']);
  }

  console.log('[AuthGuard] Verifying token with backend...');
  return auth.verifyToken().pipe(map(valid => {
    if (valid) {
      console.log('[AuthGuard] ✓ Route guard PASSED - User authenticated, allowing navigation');
      return true;
    }
    console.log('[AuthGuard] ✗ Route guard BLOCKED - Token verification failed, redirecting to login');
    return router.createUrlTree(['/login']);
  }));
};


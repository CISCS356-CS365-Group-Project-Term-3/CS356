import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { inject } from '@angular/core';
import { map } from 'rxjs/operators';

/**
 * Functional guard that verifies JWT using the backend verify API.
 * Wipes out dead tokens to prevent endless validation loops.
 */
export const AuthGuard: CanActivateFn = (_route, _state) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  const token = auth.getToken();
  if (!token) {
    return router.createUrlTree(['/login']);
  }

  return auth.verifyToken().pipe(
    map(valid => {
      if (valid) {
        return true;
      }

      // token gets deleted if invalid, so user is redirected to login page
      auth.clearToken();
      return router.createUrlTree(['/login']);
    })
  );
};

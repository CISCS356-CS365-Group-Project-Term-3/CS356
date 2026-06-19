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
    // redirect to login
    return router.createUrlTree(['/login']);
  }

  // verify with backend
  return auth.verifyToken().pipe(map(valid => {
    if (valid) return true;
    return router.createUrlTree(['/login']);
  }));
};


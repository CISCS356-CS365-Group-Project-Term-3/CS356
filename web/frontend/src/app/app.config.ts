import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

import { routes } from './app.routes';
import { mockBackendInterceptor } from './features/results/testing/mock-backend.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    // TODO: remove withInterceptors([mockBackendInterceptor]) once the real backend is reachable
    provideHttpClient(withInterceptors([mockBackendInterceptor])),
  ]
};

import { HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { of } from 'rxjs';
import { MOCK_RESULT_SUMMARIES } from './mock-results';
import { MOCK_INFRASTRUCTURE_CONFIG } from './mock-infrastructure-config';

// mcok for using to test frontend without docker
export const mockBackendInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.url.endsWith('/experiment-management/experiments-results')) {
    return of(new HttpResponse({ status: 200, body: MOCK_RESULT_SUMMARIES }));
  }

  if (req.url.endsWith('/infra/rest/get_active_ui_options')) {
    return of(new HttpResponse({ status: 200, body: MOCK_INFRASTRUCTURE_CONFIG }));
  }

  return next(req);
};

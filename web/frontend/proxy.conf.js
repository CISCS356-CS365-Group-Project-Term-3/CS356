const USER_MGMT     = 'http://127.0.0.1:5001';
const EXPERIMENT_MGMT = 'http://127.0.0.1:5000';
const INFRA_MGMT    = 'http://127.0.0.1:5002';

module.exports = {
  '/user-management': {
    target: USER_MGMT,
    secure: false,
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/user-management/, '')
  },
  '/experiment-management': {
    target: EXPERIMENT_MGMT,
    secure: false,
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/experiment-management/, '')
  },
  '/infra': {
    target: INFRA_MGMT,
    secure: false,
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/infra/, '')
  }
};

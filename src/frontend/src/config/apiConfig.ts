// Extend Window interface to include ENV_CONFIG
declare global {
  interface Window {
    ENV_CONFIG?: {
      TOY_SERVICE_URL?: string;
      TRIP_SERVICE_URL?: string;
      DEMO_DATA_API_URL?: string;
    };
  }
}

// Runtime configuration loaded from env-config.js (set at container start) or build-time env vars
export const API_CONFIG = {
  TOY_SERVICE_BASE_URL: window.ENV_CONFIG?.TOY_SERVICE_URL || import.meta.env.VITE_TOY_SERVICE_URL || 'http://localhost:8001',
  TRIP_SERVICE_BASE_URL: window.ENV_CONFIG?.TRIP_SERVICE_URL || import.meta.env.VITE_TRIP_SERVICE_URL || 'http://localhost:8002',
  DEMO_DATA_API_URL: window.ENV_CONFIG?.DEMO_DATA_API_URL || import.meta.env.VITE_DEMO_DATA_API_URL || 'http://localhost:8010',
};

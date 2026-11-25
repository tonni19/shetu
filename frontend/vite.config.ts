// FILE:        frontend/vite.config.ts
// PURPOSE:     Settings for Vite, the tool that serves the React app while we develop and builds
//              it for release. The important part is the proxy to the FastAPI backend.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  the backend running on http://127.0.0.1:8000 (backend/README.md, Maruf, T1)
// USED BY:     `npm run dev`, `npm run build`, `npm run preview`
// STATUS:      REAL
// DATA:        No data lives here.
// AI NOTE:     Keep the proxy. The browser talks only to the Vite address (localhost:5173), and
//              Vite forwards /api and /healthz to the backend. To the browser it is one site, so the
//              session cookie that POST /api/login sets is stored and sent back automatically.
//              Without the proxy, every fetch would need `credentials: "include"` and the backend's
//              CORS list (SHETU_CORS_ORIGINS) would have to match exactly. This is the setting
//              backend/README.md asks for ("For the React app").

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const BACKEND = "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Fail loudly instead of silently moving to 5174: the backend's CORS list and the planned
    // Selenium flows (Nazha) expect 5173.
    strictPort: true,
    proxy: {
      "/api": BACKEND,
      "/healthz": BACKEND,
    },
  },
  preview: {
    port: 4173,
    proxy: {
      "/api": BACKEND,
      "/healthz": BACKEND,
    },
  },
});

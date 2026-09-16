import { defineConfig } from "vite";

export default defineConfig(({ command }) => ({
  base: command === "build" ? (process.env.VITE_BASE ?? "/HKHS-Code-Search/") : "/",
  server: { proxy: { "/api": "http://127.0.0.1:8000" } },
}));

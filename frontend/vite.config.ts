import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

/**
 * StoryTime Phase 13B frontend build config.
 *
 * `base: "./"` makes the production build use relative asset paths, so the
 * static output works from a subpath, from a static host (GitHub Pages,
 * Netlify, Vercel static export), or opened from the local filesystem — no
 * server rewrites required. This matches the Phase 13B static-shell scope.
 */
export default defineConfig({
  base: "./",
  plugins: [react()],
  build: {
    outDir: "dist",
    sourcemap: false,
  },
});

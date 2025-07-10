// spacetrack/vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { viteStaticCopy } from "vite-plugin-static-copy";

const cesiumPath = "node_modules/cesium/Build/Cesium";

export default defineConfig({
  plugins: [
    react(),
    viteStaticCopy({
      targets: [
        { src: `${cesiumPath}/Workers`,            dest: "cesium" },
        { src: `${cesiumPath}/Assets`,             dest: "cesium" },
        { src: `${cesiumPath}/ThirdParty`,         dest: "cesium" },
        { src: `${cesiumPath}/Widgets`,            dest: "cesium" }
      ]
    })
  ],
  resolve: {
    alias: {
      cesium: path.resolve(__dirname, cesiumPath)
    }
  },
  define: {
    // Cesium looks here for those static folders
    CESIUM_BASE_URL: JSON.stringify("/cesium")
  },
  server: {
    port: 5173
  }
});

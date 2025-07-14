// spacetrack/src/App.jsx
import { useEffect, useRef, useState } from "react";
import {
  Viewer as CesiumViewer,
  Cartesian3,
  Color,
  ScreenSpaceEventType
} from "cesium";
import "cesium/Widgets/widgets.css";
import * as satellite from "satellite.js";
import axios from "axios";
import RiskInfoPanel from "./components/RiskInfoPanel";
import * as Cesium from "cesium";
// Cesium Ion token comes from the VITE_CESIUM_TOKEN entry in .env
Cesium.Ion.defaultAccessToken = import.meta.env.VITE_CESIUM_TOKEN;



const BACKEND_TLES     = "http://localhost:5050/api/tles";
const BACKEND_PREDICT  = "http://localhost:5050/api/predict";

/* ── helper ─────────────────────────────────────────────── */
function parseTLE(text) {
  const l = text.split("\n").map((x) => x.trim()).filter(Boolean);
  const out = [];
  for (let i = 0; i < l.length - 1; i++) {
    if (l[i].startsWith("1 ") && l[i + 1].startsWith("2 ")) {
      out.push({ line1: l[i], line2: l[i + 1] });
      i++;
    }
  }
  return out;
}

/* ── component ──────────────────────────────────────────── */
export default function App() {
  const containerRef  = useRef(null);
  const viewerRef     = useRef(null);   // keep Cesium viewer instance
  const objectsRef    = useRef([]);     // [{id,risk,ttc}]
  const [selected, setSelected] = useState(null);

  /* create viewer & load data once */
  useEffect(() => {
    if (!containerRef.current) return;

    // 1) init Cesium viewer (no Resium)
    viewerRef.current = new CesiumViewer(containerRef.current, {
      shouldAnimate: true,
      animation: false,
      timeline: false
    });
    const viewer = viewerRef.current;

    /* 2) fetch data & plot */
    (async () => {
      try {
        // 2-A: raw TLEs
        const { data: tleRes } = await axios.get(BACKEND_TLES);
        if (tleRes.error) throw new Error(tleRes.error);
        const tleList = parseTLE(tleRes.tle_data).slice(0, 150);

        // 2-B: risk predictions
        const { data: predRes } = await axios.post(BACKEND_PREDICT, {
          tles: tleList
        });
        if (predRes.error) throw new Error(predRes.error);
        const risks = predRes.risks;
        const ttcs  = predRes.ttcs || [];
        /* ─── DIAGNOSTIC: log histogram + sample ids ─── */
        const buckets = { ">0.9": 0, "0.8–0.9": 0, "0.7–0.8": 0, "0.6–0.7": 0, "<0.6": 0 };
        risks.forEach((r) => {
          if (r > 0.9) buckets[">0.9"]++;
          else if (r > 0.8) buckets["0.8–0.9"]++;
          else if (r > 0.7) buckets["0.7–0.8"]++;
          else if (r > 0.6) buckets["0.6–0.7"]++;
          else buckets["<0.6"]++;
        });
        console.table(buckets);                     // ← see distribution
        console.log("first 20 risks:", risks.slice(0, 20));
        /* ────────────────────────────────────────────── */

        // 2-C: propagate + add entities
        const now  = new Date();
        const objs = [];

        tleList.forEach((tle, i) => {
          try {
            const satrec = satellite.twoline2satrec(tle.line1, tle.line2);
            const pv     = satellite.propagate(satrec, now);
            if (!pv.position) return;

            const gmst = satellite.gstime(now);
            const geo  = satellite.eciToGeodetic(pv.position, gmst);
            const lon  = satellite.degreesLong(geo.longitude);
            const lat  = satellite.degreesLat(geo.latitude);
            const alt  = geo.height * 1000; // km→m

            const risk = risks[i];
            const ttc  = ttcs[i];

            viewer.entities.add({
              id: satrec.satnum.toString(),
              position: Cartesian3.fromDegrees(lon, lat, alt),
              point: {
                pixelSize: 7,
                color:
                  risk > 0.9 ? Color.RED :
                  risk > 0.5 ? Color.ORANGE :
                  Color.GREEN,
                outlineColor: Color.BLACK,
                outlineWidth: 1
              },
              description: `Risk ${(risk * 100).toFixed(1)}%`
            });

            objs.push({ id: satrec.satnum.toString(), risk, ttc });
          } catch {/* ignore bad TLE */}
        });

        objectsRef.current = objs;
      } catch (e) {
        console.error("Load/plot error:", e);
      }
    })();

    /* 3) click handler */
    viewer.screenSpaceEventHandler.setInputAction(
      (click) => {
        const picked = viewer.scene.pick(click.position);
        if (picked?.id) {
          const obj = objectsRef.current.find((o) => o.id === picked.id.id);
          if (obj) setSelected(obj);
        }
      },
      ScreenSpaceEventType.LEFT_CLICK
    );

    /* cleanup */
    return () => viewer.destroy();
  }, []);

  /* ── render ───────────────────────────────────────────── */
  return (
    <div style={{ width: "100vw", height: "100vh", position: "relative" }}>
      <div ref={containerRef} style={{ width: "100%", height: "100%" }} />
      <RiskInfoPanel info={selected} onClose={() => setSelected(null)} />
    </div>
  );
}



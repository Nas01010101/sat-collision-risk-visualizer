# sat-collision-risk-visualizer

A full-stack tool for visualizing and predicting satellite collision risk.

## Features (In progress)

- ML model predicts collision risk using miss distance, time to closest approach, and relative speed.
- Flask backend serves TLE data and risk predictions via REST API.
- React frontend with CesiumJS displays satellites and debris on a 3D globe, color-coded by risk.

## Setup

The Cesium viewer requires an [Ion access token](https://cesium.com/ion/) which
should be provided through Vite's environment system. Inside the `spacetrack`
folder create a `.env` file and add your token:

```env
VITE_CESIUM_TOKEN=YOUR_TOKEN_HERE
```

`vite.config.js` loads this variable automatically so the React code can access
it via `import.meta.env.VITE_CESIUM_TOKEN`.


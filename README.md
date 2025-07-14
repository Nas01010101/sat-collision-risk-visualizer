# sat-collision-risk-visualizer

A full-stack tool for visualizing and predicting satellite collision risk.

## Project layout

- `backend/` – Flask API serving recent TLEs from Space-Track and ML risk
  predictions.
- `ml/` – scripts and notebooks used to build the classifier. The trained
  model and processed features are checked in.
- `spacetrack/` – React + Vite front‑end which renders a 3D globe with
  CesiumJS.
- `package.json` – small Node helper utilities (e.g. `satellite.js`).

## Features (In progress)

- ML model predicts collision risk using miss distance, time to closest approach, and relative speed.
- Flask backend serves TLE data and risk predictions via REST API.
- React frontend with CesiumJS displays satellites and debris on a 3D globe, color-coded by risk.

## Prerequisites

- Python 3.11 and [pip](https://pip.pypa.io/)
- [Node.js](https://nodejs.org/) (v18+ recommended)

Install the Python dependencies into a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r ml/requirements.txt flask flask-cors
```

Install the Node dependencies (for the React frontend):

```bash
cd spacetrack
npm install
cd ..
```

## Environment variables

The application requires credentials for Space-Track and a Cesium ion token. Set
these before running either component:

```bash
export SPACE_TRACK_USER=<your-username>
export SPACE_TRACK_PASS=<your-password>
export CESIUM_ION_TOKEN=<your-cesium-token>
```

**Security tip:** Never commit these tokens or credentials to version control.

## Running the app

1. Start the Flask backend:

   ```bash
   source venv/bin/activate
   python backend/spacetrack_server.py
   ```

   It listens on `http://localhost:5050`.

2. In another terminal, run the React frontend:

   ```bash
   cd spacetrack
   npm run dev
   ```

   Vite serves the UI at `http://localhost:5173`.

## Retraining the model (optional)

If you wish to rebuild the risk model from scratch:

```bash
cd ml
python fetch_cdm.py               # downloads public CDMs (needs Space-Track creds)
python train.py                   # trains and saves model_risk.pkl
cd ..
```

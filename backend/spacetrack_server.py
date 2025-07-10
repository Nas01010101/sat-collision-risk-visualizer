#!/usr/bin/env python
"""
Minimal Flask proxy for Space-Track TLEs + ML risk prediction
-------------------------------------------------------------
• Reads SPACE_TRACK_USER / SPACE_TRACK_PASS from env vars
• Adds CORS headers so React (port 5173) can call it
• GET  /api/tles     → JSON { "tle_data": "...raw TLE text..." }
• POST /api/predict  → JSON { "risks": [0.12, 0.87, …] }
• GET  /health       → "OK"
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from requests.sessions import Session

# Import your ML glue function (returns list of risk probabilities)
from ml_model import predict_risks

# Read Space-Track credentials from environment
USERNAME = os.getenv("SPACE_TRACK_USER")
PASSWORD = os.getenv("SPACE_TRACK_PASS")
if not USERNAME or not PASSWORD:
    raise RuntimeError("Set env vars SPACE_TRACK_USER and SPACE_TRACK_PASS before running.")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def fetch_latest_tles() -> str:
    """
    Logs in to Space-Track and fetches the latest TLEs
    (one per NORAD ID, from the last 30 days), returning raw TLE text.
    """
    with Session() as session:
        # 1) Authenticate
        login_resp = session.post(
            "https://www.space-track.org/ajaxauth/login",
            data={"identity": USERNAME, "password": PASSWORD}
        )
        if login_resp.status_code != 200:
            raise RuntimeError(f"Space-Track login failed: {login_resp.text[:120]}…")

        # 2) Fetch TLEs
        tle_url = (
            "https://www.space-track.org/basicspacedata/query/"
            "class/tle_latest/ORDINAL/1/EPOCH/%3Enow-30/"
            "orderby/NORAD_CAT_ID%20asc/format/tle/"
        )
        tle_resp = session.get(tle_url)
        if tle_resp.status_code != 200:
            raise RuntimeError(f"TLE fetch failed: {tle_resp.text[:120]}…")

        return tle_resp.text


@app.route("/api/tles", methods=["GET"])
def api_tles():
    try:
        raw_tle = fetch_latest_tles()
        return jsonify({"tle_data": raw_tle})
    except Exception as exc:
        app.logger.error("ERROR in /api/tles → %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    Expects JSON:
      { "tles": [ { "line1": "...", "line2": "..." }, … ] }
    Returns JSON:
      { "risks": [0.12, 0.87, …] }
    """
    data = request.get_json(force=True, silent=True)
    if not data or "tles" not in data or not isinstance(data["tles"], list):
        return jsonify({"error": "Request JSON must include a list under 'tles'"}), 400

    try:
        risks = predict_risks(data["tles"])
        return jsonify({"risks": risks})
    except Exception as exc:
        app.logger.error("ERROR in /api/predict → %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


if __name__ == "__main__":
    # By default listens at http://127.0.0.1:5050
    # Change host to "0.0.0.0" to expose externally
    app.run(host="127.0.0.1", port=5050, debug=True)

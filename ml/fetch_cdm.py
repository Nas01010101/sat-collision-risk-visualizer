"""
Download public Conjunction Data Messages (CDMs) from Space-Track
and save them as Parquet for ML work.

Usage:
    $ python fetch_cdm.py          # last 90 days → raw/cdm_<date>.parquet
    $ DAYS=365 python fetch_cdm.py # customise look-back window
"""
import os
import pandas as pd
import requests
from datetime import datetime, timedelta
from requests.sessions import Session
from io import StringIO  

USER = os.getenv("SPACE_TRACK_USER")
PW   = os.getenv("SPACE_TRACK_PASS")
DAYS = int(os.getenv("DAYS", "90"))

assert USER and PW, "export SPACE_TRACK_USER and SPACE_TRACK_PASS before running"

def space_track_login() -> Session:
    s = Session()
    resp = s.post(
        "https://www.space-track.org/ajaxauth/login",
        data={"identity": USER, "password": PW},
        timeout=20,
    )
    resp.raise_for_status()
    return s

def fetch_cdm_csv(sess: Session) -> str:
    since = (datetime.utcnow() - timedelta(days=DAYS)).strftime("%Y-%m-%d")
    url = (
        "https://www.space-track.org/basicspacedata/query/"
        "class/cdm_public/"
        f"TCA/%3E{since}/"
        "orderby/TCA%20desc/"
        "format/csv"
    )
    resp = sess.get(url, timeout=60)
    resp.raise_for_status()
    return resp.text

def main():
    print(f"Downloading CDMs for last {DAYS} days …")
    sess = space_track_login()
    csv_text = fetch_cdm_csv(sess)

    df = pd.read_csv(StringIO(csv_text))
    out_path = f"raw/cdm_{datetime.utcnow():%Y%m%d_%H%M}.parquet"
    df.to_parquet(out_path, index=False)
    print("Saved →", out_path, "| rows:", len(df))

if __name__ == "__main__":
    main()


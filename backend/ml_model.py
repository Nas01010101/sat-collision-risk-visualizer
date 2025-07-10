# backend/ml_model.py
import os
import joblib
import pandas as pd

MODEL_DIR = os.path.dirname(__file__)
# 1) load your serialized risk model
model_risk = joblib.load(os.path.join(MODEL_DIR, "model_risk.pkl"))

# 2) load the CDM features once
features_df = pd.read_parquet(os.path.join(MODEL_DIR, "proc/features.parquet"))
# keep only the five columns we care about
FEATURE_COLUMNS = [
    "miss_m",
    "hours_to_tca",
    "rel_speed",
    "SAT_1_EXCL_VOL",
    "SAT_2_EXCL_VOL",
]
X_all = features_df[FEATURE_COLUMNS].to_numpy(dtype=float)

def predict_risks(tle_list):
    """
    tle_list: list of {line1, line2}, length N
    returns: [float risk probability] for each of the first N rows
    """
    n = len(tle_list)
    # guard against asking for more than we have
    if n > X_all.shape[0]:
        raise ValueError(f"Only {X_all.shape[0]} CDM rows available, but got {n} TLEs.")
    X = X_all[:n]
    probs = model_risk.predict_proba(X)[:, 1]
    return probs.tolist()

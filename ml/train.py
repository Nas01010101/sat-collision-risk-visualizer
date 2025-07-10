#!/usr/bin/env python
"""
Train a binary classifier on the CDM features and serialize the trained model.
"""
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report

def main():
    # 1. Load preprocessed features
    df = pd.read_parquet("proc/features.parquet")
    X, y = df.drop(columns="y"), df["y"]

    # 2. Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # 3. Initialize & fit classifier
    clf = XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        base_score=0.5   # ensures non-zero probabilities
    )

    clf.fit(X_train, y_train)

    # 4. Evaluate
    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))

    # 5. Serialize model
    out_path = os.path.join(os.path.dirname(__file__), "model_risk.pkl")
    joblib.dump(clf, out_path)
    print(f"\nTrained model saved to: {out_path}")

if __name__ == "__main__":
    main()

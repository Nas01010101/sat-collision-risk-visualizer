# Machine Learning Workflow

This folder contains simple scripts used to train the collision–risk model.

## Setup

Create a Python environment with the dependencies listed in `requirements.txt` (or
use `environment.yml` with conda).

```bash
pip install -r requirements.txt
# or
conda env create -f environment.yml
```

## Download the CDM data

`fetch_cdm.py` downloads public Conjunction Data Messages from Space-Track and
saves them under `raw/` as a parquet file. Export your Space‑Track credentials
and run the script:

```bash
export SPACE_TRACK_USER=<username>
export SPACE_TRACK_PASS=<password>
python fetch_cdm.py            # downloads last 90 days
DAYS=365 python fetch_cdm.py   # customise look-back window
```

## Generate training features

`make_features.py` transforms the raw CDM file into a features table. It expects
TLE data in memory and writes `proc/features.parquet`.

```bash
python make_features.py
```

## Train the model

`train.py` reads `proc/features.parquet` and outputs the trained model
`model_risk.pkl`.

```bash
python train.py
```

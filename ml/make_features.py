#!/usr/bin/env python
import numpy as np
from sgp4.api import Satrec, WGS72

def compute_features_for_tles(tle_list):
    feats = []
    for tle in tle_list:
        sat = Satrec.twoline2rv(tle["line1"], tle["line2"], WGS72)
        # sgp4 ≥2.24 uses no_kozai; older versions use no
        mean_motion = getattr(sat, "no_kozai", sat.no)
        feats.append([sat.ecco, sat.inclo, sat.nodeo, sat.argpo, mean_motion])
    X = np.asarray(feats, dtype=float)
    return X, X

import numpy as np

_rng = np.random


def sample_sphere() -> (int, int, int):
    while True:
        coords = _rng.normal(size=3)
        radius_sq = np.sum(np.square(coords))
        if radius_sq != 0:
            normalized = coords / np.sqrt(radius_sq)
            return tuple(normalized)

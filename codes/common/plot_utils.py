import numpy as np
import os
from matplotlib import cm
from matplotlib.animation import PillowWriter

# Meshgrid generator
def generate_meshgrid(strike_range=(80, 120), maturity_range=(0.1, 2.0), num=50):
    strikes = np.linspace(*strike_range, num)
    maturities = np.linspace(*maturity_range, num)
    K, T = np.meshgrid(strikes, maturities)
    return K, T, strikes, maturities

# Synthetic implied volatility surface
def implied_vol_surface(K, T):
    return 0.15 + 0.25 * np.exp(-T) * np.exp(-((K-100)/15)**2)

# Synthetic local volatility surface
def local_vol_surface(K, T):
    return 0.18 + 0.12 * np.exp(-T) * np.exp(-((K-100)/18)**2)

# Save matplotlib animation as GIF
def save_gif(anim, path, fps=20):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    anim.save(path, writer=PillowWriter(fps=fps)) 
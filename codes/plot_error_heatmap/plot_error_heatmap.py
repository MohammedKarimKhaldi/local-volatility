import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image

strikes = np.linspace(80, 120, 50)
maturities = np.linspace(0.1, 2.0, 50)
K, T = np.meshgrid(strikes, maturities)

# Synthetic pricing error: higher at edges, lower at center
error = 0.01 + 0.04 * (np.abs(K-100)/20 + np.abs(T-1)/1.5)

fig, ax = plt.subplots(figsize=(7, 5))
c = ax.pcolormesh(K, T, error, cmap='Reds', shading='auto')
fig.colorbar(c, ax=ax, label='Pricing Error')
ax.set_xlabel('Strike')
ax.set_ylabel('Maturity')
ax.set_title('Pricing Error Heatmap')

os.makedirs('../../assets', exist_ok=True)
png_path = '../../assets/error_heatmap.png'
gif_path = '../../assets/error_heatmap.gif'
plt.savefig(png_path, format='png')
plt.close(fig)

# Convert PNG to GIF
im = Image.open(png_path)
im.save(gif_path, format='GIF') 
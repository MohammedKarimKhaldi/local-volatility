import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, PillowWriter
import os

# Synthetic data for local volatility surface
strikes = np.linspace(80, 120, 50)
maturities = np.linspace(0.1, 2.0, 50)
K, T = np.meshgrid(strikes, maturities)
# Example: local vol is flatter but still has smile/term structure
local_vol = 0.18 + 0.12 * np.exp(-T) * np.exp(-((K-100)/18)**2)

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111, projection='3d')
surf = [ax.plot_surface(K, T, local_vol, cmap=cm.plasma, edgecolor='none')]
ax.set_xlabel('Strike')
ax.set_ylabel('Maturity')
ax.set_zlabel('Local Volatility')
ax.set_title('Local Volatility Surface')

# Animation function
def update(frame):
    ax.view_init(elev=30, azim=frame)
    return surf

# Create animation
anim = FuncAnimation(fig, update, frames=np.arange(0, 360, 4), interval=50, blit=False)

# Ensure assets directory exists
os.makedirs('../../assets', exist_ok=True)
# Save as GIF
anim.save('../../assets/local_vol_surface.gif', writer=PillowWriter(fps=20))
plt.close(fig) 
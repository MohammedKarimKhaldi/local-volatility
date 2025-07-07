import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from plot_utils import generate_meshgrid, implied_vol_surface, save_gif

K, T, _, _ = generate_meshgrid()
implied_vol = implied_vol_surface(K, T)

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111, projection='3d')
surf = [ax.plot_surface(K, T, implied_vol, cmap=cm.viridis, edgecolor='none')]
ax.set_xlabel('Strike')
ax.set_ylabel('Maturity')
ax.set_zlabel('Implied Volatility')
ax.set_title('Implied Volatility Surface')

def update(frame):
    ax.view_init(elev=30, azim=frame)
    return surf

anim = FuncAnimation(fig, update, frames=range(0, 360, 4), interval=50, blit=False)
save_gif(anim, 'assets/implied_vol_surface.gif', fps=20)
plt.close(fig) 
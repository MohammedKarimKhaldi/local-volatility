import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

strikes = np.linspace(80, 120, 100)
times = np.linspace(0.1, 2.0, 20)

# Synthetic forward smile: smile flattens and shifts over time
forward_vol = lambda K, t: 0.18 + 0.18 * np.exp(-t) * np.exp(-((K-100-5*np.sin(2*np.pi*t/2))/15)**2)

fig, ax = plt.subplots(figsize=(7, 5))
line, = ax.plot([], [], lw=2)
text = ax.text(0.05, 0.95, '', transform=ax.transAxes, va='top')
ax.set_xlim(80, 120)
ax.set_ylim(0.1, 0.5)
ax.set_xlabel('Strike')
ax.set_ylabel('Forward Volatility')
ax.set_title('Forward Smile Evolution')

# Animation function
def update(i):
    t = times[i]
    fv = forward_vol(strikes, t)
    line.set_data(strikes, fv)
    text.set_text(f'Time = {t:.2f} yr')
    return line, text

anim = FuncAnimation(fig, update, frames=len(times), interval=200, blit=True)
os.makedirs('assets', exist_ok=True)
anim.save('assets/forward_smile_evolution.gif', writer=PillowWriter(fps=5))
plt.close(fig) 
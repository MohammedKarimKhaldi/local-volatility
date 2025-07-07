import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

strikes = np.linspace(80, 120, 100)
maturities = np.linspace(0.1, 2.0, 6)  # 6 maturities

# Synthetic implied and local vol surfaces
implied_vol = lambda K, T: 0.15 + 0.25 * np.exp(-T) * np.exp(-((K-100)/15)**2)
local_vol = lambda K, T: 0.18 + 0.12 * np.exp(-T) * np.exp(-((K-100)/18)**2)

fig, ax = plt.subplots(figsize=(7, 5))

lines = []
for _ in range(2):
    line, = ax.plot([], [], lw=2)
    lines.append(line)
text = ax.text(0.05, 0.95, '', transform=ax.transAxes, va='top')

ax.set_xlim(80, 120)
ax.set_ylim(0.1, 0.5)
ax.set_xlabel('Strike')
ax.set_ylabel('Volatility')
ax.set_title('Implied vs Local Volatility Slices')

# Animation function
def update(i):
    T = maturities[i]
    iv = implied_vol(strikes, T)
    lv = local_vol(strikes, T)
    lines[0].set_data(strikes, iv)
    lines[0].set_label('Implied Vol')
    lines[1].set_data(strikes, lv)
    lines[1].set_label('Local Vol')
    text.set_text(f'Maturity = {T:.2f} yr')
    ax.legend(loc='upper right')
    return lines + [text]

anim = FuncAnimation(fig, update, frames=len(maturities), interval=1000, blit=True)
os.makedirs('assets', exist_ok=True)
anim.save('assets/slice_comparison.gif', writer=PillowWriter(fps=1))
plt.close(fig) 
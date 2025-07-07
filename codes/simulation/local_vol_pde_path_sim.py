import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

np.random.seed(42)
Npaths = 20
Nsteps = 100
T = 1.0
S0 = 100
r = 0.0

times = np.linspace(0, T, Nsteps)
dt = times[1] - times[0]

# Synthetic local vol function
def local_vol(S, t):
    return 0.18 + 0.12 * np.exp(-t) * np.exp(-((S-100)/18)**2)

paths = np.zeros((Npaths, Nsteps))
paths[:, 0] = S0
for i in range(1, Nsteps):
    t = times[i-1]
    vol = local_vol(paths[:, i-1], t)
    dW = np.random.randn(Npaths) * np.sqrt(dt)
    paths[:, i] = paths[:, i-1] * np.exp((r - 0.5 * vol**2) * dt + vol * dW)

fig, ax = plt.subplots(figsize=(7, 5))
lines = [ax.plot([], [], lw=1, alpha=0.7)[0] for _ in range(Npaths)]
ax.set_xlim(0, T)
ax.set_ylim(np.min(paths)*0.95, np.max(paths)*1.05)
ax.set_xlabel('Time')
ax.set_ylabel('Price')
ax.set_title('Local Volatility Model Path Simulation')

# Animation function
def update(i):
    for j, line in enumerate(lines):
        line.set_data(times[:i+1], paths[j, :i+1])
    return lines

anim = FuncAnimation(fig, update, frames=Nsteps, interval=50, blit=True)
os.makedirs('assets', exist_ok=True)
anim.save('assets/local_vol_pde_path_sim.gif', writer=PillowWriter(fps=20))
plt.close(fig) 
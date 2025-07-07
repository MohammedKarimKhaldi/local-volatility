import numpy as np
import matplotlib.pyplot as plt

# Parameters
r = 0.05
T_max = 1.0
K_min, K_max = 50, 150
nK, nT = 100, 50
K = np.linspace(K_min, K_max, nK)
T = np.linspace(0, T_max, nT)
dK = K[1] - K[0]
dT = T[1] - T[0]

# Synthetic local volatility surface (smile)
def sigma_loc(K, T):
    return 0.2 + 0.3 * np.exp(-((K-100)/20)**2) * (1 - T)

# Initial condition: European call payoff at T=0
S0 = 100
payoff = np.maximum(K - S0, 0)
C = np.zeros((nT, nK))
C[0, :] = payoff

# Finite difference (explicit Euler)
for j in range(nT-1):
    for i in range(1, nK-1):
        sig = sigma_loc(K[i], T[j])
        dC_dK = (C[j, i+1] - C[j, i-1]) / (2*dK)
        d2C_dK2 = (C[j, i+1] - 2*C[j, i] + C[j, i-1]) / (dK**2)
        C[j+1, i] = C[j, i] + dT * (0.5 * sig**2 * K[i]**2 * d2C_dK2 - r * K[i] * dC_dK)
    # Boundary conditions
    C[j+1, 0] = 0
    C[j+1, -1] = K_max - S0 * np.exp(-r * T[j+1])

# Plot option price surface
KK, TT = np.meshgrid(K, T)
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(KK, TT, C, cmap='viridis')
ax.set_xlabel('Strike K')
ax.set_ylabel('Maturity T')
ax.set_zlabel('Call Price')
ax.set_title('Option Price Surface (Dupire PDE, Local Volatility)')
plt.tight_layout()
plt.show() 
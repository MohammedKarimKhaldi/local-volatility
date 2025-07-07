import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline

# Synthetic implied volatility surface
def implied_vol(K, T):
    return 0.2 + 0.3 * np.exp(-((K-100)/20)**2) * (1 - T)

K = np.linspace(50, 150, 50)
T = np.linspace(0.05, 1.0, 20)
KK, TT = np.meshgrid(K, T)
IV = implied_vol(KK, TT)

# Black-Scholes price (for call)
def bs_price(S, K, T, r, sigma):
    from scipy.stats import norm
    d1 = (np.log(S/K) + (r+0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

S0 = 100
r = 0.05
C = np.zeros_like(IV)
for i in range(len(T)):
    for j in range(len(K)):
        C[i, j] = bs_price(S0, K[j], T[i], r, IV[i, j])

# Interpolate option prices
C_spline = RectBivariateSpline(T, K, C)

# Numerical derivatives
dC_dT = np.zeros_like(C)
dC_dK = np.zeros_like(C)
d2C_dK2 = np.zeros_like(C)
for i in range(len(T)):
    for j in range(len(K)):
        dC_dT[i, j] = C_spline(T[i], K[j], dx=1, dy=0)
        dC_dK[i, j] = C_spline(T[i], K[j], dx=0, dy=1)
        d2C_dK2[i, j] = C_spline(T[i], K[j], dx=0, dy=2)

# Dupire formula
sigma2 = (dC_dT + r * K[None,:] * dC_dK) / (0.5 * K[None,:]**2 * d2C_dK2)
sigma2 = np.clip(sigma2, 0, 2)  # Remove negative/unstable values
sigma_loc = np.sqrt(sigma2)

# Plot local volatility surface
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(KK, TT, sigma_loc, cmap='plasma')
ax.set_xlabel('Strike K')
ax.set_ylabel('Maturity T')
ax.set_zlabel('Local Volatility')
ax.set_title('Calibrated Local Volatility Surface')
plt.tight_layout()
plt.show() 
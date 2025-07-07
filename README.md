# Local Volatility Models: Complete Guide

This comprehensive guide explores **local volatility models** for option pricing, including theory, calibration, numerical methods, and simulation. Navigate through the sections below to learn about the Dupire equation, calibration techniques, and practical applications, with code samples and visualizations.

---

## Table of Contents
- [Overview](#overview)
- [Introduction to Local Volatility](#introduction-to-local-volatility)
- [The Dupire Equation](#the-dupire-equation)
- [Numerical Methods](#numerical-methods)
- [Calibration Techniques](#calibration-techniques)
- [Monte Carlo Simulation](#monte-carlo-simulation)
- [Applications and Limitations](#applications-and-limitations)
- [References](#references)

---

## Overview
This section explores **local volatility models** for option pricing, including theory, calibration, numerical methods, and simulation. See the [codes/](codes/) folder for Python code samples.

---

## Introduction to Local Volatility

### What is Local Volatility?
Local volatility models generalize the Black-Scholes model by allowing the volatility to depend on both the asset price and time:

$$
\sigma = \sigma(S, t)
$$

This enables the model to fit the entire implied volatility surface observed in the market, rather than assuming a constant volatility.

**Why is this important?** In real markets, implied volatility varies with strike and maturity (the "volatility smile"). Local volatility models, such as the one introduced by Bruno Dupire, provide a framework to capture this behavior while remaining arbitrage-free.

### Comparison to Other Models
- **Black-Scholes:** Assumes constant volatility. Cannot fit volatility smiles/skews.
- **Stochastic Volatility (e.g., Heston):** Volatility follows its own random process. More flexible, but more complex to calibrate and simulate.
- **Local Volatility:** Volatility is a deterministic function of price and time, calibrated to market data.

### Mathematical Formulation

$$
dS_t = r S_t dt + \sigma_{loc}(S_t, t) S_t dW_t
$$

where $\sigma_{loc}(S, t)$ is the local volatility function to be determined from market data.

---

## The Dupire Equation

The **Dupire equation** provides a way to compute the local volatility function $\sigma_{loc}(K, T)$ directly from market option prices (or the implied volatility surface). It is a forward equation for European call prices as a function of strike $K$ and maturity $T$:

$$
\frac{\partial C}{\partial T} = \frac{1}{2} \sigma_{loc}^2(K, T) K^2 \frac{\partial^2 C}{\partial K^2} - r K \frac{\partial C}{\partial K}
$$

where $C = C(K, T)$ is the price of a European call option with strike $K$ and maturity $T$, and $r$ is the risk-free rate.

### Extracting Local Volatility from Market Data
The Dupire formula allows us to compute $\sigma_{loc}(K, T)$ from the observed market prices (or implied volatilities) of options:

$$
\sigma_{loc}^2(K, T) = \frac{\frac{\partial C}{\partial T} + r K \frac{\partial C}{\partial K}}{\frac{1}{2} K^2 \frac{\partial^2 C}{\partial K^2}}
$$

In practice, we use the implied volatility surface $\sigma_{imp}(K, T)$ and convert it to option prices using the Black-Scholes formula, then numerically differentiate to obtain the required partial derivatives.

---

## Numerical Methods

Solving the Dupire PDE for local volatility requires robust numerical methods. The most common approach is to use **finite difference methods** on a grid of strikes and maturities.

### Finite Difference Discretization
The Dupire PDE:

$$
\frac{\partial C}{\partial T} = \frac{1}{2} \sigma_{loc}^2(K, T) K^2 \frac{\partial^2 C}{\partial K^2} - r K \frac{\partial C}{\partial K}
$$

is discretized on a grid $(K_i, T_j)$. Central differences are used for the second derivative in strike, and explicit or implicit time stepping for maturity.

### Interpolation and Smoothing
Market data is only available at discrete strikes and maturities. To compute derivatives, we must interpolate the implied volatility surface (e.g., using splines or local polynomial fits) and smooth the data to reduce noise.

### Practical Issues
- **Stability:** Explicit schemes may require small time steps. Implicit or Crank-Nicolson schemes are more stable.
- **Boundary conditions:** Proper treatment at low/high strikes and short/long maturities is crucial.
- **Grid choice:** Non-uniform grids can help resolve important features (e.g., near-the-money options).

### Code & Visualization
See [`codes/dupire_finite_difference.py`](codes/dupire_finite_difference.py) for a Python implementation of the finite difference method for the Dupire PDE.

---

## Calibration Techniques

Calibrating a local volatility surface involves extracting $\sigma_{loc}(K, T)$ from observed market option prices or implied volatilities. The process typically involves:

1. **Data preparation:** Collect implied volatility data for a range of strikes and maturities.
2. **Interpolation:** Fit a smooth surface to the implied volatilities (e.g., using splines).
3. **Numerical differentiation:** Compute the required partial derivatives of option prices (or implied vols) with respect to strike and maturity.
4. **Smoothing:** Apply regularization or smoothing to reduce noise in the estimated surface.

### Python Example
See [`codes/calibrate_local_vol.py`](codes/calibrate_local_vol.py) for a Python script that calibrates a local volatility surface from synthetic implied volatility data.

### Mathematical Formula
$$
\sigma_{loc}^2(K, T) = \frac{\frac{\partial C}{\partial T} + r K \frac{\partial C}{\partial K}}{\frac{1}{2} K^2 \frac{\partial^2 C}{\partial K^2}}
$$

---

## Monte Carlo Simulation

Once the local volatility surface $\sigma_{loc}(S, t)$ is calibrated, we can simulate asset price paths under the local volatility model using the Euler-Maruyama scheme:

$$
dS_t = r S_t dt + \sigma_{loc}(S_t, t) S_t dW_t
$$

At each time step, the local volatility is evaluated at the current asset price and time. This allows us to price exotic options and compute risk measures under the local volatility model.

### Python Example
See [`codes/monte_carlo_local_vol.py`](codes/monte_carlo_local_vol.py) for a Python script that simulates paths and prices options under a local volatility model.

---

## Applications and Limitations

### When to Use Local Volatility
- When you need a model that fits the entire implied volatility surface exactly (arbitrage-free interpolation).
- For pricing and hedging vanilla and some exotic options (e.g., barrier options).
- When you want a deterministic volatility model (no additional stochastic factors).

### Strengths
- Fits market data exactly (if surface is smooth and arbitrage-free).
- Simple to simulate and calibrate (compared to stochastic volatility).
- Arbitrage-free by construction (if surface is well-behaved).

### Weaknesses
- Cannot capture volatility clustering or jumps (volatility is deterministic).
- May produce unrealistic dynamics for path-dependent options.
- Calibration can be unstable if market data is noisy or sparse.

### Comparison to Other Models
- **Stochastic Volatility:** Captures volatility clustering and smile dynamics, but is harder to calibrate and simulate.
- **Jump Diffusion:** Models sudden price moves, but adds complexity.
- **Local-Stochastic Volatility:** Combines both approaches for greater realism, at the cost of complexity.

### Real-World Considerations
- Market microstructure, liquidity, and discrete strikes/maturities can affect calibration.
- Volatility surfaces may change rapidly in stressed markets.

---

## References
- Gatheral, J. (2006). *The Volatility Surface*.
- Dupire, B. (1994). Pricing with a Smile. *Risk*, 7(1), 18-20.
- Fouque, J.P., Papanicolaou, G., Sircar, K.R., & Solna, K. (2011). *Multiscale Stochastic Volatility for Equity, Interest Rate, and Credit Derivatives*.

---

© 2024 Mohammed Karim Khaldi 
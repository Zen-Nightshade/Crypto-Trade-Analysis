Analyze **inter-trade times** (the waiting time between consecutive trades) to test whether they follow an **exponential distribution**, as implied by a Poisson process.

# Phase -1
### **1. Data Collection**
- Use the same raw trade data (timestamps).
- Compute **inter-trade times** = difference between consecutive trade timestamps (in seconds or milliseconds).
### **2. EDA: Waiting Times**
Perform statistical and graphical diagnostics:
- **Histogram & Empirical CDF:**  
    Plot the distribution of waiting times and their cumulative distribution.  
    Use both **linear** and **log-scale** histograms to inspect tail behavior.
- **QQ-Plot vs Exponential:**  
    Compare empirical quantiles of waiting times to theoretical exponential quantiles.
- **Kolmogorov–Smirnov (KS) Test:**  
    Statistical test for exponentiality (diagnostic only; assumes i.i.d.).
- **Autocorrelation of Waiting Times:**  
    Check independence — Poisson implies no correlation between consecutive waiting times.
### **3. Interpretation**
- If waiting times are **approximately exponential** and **uncorrelated**, the Poisson assumption holds.
- If waiting times show **heavy tails**, **autocorrelation**, or **multi-modal patterns**, the process likely exhibits clustering or variable intensity.
# Phase -2
### **Model Specification**
- **Data:** Inter-trade times tit_iti​
- **Likelihood:**
$$
t_i \sim \text{Exponential}(\theta)
$$
- **Prior (conjugate):**
$$
\text{Gamma}(\alpha_0, \beta_0)
$$
- **Posterior (conjugate update):**
$$
t \sim \text{Gamma} \Big(\alpha_0 + n, \, \beta_0 + \sum_i t_i \Big)
$$
### **Computations / Analytics**
- **Posterior mean:**
$$
E[θ∣t]=α0+nβ0+∑iti\mathbb{E}[\theta \mid t] = \frac{\alpha_0 + n}{\beta_0 + \sum_i t_i}E[θ∣t]=β0​+∑i​ti​α0​+n​
$$
- **Posterior predictive checks (PPC):**
    - Generate draws of waiting times (Exponential with sampled θ\thetaθ)
    - Compare histogram with observed inter-trade times
    - Optional: QQ plot against exponential quantiles
### **Extensions / MCMC**
- **PyMC / Stan:** build tiny models for sampling:
    - Gamma prior (conjugate)
    - Non-conjugate priors if desired
- **Diagnostics:**
    - Trace plots, R̂, ESS
    - Posterior predictive histogram overlay
    - Exponential QQ plot to check fit
    - Autocorrelation of residuals (if needed)
# Phase 3 - Waiting Time Modeling: Comparisons & Experiments

### **1. Conjugate vs Non-Conjugate Priors**
- Compare **Gamma** (conjugate prior on rate θ) vs **LogNormal** (non-conjugate) priors.
- Evaluate:
  - Posterior mean / median of θ
  - Tail behavior of posterior
  - Runtime and diagnostics (R̂, ESS)
  - Sensitivity to hyperparameters
- Report **LOO** or **WAIC** if applicable for predictive performance.

### **2. Check Exponential Assumption**
- Test for **memorylessness**:
  - Examine autocorrelation in inter-trade times.
  - Check log-linear hazard plots.
- If exponential assumption fails:
  - Fit **Weibull** or **Gamma** waiting time models as alternatives.
  - Compare via **LOO** for predictive accuracy.

### **3. Posterior Predictive Checks (PPC)**
- Simulate **inter-trade times** from the posterior predictive distribution.
- Compare simulated vs observed:
  - Mean, variance, quantiles, extreme waiting times
  - Burst or clustering patterns
- Overlay histograms and empirical CDFs for visual validation.

**Deliverables:**
- Plots: posterior histograms, PPC overlays, ACF/QQ plots
- Table: diagnostics (R̂, ESS), predictive fit (LOO/WAIC), model runtime
# Phase 4 - Waiting Time Modeling: Advanced Extensions
### **1. Time-Varying Arrival Rate**
- Extend exponential waiting time model to allow **time-varying rate θ(t)**.
- Equivalent to a **non-homogeneous Poisson process** in continuous time.
- Options:
  - **Piecewise exponential model:** estimate θ(t) per time bin.
  - **Gaussian Process prior** on log θ(t) for smooth variation over time.
  - **Spline-based models** for scalable approximation of θ(t).
### **2. Hierarchical Modeling Across Instruments**
- Model per-instrument rate parameters θⱼ with a hierarchical prior (Gamma or LogNormal).
- Add hyperpriors for pooling information across instruments.
- Captures differences in trading speed between instruments while sharing overall structure.
### **3. Mixture and Regime-Switching Models**
- Use **mixtures of exponentials** to capture multiple regimes of waiting behavior:
  - “Normal” regime with typical inter-trade spacing.
  - “Burst” regime with very short intervals (news or bots).
- Alternatively, use a **Markov-switching exponential or Weibull process** to model transitions between calm and active market states.
### **4. Scalable and Sequential Inference**
- For long event streams:
  - Use **variational inference (ADVI/SVI)** for approximate posteriors.
  - Employ **sequential Monte Carlo (SMC)** for online updates of θ.
- Aggregate inter-arrival times into manageable segments for batch MCMC.

**Deliverables:**
- Notebooks implementing piecewise, GP, and mixture exponential models.
- Figures showing time-varying θ(t), hazard rate plots, and regime transitions.
# Phase 5 - Waiting Time Modeling: Applications & Evaluation
### **1. Prediction**
- **Predict the next inter-trade time** given the last K trades using the posterior predictive distribution.
- Evaluate **coverage** and **calibration** of predictive intervals.
### **2. Evaluation Metrics**
- **Predictive log-score** for inter-trade times.
- **LOO cross-validation** for predictive accuracy.
- **Calibration:** check if predictive intervals contain observed inter-trade times at expected frequencies.
- Optional: frame as a classification problem (e.g., “Will next trade occur within t seconds?”) and evaluate **ROC/AUC**.
### **3. Report / Slide Deck**
- Include:
  - Data description and EDA summaries
  - Model formulation (Exponential, Weibull, mixture models, NHPP)
  - Posterior summaries (mean, credible intervals, tail behavior)
  - Posterior predictive checks (histogram, CDF, QQ plots)
  - Sensitivity analysis to priors
  - Computational cost table
  - Final conclusions & recommendations

**Deliverables:**
- Forecast plots for next inter-trade times with predictive intervals
- Posterior predictive histograms and CDFs
- Short report or slide deck summarizing all results
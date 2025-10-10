# Phase-1: Data Collection & EDA
Analyze the **number of trades per unit time** (e.g., per minute) to test whether trade arrivals behave like a **Poisson counting process**.
### **1. Data Collection**
- Download raw trade data for **BTC/USDT** (and optionally **USDT/USD**) from Binance using API.
- Include: `timestamp`, `price`, and `size`.
- Choose a time window (start from one week).
### **2. Preprocessing**
Aggregate raw trade data into fixed time buckets (1-minute or 5-minute intervals).
For each interval, compute:
Trade count = number of trades in that interval
(Optionally) total or average trade size
### **3. EDA: Trade Counts**
Produce visualizations and statistics to understand the count process.
- **Time Series Plot:**  
    Plot trade counts vs time to see activity fluctuations.
- **Mean–Variance Relationship:**  
    Check if `mean ≈ variance` (Poisson property: _equidispersion_).  
    → Overdispersion (variance > mean) suggests clustering or non-Poisson behavior.
- **Autocorrelation Function (ACF):**  
    Compute ACF of trade counts to test for temporal dependence.  
    → Independence ⇒ ACF near zero.

    ACF in this context gives the dependence of count of trades in future and current count of trades. 
- **Distribution Check:**  
    Compare histogram of counts with Poisson(λ = mean count).  
    Optionally, use a goodness-of-fit test (e.g., chi-square).
### **4. Interpretation**
- If counts show **constant mean rate, mean ≈ variance, and low ACF**, Poisson may be plausible.
- Otherwise, evidence of **time-varying rates** or **clustering** suggests a non-Poisson process (e.g., self-exciting or inhomogeneous).
# Phase-2: Bayesian Modeling
Model the **number of trades per interval** using a **Poisson likelihood** and **Gamma conjugate prior**. Compare analytical posterior updates to sampling-based Bayesian inference.
### **Computations / Analytics**

- **Posterior mean:**
$$
E[λ∣y]=α0+∑iyiβ0+n\mathbb{E}[\lambda \mid y] = \frac{\alpha_0 + \sum_i y_i}{\beta_0 + n}E[λ∣y]=β0​+nα0​+∑i​yi​​
$$
- **Credible intervals:** use Gamma percentiles.
- **Posterior predictive checks (PPC):**
    - Generate Poisson draws from the posterior predictive distribution.
    - Overlay histogram on observed trade counts to see if the model fits.
### **Extensions / MCMC**
- Use **PyMC or Stan** for sampling-based inference:
    - **Conjugate Gamma prior**: validate analytic solution.
    - **LogNormal prior**: non-conjugate comparison, observe how posterior shape differs and computation cost.
- **Diagnostics:**
    - Trace plots, R̂, effective sample size (ESS).
    - Posterior predictive checks (PPC) to evaluate model fit.
    - Optional: model comparison via LOO / WAIC.
# Phase 3 - Trade Count Modeling: Comparisons & Experiments

### **1. Conjugate vs Non-Conjugate Priors**
- Compare **Gamma** (conjugate) vs **LogNormal** (non-conjugate) priors on λ (trade rate).
- Evaluate:
  - Posterior central tendency (mean, median)
  - Tail behavior (posterior spread / heaviness)
  - Runtime (time per effective sample)
  - Diagnostics: R̂, ESS
  - Sensitivity to hyperparameters (small hyperprior sweep)
- Report **LOO** or **WAIC** scores to assess predictive fit.

### **2. Check Poisson Assumptions**
- Compute **sample variance / mean** of trade counts.
  - If `var > mean` → **overdispersion** (Poisson may be inadequate).
- If overdispersion detected:
  - Consider **Negative Binomial (NB)** model (Gamma–Poisson mixture)
  - Or a **hierarchical Poisson** model with time-varying λ.

### **3. Posterior Predictive Checks (PPC)**
- Simulate **trade counts** from the posterior.
- Compare simulated vs observed summaries:
  - Mean, variance, quantiles, maxima, burstiness
- Use posterior predictive histograms to visualize model fit.

**Deliverables:**
- Comparative plots (posterior distributions, PPC histograms)
- Diagnostic table (R̂, ESS, runtime, LOO/WAIC)
# Phase 4 - Trade Count Modeling: Advanced Extensions
### **1. Non-Homogeneous Poisson (Time-Varying Rate)**
- Model a **time-varying trade rate** λₜ instead of a constant λ.
- **Piecewise constant model:**  
  - Split the day into bins (e.g., hourly).  
  - Estimate λₜ per bin with **smoothing priors** (hierarchical Gamma prior or random walk prior).  
  - Intuitive and easy to implement.
- **Gaussian Process prior on log-rate:**  
  - Model `log λ(t) ~ GP(·)` to capture smooth temporal variation.  
  - Complexity scales as O(T³) for T time points; use sparse GP approximations for large T.  
  - Stan provides GP examples and implementation guidance.
- **Alternative:**  
  - Use **spline basis (B-splines)** for log λ(t) to achieve scalable and flexible rate dynamics.

### **2. Hierarchical Modeling Across Instruments (Multi-Ticker)**
- Model ticker-specific rates λⱼ with a **group-level prior** (Gamma or LogNormal).
- Add **hyperpriors** for hierarchical shrinkage.
- Benefits:
  - Borrows statistical strength across instruments.
  - Stabilizes estimation when some tickers have low trade counts.
- For many parameters:
  - Use **shrinkage priors** like **horseshoe** or **regularized horseshoe**.
### **3. Mixture Regimes (Spike vs Normal)**
- Model **mixtures of Poissons** or **Markov-switching Poisson processes**:
  - One regime captures **normal activity**.
  - The other captures **high-rate spikes** (e.g., news bursts, bots).
- Allows modeling of **regime switching** and **burstiness** in trading activity.
### **4. Scalable Inference**
- For very large tick datasets:
  - Subsample windows or aggregate to minute-level counts.
  - Use **variational inference** (PyMC ADVI, NumPyro SVI) for approximate posterior estimation.
- For real-time or streaming data:
  - Apply **particle filters** or **sequential Monte Carlo** for online Bayesian updates.
- Use **control variates and subsampling** for efficiency in massive data scenarios.

**Deliverables:**
- Notebooks implementing NHPP, hierarchical, and mixture models.
- Figures showing time-varying rate λₜ, posterior smoothing, and regime dynamics.
# Phase 5 - Trade Count Modeling: Applications & Evaluation
### **1. Prediction**
- **Forecast future counts** per minute/hour using the posterior predictive distribution.
- Generate **uncertainty bands** around predicted counts.
- Can also frame as a **classification problem** (e.g., “Will > k trades occur in the next minute?”) if needed.
### **2. Evaluation Metrics**
- **Predictive log-score:** measures how well the posterior predicts new counts.
- **LOO (Leave-One-Out) cross-validation** for predictive accuracy.
- **Calibration:** coverage of predictive intervals (e.g., 80%, 95%).
- **ROC / AUC:** only if converted to a classification task (high-activity vs low-activity).
### **3. Report / Slide Deck**
- Include:
  - Data description and EDA summaries
  - Model formulation (Poisson, Negative Binomial, NHPP, etc.)
  - Posterior summaries (mean, credible intervals, tail behavior)
  - Posterior predictive checks (PPC histograms, time series plots)
  - Sensitivity analysis for priors
  - Computational cost table (time per effective sample)
  - Final conclusions & recommendations

**Deliverables:**
- Forecast plots with uncertainty bands
- Posterior predictive histograms for counts
- Short report or slide deck summarizing all findings
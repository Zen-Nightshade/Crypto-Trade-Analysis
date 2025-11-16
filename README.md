# Bayesian Analysis of High-Frequency Crypto Trades

## Overview

This project applies a suite of advanced Bayesian techniques to model and understand the complex dynamics of high-frequency BTC/USDT trade data, focusing on both **trade rate** (number of trades per minute) and **trade volume**.

The core analytical components include:
-   **Probabilistic Modeling:** Using Gamma-Poisson, LogNormal-Poisson, and Joint Normal distributions to model trade counts and volumes.
-   **Advanced Hierarchical Modeling:** A Hierarchical Negative Binomial Regression model is developed to capture overdispersion and daily seasonality in trade counts.
-   **Bayesian Regression:** A linear regression model is used to predict log-returns based on market features.
-   **Formal Hypothesis Testing:** Simple and composite **Bayes Factors** are calculated to rigorously test hypotheses about market behavior.
-   **Computational Inference:** Posterior distributions are estimated using a variety of methods, including analytical solutions for conjugate models, Grid Approximation, and custom-built MCMC samplers (**Metropolis-Hastings** and **Gibbs Sampling**).

The project's goal is to move beyond simple point estimates to provide a robust, probabilistic understanding of market activity, complete with principled uncertainty quantification.

---

## Repository Structure

```
├── data/
│   ├── raw/
│   │   └── one_week             # Trades from 2025-10-01 to 2025-10-08
│   └── processed/
│       ├── trades_2025-10-01_to_2025-10-07_1min.csv
│       ├── trades_2025-10-01_to_2025-10-07_10s.csv
│       ├── hierarchical_1min_data.csv
│       └── regression_1min_data.csv
├── figures/                     # All plots and figures
├── metadata/
├── notebooks/                   # Jupyter notebooks for analysis and modeling
│   ├── Exploratory_Data_Analysis.ipynb
│   ├── Gamma_Poisson_Model.ipynb
│   ├── Joint_Normal_Volume_model.ipynb
│   ├── Log_Normal_Poisson_Model.ipynb
│   ├── BayesianRegression.ipynb
│   └── Hierarchical_NBG_model.ipynb
├── reports/                     # Project reports
├── scripts/                     # Python scripts for data processing and modeling
│   ├── fetch_data.py            # Download trades from Binance
│   ├── data_splitter.py
│   ├── preprocess.py            # Core preprocessing for trade aggregation
│   ├── hierarchical_preprocess.py
│   ├── regression_preprocessor.py
│   ├── random_utils.py          # Classes for random variable generation
│   └── plot_trades.py
├── .gitignore
├── README.md                    # Overview, project description, instructions
└── requirements.txt
```

---

## Data

*   **Raw Data:** Trades are fetched from Binance using the `ccxt` API for the period `2025-10-01` to `2025-10-08`.
*   **Preprocessing:** Trades are aggregated into **1-minute and 10-second intervals**. Custom pre-processing scripts also generate feature-rich datasets for the regression and hierarchical models. Key computed fields include:
    *   Timestamp, Price (VWAP), Trade Cost, Trade Count
    *   Lagged variables (log-returns, volume, etc.)
    *   Buy/Sell Imbalance and Volatility metrics

This preprocessing helps **reduce noise**, **stabilize variability**, and **engineer features**, making the data more suitable for advanced Bayesian modeling.

---

## Models & Inference

### 1. Trade Volume Modeling (Log-Normal)

-   **Model:** We model the **logarithm of trade volume** using a **Joint Normal distribution** with unknown mean ($\mu$) and variance ($\sigma^2$) to stabilize variance and handle the natural skewness of the data.
-   **Priors:** Conjugate Normal-Inverse-Gamma priors are used, allowing for analytical updates to the posterior distribution.
-   **Bayes Factor Analysis:** This model is extended to perform formal hypothesis testing. We calculate both **simple** (e.g., $\mu=14$) and **composite** (e.g., $\mu \in (13, 15)$) Bayes Factors to rigorously evaluate evidence about the mean of the log-volume process. This also allows us to study how the stability of evidence changes with the amount of data used (lag).

### 2. Bayesian Regression for Log-Returns

-   **Goal:** To predict log-returns using a set of lagged market features (e.g., previous returns, volume, volatility).
-   **Model:** A Bayesian Linear Regression model is implemented with Normal priors on the coefficients and an Inverse-Gamma prior on the error variance.
-   **Inference:** The joint posterior is intractable. We therefore use a **Gibbs Sampler** to efficiently draw samples from the posterior by iteratively sampling from the known full-conditional distributions of the parameters.

### 3. Trade Rate (Count) Modeling

-   **Initial Count Models:** We first apply a **Gamma-Poisson** (conjugate) model and a **LogNormal-Poisson** (non-conjugate) model. For the LogNormal-Poisson model, due to its non-conjugate nature which results in an intractable posterior, we explore and compare multiple sampling techniques to approximate the posterior, including **Grid Approximation**, standard **Monte Carlo importance sampling**, and a **Metropolis-Hastings MCMC** sampler.
-   **Hierarchical Negative Binomial Model:** Our most advanced model for trade counts, designed to overcome the limitations of simpler approaches. Its key features are:
    -   **Negative Binomial Likelihood:** Natively handles the overdispersion (variance > mean) common in financial trade data.
    -   **Regression Framework:** Uses lagged market features to predict the mean trade count.
    -   **Hierarchical Structure:** Models the baseline trade count for each hour of the day as being drawn from a shared group distribution. This captures daily seasonality and allows the model to "borrow strength" across hours for more stable estimates.
    -   **Inference:** Fitted using a custom-built **Metropolis-Hastings MCMC sampler** to draw samples from the high-dimensional posterior.

---

## Usage

1.  Clone the repository:
    ```bash
    git clone https://github.com/Zen-Nightshade/Crypto-Trade-Analysis.git
    cd Crypto-Trade-Analysis
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Fetch and preprocess data:
    ```bash
    python scripts/fetch_data.py
    python scripts/preprocess.py
    # Run other preprocessors as needed for specific models
    ```

4.  Run notebooks for exploratory analysis and modeling. The notebooks are named descriptively based on the model they implement.

5.  Generated figures and plots are stored in the `figures/` directory.

---

## Key Results

*   **Bayes Factor Analysis** provides strong, stable evidence that the long-term mean of log-volume is concentrated within the (13, 15) interval, but also shows that short-term inferences (using small lags) are highly unreliable due to market noise.
*   The **Bayesian Regression model** for log-returns successfully creates well-calibrated 95% credible intervals that contain over 99.9% of the observed returns, effectively quantifying the extreme uncertainty of the process.
*   While simple count models (Gamma-Poisson) struggled with market volatility (with over 85% of data falling outside the 95% PPI), the **Hierarchical Negative Binomial model shows an excellent fit**. Its posterior predictive checks reveal that it is well-calibrated, with its 95% credible intervals containing ~96% of the actual data points, successfully modeling both normal activity and extreme market spikes.

---

## Who We Are

-   [Zen_Nightshade](https://github.com/Zen-Nightshade)
-   [Celingsz](https://github.com/Ceilingsz)
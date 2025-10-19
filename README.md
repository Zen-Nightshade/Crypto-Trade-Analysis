# Crypto Trade Analysis

## Overview
This project performs a **Bayesian analysis of cryptocurrency trade activity** (BTC/USDT) at high frequency, focusing on both **trade rate** (number of trades per minute) and **trade volume** (total cost of trades per minute).  
We aim to model and understand the dynamics of trades, capture uncertainty, and assess model performance using **Posterior Predictive Intervals (PPI)**.

---

## Project Structure

```
├── data/                       # Raw and processed data
│   ├── raw/
│   │   └── one_week             # Contains trades from 2025-10-01 00:00:00 to 2025-10-08 00:00:00
│   └── processed/
├── figures/                     # All plots and figures
├── metadata/
├── notebooks/                   # Jupyter / Colab notebooks
│   ├── Exploratory_Data_Analysis.ipynb
│   ├── Gamma_Poisson_Model.ipynb
│   ├── Joint_Normal_Volume_model.ipynb
│   └── Log_Normal_Poisson_Model.ipynb
├── reports/                     # Contain project report
├── scripts/                     # Python scripts for data processing
│   ├── fetch_data.py            # Download trades from Binance/CCXT
│   ├── data_splitter.py
│   ├── preprocess.py            # Aggregate raw trades into intervals of 1min and 10s
│   ├── random_utils.py          # Classes to generate random variables from different distributions
│   └── plot_trades.py           # Standard plotting functions used in EDA
├── .gitignore
├── README.md                    # Overview, project description, instructions
└── requirements.txt

````

---

## Data
* **Raw Data:** Trades are fetched from Binance using the `ccxt` API.
* **Preprocessing:** Trades are aggregated into **1-minute and 10-second intervals**, with the following computed fields:
  * Timestamp
  * Bought quantity
  * Sold quantity
  * Total traded quantity
  * Price (computed via **Volume-Weighted Average Price**, VWAP)
  * Trade cost
  * Number of trades
  * Symbol

This preprocessing helps **reduce noise** and **stabilize variability**, making the data more suitable for Bayesian modeling.

---

## Models

### Trade Rate Models
- **Gamma–Poisson Model:** Conjugate Bayesian model for the number of trades per minute.  
- **Lognormal–Poisson Model:** Non-conjugate Bayesian model, more flexible for heavy-tailed trade rates.  
  > **Note:** This model uses Monte Carlo simulations for posterior inference and can benefit from a GPU for faster computation.

**Lag-based Updating:**  
The posterior at time *t* is updated using data from the previous *lag* minutes to capture short-term temporal dependencies. Smaller lag values improve model responsiveness to rapid market changes.  

**Posterior Predictive Checks:**  
We validate the models by simulating trade counts from the posterior and comparing them with observed data.  

### Trade Volume Models
- **Joint Normal Model:** We model the **logarithm of trade volume** to stabilize variance and reduce skewness.  
- Smaller lag values result in more responsive predictions, allowing the model to adapt to recent market changes.  
- Posterior Predictive Intervals (PPI) captured a large proportion of observed trade volumes, indicating strong model fit.

---

## Usage

1. Clone the repository:

```bash
git clone https://github.com/Zen-Nightshade/Crypto-Trade-Analysis.git
cd Crypto-Trade-Analysis
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Fetch and preprocess data:

```bash
python scripts/fetch_data.py
python scripts/preprocess.py
```

4. Run notebooks for exploratory analysis and modeling:

* `notebooks/Exploratory_Data_Analysis.ipynb`
* `notebooks/Gamma_Poisson_Model.ipynb`
* `notebooks/Joint_Normal_Volume_model.ipynb`
* `notebooks/Log_Normal_Poisson_Model.ipynb`

5. Generated figures and plots are stored in the `figures/` directory.

---

## Results

* Both **trade rate models** struggle to capture extreme fluctuations at very high frequency, with a large proportion of data points lying outside the PPI.
* Smaller lag values improve model responsiveness, especially for sudden market movements.
* The **Joint Normal model** for trade volume shows a better fit and PPI coverage compared to trade rate models, capturing the majority of variability in the log-transformed trade volume effectively.

---

# Who We Are
- [Zen_Nightshade](https://github.com/Zen-Nightshade)
- [Celingsz](https://github.com/Ceilingsz)
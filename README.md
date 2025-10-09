# Crypto Trade Analysis Project Repository Layout

## Root Structure
├── README.md                   # Overview, project description, instructions
├── environment.yml / requirements.txt  # Conda or pip dependencies
├── data/                       # Raw and processed data
│   ├── raw/                    # Original trade data CSVs or JSON
│   └── processed/              # Aggregated/minute-level counts, inter-trade times
├── notebooks/                  # Jupyter / Colab notebooks
│   ├── phase1_counts_EDA.ipynb          # Phase 1: trade count exploration
│   ├── phase1_waiting_EDA.ipynb         # Phase 1: waiting time exploration
│   ├── phase2_counts_Bayesian.ipynb     # Phase 2: analytic and MCMC Poisson models
│   ├── phase2_waiting_Bayesian.ipynb    # Phase 2: analytic and MCMC Exponential models
│   ├── phase3_counts_comparisons.ipynb  # Phase 3: conjugate vs non-conjugate counts
│   ├── phase3_waiting_comparisons.ipynb # Phase 3: conjugate vs non-conjugate waiting times
│   ├── phase4_counts_advanced.ipynb     # Phase 4: NHPP, hierarchical, mixtures counts
│   ├── phase4_waiting_advanced.ipynb    # Phase 4: time-varying, mixture, hierarchical waiting times
│   ├── phase5_counts_prediction.ipynb   # Phase 5: forecasts, PPC, evaluation for counts
│   └── phase5_waiting_prediction.ipynb  # Phase 5: forecasts, PPC, evaluation for waiting times
├── scripts/                    # Python scripts for data processing / model utilities
│   ├── fetch_data.py            # Download trades from Binance/CCXT
│   ├── preprocess_counts.py     # Aggregate raw trades into counts per interval
│   ├── preprocess_waiting.py    # Compute inter-trade times
│   ├── bayesian_utils.py        # Functions for posterior computation, PPC
│   └── plotting_utils.py        # Standard plotting functions for EDA and PPC
├── figures/                    # All plots and figures
│   ├── counts/                  # Trade counts plots (time series, PPC, diagnostics)
│   └── waiting/                 # Waiting time plots (histogram, QQ, PPC)
├── models/                     # Saved model objects or Stan/PyMC model files
│   ├── counts/                  # Stan/PyMC models for counts
│   └── waiting/                 # Stan/PyMC models for waiting times
└── reports/                    # Short reports or slide decks
    ├── counts_report.pdf
    └── waiting_report.pdf

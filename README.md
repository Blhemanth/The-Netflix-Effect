# 🎬 The Netflix Effect: What Makes a Show Popular?

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-red.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)
![Netflix Theme](https://img.shields.io/badge/Theme-Netflix%20Dark%20%26%20Crimson-E50914.svg)

An empirical data science investigation and interactive web application exploring Netflix's global catalog of **8,807 titles**. This project analyses the algorithmic blueprint behind streaming dominance—from format economics and runtime sweet spots to the 2016 inflection point, maturity ratings, and international localization.

---

## 🚀 Live Features & Functional Components

The application is structured into five core interactive modules:

1. **🏠 Overview & Metrics**:
   - Executive KPI metric cards (Total Titles, 69.6% Movies vs. 30.4% TV Shows, TV-MA dominance, peak ingestion year).
   - Core strategic takeaways and executive format economics.
   - Interactive catalog search engine with multi-variable filters (format, year range, maturity rating, title/cast query).
   - One-click CSV export of filtered datasets.

2. **📊 Visualizations & Exploratory Data Analysis (EDA)**:
   - Dedicated viewer and full gallery view of **10 high-resolution analytical charts**.
   - Quantitative data breakdowns, benchmarks, and business takeaways for every visualization.

3. **💡 Deep Analytical Insights**:
   - **Content Format Dominance**: The 70/30 split and why serialized TV acts as the ultimate retention engine.
   - **The 2016 Inflection Point**: The global rollout to 130+ countries and the shift to proprietary Netflix Originals.
   - **Genre Preferences & Borderless Consumption**: The rise of International titles, Dramas, and high-ROI Stand-Up Comedy.
   - **Maturity Ratings Moat**: Why over 60.9% of the catalog is TV-MA & TV-14, creating creative freedom unconstrained by broadcast decency laws.
   - **Geographic Production Hubs**: US dominance vs. the surge of India, UK, South Korea, Spain, and France.

4. **🎯 Actionable Recommendations**:
   - **Pillar 1:** Strategic Genre Investment & Hybridization (90–105 minute runtime sweet spot).
   - **Pillar 2:** Hyper-Localized Expansion with Global Export DNA (local-to-global models).
   - **Pillar 3:** Family Catalog Optimization (bridging the 10.2% family content gap against Disney+).
   - **Pillar 4:** Series Longevity & Overcoming the 1-Season Cancellation Cliff (67% single-season attrition).
   - **Strategic Priority Matrix**: Impact vs. Effort executive prioritization.

5. **📖 Data Storytelling Report**:
   - Publication-grade narrative following the **Problem ➔ Analysis ➔ Insights ➔ Recommendations** structure.
   - Interactive knowledge check quiz testing user streaming strategy knowledge.

---

## 📊 The 10 High-Resolution Visualizations

| Index | Visual File | Analytical Focus | Key Metric / Insight |
| :---: | :--- | :--- | :--- |
| **01** | `viz1_type_distribution.png` | Format Split | **69.6% Movies** vs. **30.4% TV Shows** |
| **02** | `viz2_growth_trend.png` | Ingestion Velocity (2008–2021) | **+370% surge** post-2016; peak in 2019 (2,016 titles) |
| **03** | `viz3_top_genres.png` | Genre Breakdown | International (4,103+), Dramas (2,427), Comedies (1,674) |
| **04** | `viz4_ratings_distribution.png` | Target Audience Ratings | **60.9%** rated TV-MA (36.4%) or TV-14 (24.5%) |
| **05** | `viz5_top_countries.png` | Global Sourcing Hubs | US (3,689), India (1,046), UK (804), Canada (445) |
| **06** | `viz6_movie_durations.png` | Feature Film Runtimes | Gaussian bell curve; median **98 minutes** |
| **07** | `viz7_tv_seasons.png` | TV Show Lifespans | **67.0%** of TV series have only 1 season |
| **08** | `viz8_monthly_seasonality.png` | Addition Seasonality | Major release surges in **December** (813) & **July** (827) |
| **09** | `viz9_release_year_trend.png` | Content Freshness | **73%+** of catalog released between 2015 and 2021 |
| **10** | `viz10_top_directors.png` | Creative Talent Volume | Animation franchises (Rajiv Chilaka) & Comedy specials |

---

## 🛠️ Tech Stack & Styling

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Data Engineering**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Imaging Engine**: [Pillow (PIL)](https://python-pillow.org/)
- **Design Language**: Custom Netflix Branding CSS
  - Deep Black Background (`#141414`)
  - Surface Card Gradients (`#1A1A1A`, `#161616`)
  - Netflix Red Accents (`#E50914`)
  - Crisp typography using Google Fonts (*Bebas Neue* & *Montserrat*)

---

## ⚡ Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Blhemanth/The-Netflix-Effect.git
cd The-Netflix-Effect
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```

The app will launch at `http://localhost:8501`.

---

## 📂 Repository Structure

```
The-Netflix-Effect/
├── app.py                         # Complete interactive Streamlit application
├── netflix_titles.csv             # Kaggle dataset (8,807 Netflix records)
├── requirements.txt               # Python package dependencies
├── .gitignore                     # Git exclusion rules
├── README.md                      # Comprehensive project documentation
├── viz1_type_distribution.png     # Visual 1: Movies vs TV Shows split
├── viz2_growth_trend.png          # Visual 2: Ingestion trend over time
├── viz3_top_genres.png            # Visual 3: Top catalog genres
├── viz4_ratings_distribution.png  # Visual 4: Maturity ratings breakdown
├── viz5_top_countries.png         # Visual 5: Top producing nations
├── viz6_movie_durations.png       # Visual 6: Movie duration distribution
├── viz7_tv_seasons.png            # Visual 7: TV season distribution
├── viz8_monthly_seasonality.png   # Visual 8: Monthly content addition seasonality
├── viz9_release_year_trend.png    # Visual 9: Release year trends
└── viz10_top_directors.png        # Visual 10: Top prolific directors
```

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

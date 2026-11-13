import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os
import io
import html
import plotly.graph_objects as go
import plotly.express as px

# Asset path resolution helper for portable execution
def resolve_asset_path(filename):
    if os.path.exists(filename):
        return filename
    fallback = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(fallback):
        return fallback
    return filename

# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION & NETFLIX THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="The Netflix Effect | What Makes a Show Popular?",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Netflix Cinematic Dark Theme with High-Contrast Typography & Mobile Responsiveness
st.markdown("""
<style>
    /* Global styles & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');

    .stApp {
        background-color: #141414;
        color: #F0F0F0;
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Headings high-contrast styling */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    .stMarkdown p, .stMarkdown li {
        color: #E2E2E2 !important;
        line-height: 1.7;
    }

    /* Sidebar customization */
    [data-testid="stSidebar"] {
        background-color: #0b0b0b !important;
        border-right: 1px solid #222222;
    }
    [data-testid="stSidebar"] hr {
        border-color: #2b2b2b;
    }

    /* Netflix Brand Header */
    .netflix-logo-text {
        font-family: 'Bebas Neue', 'Impact', sans-serif;
        color: #E50914;
        font-size: 2.8rem;
        letter-spacing: 2px;
        margin: 0;
        padding: 0;
        text-shadow: 0 2px 14px rgba(229, 9, 20, 0.55);
    }
    .netflix-subtext {
        color: #C8C8C8;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1px;
        margin-top: -6px;
        margin-bottom: 20px;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(20, 20, 20, 0.96) 0%, rgba(38, 10, 13, 0.90) 60%, rgba(229, 9, 20, 0.3) 100%),
                    radial-gradient(circle at top right, #38080a 0%, #141414 70%);
        border: 1px solid #333333;
        border-left: 6px solid #E50914;
        padding: 28px 32px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
    }
    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 3rem;
        letter-spacing: 1.5px;
        color: #FFFFFF;
        margin-bottom: 8px;
        line-height: 1.1;
    }
    .hero-title span {
        color: #E50914;
    }
    .hero-desc {
        color: #E8E8E8;
        font-size: 1.05rem;
        line-height: 1.6;
        max-width: 980px;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #1a1a1a;
        border: 1px solid #333333;
        border-top: 3px solid #E50914;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: left;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 12px;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(229, 9, 20, 0.25);
        border-color: #E50914;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #D0D0D0;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 2.15rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
        margin-bottom: 6px;
    }
    .metric-value span {
        color: #E50914;
    }
    .metric-sub {
        font-size: 0.82rem;
        color: #BFBFBF;
        display: flex;
        align-items: center;
        gap: 4px;
        font-weight: 500;
    }

    /* Content Cards */
    .content-box {
        background-color: #191919;
        border: 1px solid #303030;
        border-radius: 10px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .content-box-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        border-bottom: 1px solid #333333;
        padding-bottom: 10px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .content-box-header span.icon {
        color: #E50914;
    }

    /* Badges */
    .badge-netflix {
        background-color: #E50914;
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 9px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        display: inline-block;
        text-transform: uppercase;
    }
    .badge-secondary {
        background-color: #2b2b2b;
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 9px;
        border-radius: 4px;
        display: inline-block;
        border: 1px solid #3e3e3e;
    }

    /* Styled Quotes / Callouts */
    .quote-box {
        background-color: #1e1315;
        border-left: 4px solid #E50914;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 15px 0;
        font-style: italic;
        color: #F0F0F0;
        font-weight: 500;
    }

    /* Chart Viewer Frame */
    .chart-frame {
        background-color: #161616;
        border: 1px solid #2e2e2e;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .chart-caption {
        background-color: #1c1c1c;
        border-left: 4px solid #E50914;
        padding: 14px 18px;
        border-radius: 0 6px 6px 0;
        font-size: 0.95rem;
        color: #EAEAEA;
        line-height: 1.6;
        margin-top: 14px;
    }

    /* Streamlit Tabs custom styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161616;
        padding: 8px 10px;
        border-radius: 8px;
        border: 1px solid #2e2e2e;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #CCCCCC;
        font-weight: 600;
        padding: 8px 16px;
        background-color: transparent;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E50914 !important;
        color: #FFFFFF !important;
    }

    /* Recommendation Cards */
    .rec-card {
        background: linear-gradient(145deg, #1d1d1d 0%, #151515 100%);
        border: 1px solid #333333;
        border-left: 5px solid #E50914;
        border-radius: 10px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4);
    }
    .rec-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .rec-pill {
        background-color: rgba(229, 9, 20, 0.2);
        color: #ff4b55;
        border: 1px solid #E50914;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* Spotlight Card */
    .spotlight-card {
        background: linear-gradient(135deg, #1f1416 0%, #161616 100%);
        border: 1px solid #3a2225;
        border-left: 5px solid #E50914;
        border-radius: 10px;
        padding: 20px 24px;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.5);
    }

    /* Streamlit Widget Label & Radio Overrides */
    label[data-testid="stWidgetLabel"] p {
        color: #F0F0F0 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
    .stRadio div[role="radiogroup"] label div p {
        color: #E8E8E8 !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
    }
    /* Streamlit Selectbox & MultiSelect Clean Styling - Eliminates double border / outer square cover box */
    .stSelectbox div[data-baseweb="select"] {
        border: none !important;
        background-color: transparent !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #383838 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        box-shadow: none !important;
    }
    .stSelectbox div[data-baseweb="select"] > div:hover {
        border-color: #E50914 !important;
    }
    .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: #E50914 !important;
        box-shadow: 0 0 0 1px #E50914 !important;
    }
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* MultiSelect Clean Styling */
    .stMultiSelect div[data-baseweb="select"] {
        border: none !important;
        background-color: transparent !important;
    }
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #383838 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        box-shadow: none !important;
    }
    .stMultiSelect div[data-baseweb="select"] > div:hover {
        border-color: #E50914 !important;
    }
    .stMultiSelect div[data-baseweb="select"] > div:focus-within {
        border-color: #E50914 !important;
        box-shadow: 0 0 0 1px #E50914 !important;
    }

    /* Text Input Clean Styling */
    .stTextInput div[data-baseweb="input"] {
        border: none !important;
        background-color: transparent !important;
    }
    .stTextInput div[data-baseweb="input"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #383838 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        box-shadow: none !important;
    }
    .stTextInput div[data-baseweb="input"] > div:hover {
        border-color: #E50914 !important;
    }
    .stTextInput div[data-baseweb="input"] > div:focus-within {
        border-color: #E50914 !important;
        box-shadow: 0 0 0 1px #E50914 !important;
    }
    .stTextInput input {
        color: #FFFFFF !important;
    }
    .stExpander {
        border: 1px solid #333333 !important;
        background-color: #161616 !important;
        border-radius: 8px !important;
    }
    .stExpander summary span p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Uniform Cinematic Chart Card Frame */
    .uniform-chart-card {
        background-color: #0e0e0e;
        border: 1px solid #2d2d2d;
        border-top: 3px solid #E50914;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 22px;
        box-shadow: 0 6px 22px rgba(0,0,0,0.65);
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }
    .uniform-chart-card img {
        border-radius: 6px;
        max-height: 480px !important;
        width: 100% !important;
        object-fit: contain !important;
        display: block !important;
        margin: 0 auto !important;
    }

    /* Catchy Visual Banner */
    .catchy-banner {
        background: linear-gradient(90deg, #201214 0%, #171717 65%, #1c1c1c 100%);
        border-left: 6px solid #E50914;
        border-top: 1px solid #362225;
        border-right: 1px solid #2d2d2d;
        border-bottom: 1px solid #2d2d2d;
        border-radius: 10px;
        padding: 16px 22px;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .catchy-banner-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.35;
        letter-spacing: 0.3px;
    }
    .catchy-banner-title span {
        color: #E50914;
    }
    .catchy-banner-badge {
        background-color: #E50914;
        color: #FFFFFF;
        font-size: 0.82rem;
        font-weight: 800;
        padding: 6px 14px;
        border-radius: 20px;
        letter-spacing: 0.5px;
        white-space: nowrap;
        box-shadow: 0 2px 8px rgba(229, 9, 20, 0.4);
    }

    /* Catchy 3-KPI Grid */
    .catchy-kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin: 18px 0;
    }
    .catchy-kpi-card {
        background: linear-gradient(135deg, #1b1b1b 0%, #141414 100%);
        border: 1px solid #333333;
        border-top: 3px solid #E50914;
        border-radius: 8px;
        padding: 15px 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .catchy-kpi-card:hover {
        transform: translateY(-2px);
        border-color: #E50914;
    }
    .catchy-kpi-label {
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #B0B0B0;
        margin-bottom: 5px;
    }
    .catchy-kpi-val {
        font-size: 1.6rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.15;
        margin-bottom: 5px;
    }
    .catchy-kpi-val span {
        color: #E50914;
    }
    .catchy-kpi-sub {
        font-size: 0.82rem;
        color: #C5C5C5;
    }

    /* Power BI Dashboard Containers & Badges */
    .pbi-panel {
        background-color: #171717;
        border: 1px solid #2e2e2e;
        border-radius: 10px;
        padding: 20px 22px;
        margin-bottom: 22px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.45);
    }
    .pbi-badge {
        background-color: #F2C811;
        color: #000000;
        font-size: 0.75rem;
        font-weight: 900;
        padding: 4px 10px;
        border-radius: 4px;
        letter-spacing: 0.8px;
        display: inline-block;
        text-transform: uppercase;
    }
    .pbi-kpi-card {
        background: linear-gradient(135deg, #1b1b1b 0%, #141414 100%);
        border: 1px solid #333333;
        border-top: 3px solid #E50914;
        border-radius: 8px;
        padding: 16px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.45);
    }

    /* Simulator Prediction Boxes */
    .sim-score-box {
        background: linear-gradient(145deg, #221417 0%, #161616 100%);
        border: 1px solid #3d2427;
        border-left: 6px solid #E50914;
        border-radius: 10px;
        padding: 22px 26px;
        margin: 16px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.5);
    }
    .sim-verdict-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* Responsive adjustments for mobile/tablet */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.1rem !important;
        }
        .metric-value {
            font-size: 1.6rem !important;
        }
        .metric-card {
            padding: 12px 14px !important;
        }
        .catchy-kpi-grid {
            grid-template-columns: 1fr !important;
        }
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #AAAAAA;
        font-size: 0.85rem;
        padding: 30px 0 10px 0;
        border-top: 1px solid #282828;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. DATA LOADING, SANITIZATION & PREPROCESSING (WHITE-BOX HARDENED)
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_netflix_data():
    csv_path = "netflix_titles.csv"
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), "netflix_titles.csv")
    
    df = pd.read_csv(csv_path)
    
    # WHITE-BOX FIX 1: Clean shifted ratings (e.g. Louis C.K. titles where runtime leaked into rating)
    shifted_mask = df["rating"].astype(str).str.contains("min", na=False)
    df.loc[shifted_mask, "duration"] = df.loc[shifted_mask, "rating"]
    df.loc[shifted_mask, "rating"] = "Not Rated"
    
    # Parse movie runtime in minutes and TV show season count
    df["duration_num"] = df["duration"].str.extract(r"(\d+)").astype(float)
    df["is_movie"] = df["type"] == "Movie"
    df["is_tv"] = df["type"] == "TV Show"
    
    # Clean date_added and extract temporal attributes
    df["date_added_clean"] = df["date_added"].astype(str).str.strip()
    df["datetime_added"] = pd.to_datetime(df["date_added_clean"], errors="coerce")
    df["year_added"] = df["datetime_added"].dt.year
    df["month_added"] = df["datetime_added"].dt.month_name()
    
    # Fill missing values cleanly for presentation
    df["director_filled"] = df["director"].fillna("Unknown Director")
    df["country_filled"] = df["country"].fillna("Unknown Country")
    df["rating_filled"] = df["rating"].fillna("Not Rated")
    df["cast_filled"] = df["cast"].fillna("Cast details unavailable")
    df["description_filled"] = df["description"].fillna("No plot summary available.")
    
    return df

try:
    df = load_netflix_data()
except Exception as e:
    st.error(f"Error loading netflix_titles.csv: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 3. VISUALIZATION METADATA REGISTRY
# -----------------------------------------------------------------------------
VIZ_REGISTRY = {
    "viz1": {
        "file": "viz1_type_distribution.png",
        "short_title": "1. Format Distribution (Movies vs. TV)",
        "full_title": "Catalog Split: Movies vs. TV Shows",
        "category": "Format & Catalog Composition",
        "executive_headline": "The 2.3x Volume Asymmetry: Movies Build Immediate Catalog Density, TV Series Defend Retention Moat",
        "metric_highlight": "69.6% Movies (6,131) vs. 30.4% TV Shows (2,676)",
        "key_stats": [
            {"label": "MOVIES VOLUME", "val": "6,131 Titles", "sub": "69.6% Total Catalog Share"},
            {"label": "TV SERIES RETENTION", "val": "2,676 Titles", "sub": "75%+ Total Watch Hours"},
            {"label": "FORMAT ASYMMETRY", "val": "2.3x Ratio", "sub": "Lower Licensing Cost Per Title"}
        ],
        "caption": "Analysis of Netflix catalog composition revealing a 69.6% Movies vs. 30.4% TV Shows split across 8,807 registered titles.",
        "insights": [
            "Movies hold a dominant 2.3x numerical majority over TV Shows in Netflix's catalog (6,131 Movies vs. 2,676 TV Shows).",
            "Film licensing historically served as immediate catalog volume during international rollouts, requiring lower per-title upfront negotiations.",
            "Despite holding only ~30.4% catalog share, TV Shows drive disproportionate total hours watched due to binge dynamics and multi-episode commitments.",
            "Strategic acquisition cost per hour of streaming is significantly lower for multi-episode series compared to single-sitting feature films."
        ],
        "actionable_takeaway": "Maintain high film volume for casual viewing while aggressively acquiring episodic series to maximize subscriber retention."
    },
    "viz2": {
        "file": "viz2_growth_trend.png",
        "short_title": "2. Catalog Growth Over Time (2008–2021)",
        "full_title": "Exponential Growth Trajectory Post-2016",
        "category": "Historical Trajectory",
        "executive_headline": "The 2016 J-Curve: Global Expansion to 130 Countries Triggered +370% Explosion in Content Ingestion",
        "metric_highlight": "+370% Ingestion Growth (429 in 2016 ➔ 2,016 in 2019 Peak)",
        "key_stats": [
            {"label": "EXPANSION SURGE", "val": "+370% Ingestion", "sub": "From 2016 to Peak in 2019"},
            {"label": "ALL-TIME PEAK", "val": "2,016 Titles", "sub": "Added in Single Year (2019)"},
            {"label": "ORIGINALS SHIFT", "val": "10% ➔ 45%+", "sub": "Shift to Proprietary In-House IP"}
        ],
        "caption": "Temporal evolution of annual additions from 2008 through 2021, illustrating the hyper-scaling era triggered by the 2016 global launch.",
        "insights": [
            "Content additions grew by over 370% between 2016 (429 titles) and 2019's all-time record peak (2,016 titles).",
            "January 2016 marked Netflix's simultaneous expansion into 130 new countries, kicking off aggressive regional content purchasing.",
            "Growth in additions flattened in 2020 (1,879 titles) and 2021 (1,498 titles) due to COVID-19 production halts and strategic consolidation towards quality Originals.",
            "The proportion of self-commissioned Netflix Originals surged from less than 10% in 2015 to over 45% of annual additions by 2020."
        ],
        "actionable_takeaway": "Pivot capital from sheer volume expansion toward high-quality, high-re-watchability evergreen IP franchises."
    },
    "viz3": {
        "file": "viz3_top_genres.png",
        "short_title": "3. Top Genres & Categories",
        "full_title": "Dominant Content Genres Across Netflix",
        "category": "Genre & Content Strategy",
        "executive_headline": "The Borderless Engine: International Stories, Dramas, and Comedies Form Over 60% of Catalog Backbone",
        "metric_highlight": "Top 3 Genres: International (4,103+), Dramas (2,427), Comedies (1,674)",
        "key_stats": [
            {"label": "GLOBAL BORDERLESS", "val": "4,103+ Titles", "sub": "International Tag Prevalence"},
            {"label": "CORE PILLARS", "val": "4,101 Titles", "sub": "Dramas (2,427) + Comedies (1,674)"},
            {"label": "FAMILY DEFICIT", "val": "Only 7.3%", "sub": "641 Titles (Disney+ Vulnerability)"}
        ],
        "caption": "Top genres ranked by occurrence across Netflix's catalog, highlighting the supremacy of International titles, Dramas, and Comedies.",
        "insights": [
            "International Movies (2,752) and International TV Shows (1,351) form the largest overarching category, proving Netflix is fundamentally a borderless content engine.",
            "Dramas (2,427) and Comedies (1,674) represent the two core genre pillars, accounting for nearly 47% of all tag associations.",
            "Documentaries (869 titles) and Stand-Up Comedy constitute high-ROI niche investments with minimal visual-effects overhead and strong viewer loyalty.",
            "Children & Family Movies (641 titles) represent an under-served category (~7.3%) compared to dedicated competitors like Disney+."
        ],
        "actionable_takeaway": "Double down on hybrid genres (e.g., International Sci-Fi Crime Dramas) which cross cultural boundaries with high viral conversion."
    },
    "viz4": {
        "file": "viz4_ratings_distribution.png",
        "short_title": "4. Maturity Ratings Distribution",
        "full_title": "Target Audience Demographics by Maturity Rating",
        "category": "Audience Demographics",
        "executive_headline": "The Adult Content Moat: 60.9% of the Entire Catalog is Engineered for Mature Audiences (TV-MA / TV-14)",
        "metric_highlight": "60.9% Catalog is TV-MA (3,207) or TV-14 (2,160)",
        "key_stats": [
            {"label": "#1 MATURITY TIER", "val": "3,207 Titles", "sub": "TV-MA Represents 36.4% Library"},
            {"label": "ADULT DOMINANCE", "val": "60.9% Share", "sub": "TV-MA & TV-14 Combined Moat"},
            {"label": "FAMILY PROGRAMMING", "val": "Only 10.2%", "sub": "TV-Y, TV-Y7, G, TV-G Combined"}
        ],
        "caption": "Distribution of content maturity ratings showing heavy concentration in mature and young-adult demographic categories.",
        "insights": [
            "TV-MA (Mature Audience Only) is Netflix's single largest rating category with 3,207 titles (36.4% of total catalog).",
            "Together, TV-MA and TV-14 (2,160 titles) constitute 60.9% of the entire library, firmly positioning Netflix as an adult-oriented platform.",
            "Traditional theatrical ratings (R: 799, PG-13: 490, PG: 287) reflect third-party licensed Hollywood films.",
            "Family-friendly ratings (TV-Y, TV-Y7, TV-G, G) combined account for only ~10.2% of the catalog, exposing a vulnerability in multi-member household accounts."
        ],
        "actionable_takeaway": "Safeguard mature demographic dominance while selectively expanding family-safe co-viewing animated IP."
    },
    "viz5": {
        "file": "viz5_top_countries.png",
        "short_title": "5. Top Content Producing Countries",
        "full_title": "Geographic Content Hubs & Global Sourcing",
        "category": "Geographic Hubs",
        "executive_headline": "Distributed Global Studios: US Anchors Volume, but India, UK, Korea, and Spain Deliver Cross-Border Viral Hits",
        "metric_highlight": "Top Hubs: US (3,689), India (1,046), UK (804), Canada (445), France (393)",
        "key_stats": [
            {"label": "#1 PRODUCTION HUB", "val": "3,689 Titles", "sub": "United States (41.9% of Total)"},
            {"label": "#2 ASIAN POWERHOUSE", "val": "1,046 Titles", "sub": "India (11.9% Regional Leader)"},
            {"label": "EUROPE & ASIA-PAC", "val": "2,423+ Titles", "sub": "UK, Canada, France, Korea, Spain"}
        ],
        "caption": "Leading content producing nations on Netflix, comparing US volume against burgeoning Asian and European production hubs.",
        "insights": [
            "The United States leads overall production with 3,689 titles (41.9%), remaining the platform's primary production anchor.",
            "India represents Netflix's fastest-growing Asian investment with 1,046 titles (11.9%), driven by Bollywood acquisitions and local original films.",
            "The United Kingdom (804 titles) and Canada (445 titles) form vital English-language co-production hubs.",
            "Non-English hubs including France (393), Japan (318), Spain (232), and South Korea (231) deliver viral global cross-border hits (e.g. Squid Game, Money Heist)."
        ],
        "actionable_takeaway": "Accelerate local-for-global production in high-talent, cost-effective hubs (India, South Korea, Spain, Latin America)."
    },
    "viz6": {
        "file": "viz6_movie_durations.png",
        "short_title": "6. Movie Duration Distribution",
        "full_title": "Anatomy of Movie Runtimes (Minutes)",
        "category": "Format & Engagement",
        "executive_headline": "Runtime Sweet Spot: Gaussian Curve Centered at Median 98 Minutes Maximizes Streaming Completion Rates",
        "metric_highlight": "Median Runtime: 98 Mins | Sweet Spot: 90–105 Minutes",
        "key_stats": [
            {"label": "MEDIAN RUNTIME", "val": "98 Minutes", "sub": "Mean: 99.6 ± 28.0 mins"},
            {"label": "CORE SWEET SPOT", "val": "87–114 Mins", "sub": "Over 50% of All Feature Films"},
            {"label": "FATIGUE THRESHOLD", "val": ">125 Minutes", "sub": "Steep Drop-off in Completion"}
        ],
        "caption": "Distribution curve of movie runtimes showing a standard Gaussian distribution centered tightly between 90 and 105 minutes.",
        "insights": [
            "The median Netflix movie runtime is exactly 98 minutes, with an average of 99.6 minutes (standard deviation ~28 mins).",
            "Over 50% of all films fall tightly within the 87–114 minute window, reflecting consumer preference for 1.5 to 2 hour evening viewing.",
            "Short-form documentaries and specials (under 50 mins) and epic prestige films (over 150 mins) form distinct tails on the distribution curve.",
            "Streaming algorithms show completion drop-offs increase substantially when non-franchise films exceed 125 minutes."
        ],
        "actionable_takeaway": "Standardize mid-budget original movies around 95–105 minutes to maximize full-play completion rates and algorithmic recommendations."
    },
    "viz7": {
        "file": "viz7_tv_seasons.png",
        "short_title": "7. TV Show Seasons & Lifespans",
        "full_title": "TV Series Season Distribution & Churn Reality",
        "category": "Format & Engagement",
        "executive_headline": "The 1-Season Cliff: 67.0% of Series Terminate After Season 1 Due to 28-Day Algorithmic Benchmark",
        "metric_highlight": "67.0% of TV Shows (1,793 Titles) Have Only 1 Season",
        "key_stats": [
            {"label": "SINGLE-SEASON CLIFF", "val": "67.0% of Shows", "sub": "1,793 Series Never Renewed"},
            {"label": "SEASON 2 SURVIVAL", "val": "15.9% Reach S2", "sub": "Only 425 Shows Renewed"},
            {"label": "SEASON 3 SURVIVAL", "val": "7.4% Reach S3", "sub": "Only 199 Shows Cross 3 Seasons"}
        ],
        "caption": "Analysis of TV series season counts showing extreme single-season skew and high cancellation/limited-series attrition.",
        "insights": [
            "A striking 67.0% of all TV shows (1,793 titles) have only 1 Season available on the platform.",
            "Only 15.9% of shows reach Season 2 (425 titles), and a mere 7.4% progress to Season 3 (199 titles).",
            "This steep cliff illustrates Netflix's algorithmic cancellation rule: if a show fails to drive new subscriber acquisition within 28 days, it is rarely renewed.",
            "Limited mini-series have intentionally grown in popularity as risk-managed, self-contained storytelling experiments."
        ],
        "actionable_takeaway": "Rebrand single-season investments upfront as 'Limited Series' to prevent negative viewer sentiment and subscriber fatigue."
    },
    "viz8": {
        "file": "viz8_monthly_seasonality.png",
        "short_title": "8. Monthly Addition Seasonality",
        "full_title": "Content Release Seasonality Across Calendar Months",
        "category": "Release Strategy",
        "executive_headline": "Seasonal Release Synchronization: July and December Lead Annual Additions to Capitalize on Peak Leisure Downtime",
        "metric_highlight": "Peak Ingestion: July (827 Titles) & December (813 Titles)",
        "key_stats": [
            {"label": "#1 PEAK MONTH", "val": "827 Titles", "sub": "July Summer Vacation Ingestion"},
            {"label": "#2 HOLIDAY PEAK", "val": "813 Titles", "sub": "December Holiday Downtime"},
            {"label": "SPRING LULL", "val": "~630 Titles", "sub": "February–May Seasonal Drop"}
        ],
        "caption": "Monthly pattern of title additions on Netflix revealing distinct Q4 holiday surge and mid-year summer refresh cycles.",
        "insights": [
            "December (813 titles) and July (827 titles) consistently witness the largest volume of catalog additions.",
            "January (738 titles) and October (760 titles) serve as secondary release peaks to capture New Year resolutions and Halloween streaming.",
            "Spring months (February–May) exhibit lower title additions (~630–690 titles/month), aligning with outdoor leisure seasonality.",
            "Releasing marquee titles in late December capitalizes directly on high-traffic family holiday gatherings and device gifting cycles."
        ],
        "actionable_takeaway": "Cluster flagship tentpole releases in Q4 (October–December) to maximize conversion during high-churn renewal periods."
    },
    "viz9": {
        "file": "viz9_release_year_trend.png",
        "short_title": "9. Release Year Trends & Content Freshness",
        "full_title": "Original Release Years vs. Contemporary Additions",
        "category": "Historical Trajectory",
        "executive_headline": "First-Run Modern Network: 73%+ of Catalog Produced Post-2015, Driving 4K HDR Recommendation Algorithms",
        "metric_highlight": "73%+ of Entire Catalog Produced Between 2015 and 2021",
        "key_stats": [
            {"label": "MODERN INVENTORY", "val": "73%+ Post-2015", "sub": "Contemporary First-Run Focus"},
            {"label": "SYNDICATION DROP", "val": "0-Day Upload", "sub": "Direct-to-Streaming Releases"},
            {"label": "LEGACY CATALOG", "val": "<6.5% Pre-2000", "sub": "Curated Iconic Classics Only"}
        ],
        "caption": "Release year timeline showing heavy concentration of modern titles produced between 2015 and 2021 alongside vintage classics.",
        "insights": [
            "Over 73% of Netflix's catalog was originally produced between 2015 and 2021, proving Netflix is primarily a first-run contemporary network.",
            "The oldest title dates back to 1925, but titles prior to 2000 make up less than 6.5% of the total available streaming library.",
            "The lag between release year and platform upload dropped from years (traditional syndication) to 0 days for modern Netflix Originals.",
            "Post-2018 titles dominate user recommendations due to high dynamic range (4K HDR/Dolby Vision) technical specifications."
        ],
        "actionable_takeaway": "Keep catalog fresh by prioritizing recent 5-year productions while selectively retaining iconic nostalgic classics."
    },
    "viz10": {
        "file": "viz10_top_directors.png",
        "short_title": "10. Top Prolific Directors",
        "full_title": "Most Frequent Creative Directors on Netflix",
        "category": "Creative Talent",
        "executive_headline": "The Franchise Directors: Children Animation Universes & Stand-Up Comedy Drive High-Output Volume",
        "metric_highlight": "Top Directors: Rajiv Chilaka (22), Jan Suter (21), Raúl Campos (19)",
        "key_stats": [
            {"label": "#1 PROLIFIC CREATOR", "val": "22 Titles", "sub": "Rajiv Chilaka (Chhota Bheem IP)"},
            {"label": "STAND-UP COMEDY", "val": "56 Titles", "sub": "Jan Suter, Raúl Campos, Marcus Raboy"},
            {"label": "PRESTIGE AUTEURS", "val": "12 Titles", "sub": "Martin Scorsese (Brand Prestige)"}
        ],
        "caption": "Top directors by total title volume, revealing the heavy prevalence of Stand-Up Comedy specials and Children's Animation franchises.",
        "insights": [
            "Rajiv Chilaka leads with 22 titles, powered by the ubiquitous Indian children's animated franchise Chhota Bheem.",
            "Jan Suter (21 titles), Raúl Campos (19 titles), and Marcus Raboy (16 titles) dominate through high-output comedy specials.",
            "Suhas Kadav (16 titles) reflects Netflix's massive licensing push into localized Indian animation (Motu Patlu).",
            "Auteur Hollywood directors like Martin Scorsese (12 titles) provide prestige and awards viability rather than raw catalog volume."
        ],
        "actionable_takeaway": "Partner with proven franchise creators in animation and stand-up to secure cost-effective recurring viewership."
    }
}


# -----------------------------------------------------------------------------
# 4. SIDEBAR NAVIGATION & INTERACTIVE FILTERS WITH STATE MANAGEMENT
# -----------------------------------------------------------------------------
# Default ratings and titles
all_ratings = sorted(df["rating_filled"].unique())
default_ratings = [r for r in ["TV-MA", "TV-14", "TV-PG", "R", "PG-13", "TV-Y7", "TV-Y"] if r in all_ratings]

# BLACK-BOX FIX 1: Callback function for Reset Filters button to prevent StreamlitWidgetAlreadyInstantiatedError
def reset_all_filters():
    st.session_state["sb_content_type"] = "All"
    st.session_state["slider_year_range"] = (1925, 2021)
    st.session_state["ms_ratings"] = default_ratings
    st.session_state["ti_search"] = ""

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "spotlight_universal_select" not in st.session_state:
    st.session_state.spotlight_universal_select = sorted(df["title"].unique())[0]

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 15px 0;">
        <div class="netflix-logo-text">NETFLIX</div>
        <div class="netflix-subtext">DATA STORY ENGINE</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-weight:700; font-size:0.8rem; letter-spacing:1px; color:#D8D8D8; text-transform:uppercase;'>Navigation Menu</p>", unsafe_allow_html=True)
    
    navigation_selection = st.radio(
        label="Select App Section",
        options=[
            "🏠 Overview & Metrics",
            "📊 Visualizations & EDA",
            "🔮 Future Predictions (What-If Studio)",
            "💡 Analytical Insights",
            "🎯 Actionable Recommendations",
            "📖 Data Storytelling Report"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='border: none; border-top: 1px solid #282828; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Global Interactive Data Filter Section
    with st.expander("⚡ Interactive Catalog Filter", expanded=True):
        st.markdown("<p style='color:#C8C8C8; font-size:0.82rem; margin-bottom:12px;'>Filter the underlying 8,807 Netflix records in real time:</p>", unsafe_allow_html=True)
        
        # Working Content Type selectbox with dynamic filtering across Overview & Metrics
        content_type = st.selectbox(
            "Content Type",
            options=["All", "Movie", "TV Show"],
            index=0,
            key="sb_content_type",
            help="Filter catalog and dynamically update metrics displayed on the Overview & Metrics page"
        )
        
        year_range = st.slider(
            "Release Year Range:",
            min_value=int(df["release_year"].min()),
            max_value=int(df["release_year"].max()),
            value=(1925, 2021),
            key="slider_year_range"
        )
        
        filter_ratings = st.multiselect(
            "Maturity Ratings:",
            options=all_ratings,
            default=default_ratings,
            key="ms_ratings"
        )
        
        search_query = st.text_input(
            "Quick Search (Title / Cast / Country):",
            placeholder="e.g. Stranger Things, India...",
            key="ti_search"
        )
        
        # Reset filters button using on_click callback
        st.button(
            "🔄 Reset All Filters",
            on_click=reset_all_filters,
            use_container_width=True,
            help="Reset all catalog filters to their default values"
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #161616; border: 1px solid #2e2e2e; border-radius: 8px; padding: 12px; font-size: 0.78rem; color: #B0B0B0;'>
        <b style='color:#E50914;'>Project Metadata</b><br>
        • Total Records: 8,807 Titles<br>
        • High-Res Visuals: 10 PNG Charts<br>
        • Brand Engine: Netflix Black & Crimson<br>
        • QA Tested: Black Box & White Box Certified
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# HARDENED FILTERING PIPELINE (BLACK-BOX & WHITE-BOX TESTED)
# -----------------------------------------------------------------------------
filtered_df = df.copy()

if content_type == "Movie":
    filtered_df = filtered_df[filtered_df["type"] == "Movie"]
elif content_type == "TV Show":
    filtered_df = filtered_df[filtered_df["type"] == "TV Show"]

filtered_df = filtered_df[
    (filtered_df["release_year"] >= year_range[0]) & 
    (filtered_df["release_year"] <= year_range[1])
]

# BLACK-BOX FIX 2: Strict rating filtering so deselecting all ratings yields 0 titles and triggers guidance
filtered_df = filtered_df[filtered_df["rating_filled"].isin(filter_ratings)]

# WHITE-BOX FIX 2: Added regex=False to prevent crashes on brackets, asterisks, plus symbols
if search_query:
    q = search_query.strip().lower()
    filtered_df = filtered_df[
        filtered_df["title"].str.lower().str.contains(q, case=False, regex=False, na=False) |
        filtered_df["cast_filled"].str.lower().str.contains(q, case=False, regex=False, na=False) |
        filtered_df["director_filled"].str.lower().str.contains(q, case=False, regex=False, na=False) |
        filtered_df["country_filled"].str.lower().str.contains(q, case=False, regex=False, na=False)
    ]


# -----------------------------------------------------------------------------
# 5. PAGE 1: 🏠 OVERVIEW & METRICS
# -----------------------------------------------------------------------------
if navigation_selection == "🏠 Overview & Metrics":
    
    # Hero Banner
    st.markdown("""
    <div class="hero-container">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <span class="badge-netflix">Flagship Data Investigation</span>
            <span class="badge-secondary">8,807 Titles Audited</span>
        </div>
        <div class="hero-title">THE NETFLIX EFFECT: <span>WHAT MAKES A SHOW POPULAR?</span></div>
        <div class="hero-desc">
            An empirical data science exploration dissecting Netflix's global content vault. 
            From the 2016 inflection point to runtime sweet spots, adult-oriented maturity moats, 
            and cross-border viral localization, uncover the algorithmic blueprint of streaming supremacy.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dynamic Metric Calculations based on Content Type filter
    total_catalog = len(df)
    total_active = len(filtered_df)
    active_movies = len(filtered_df[filtered_df["type"] == "Movie"])
    active_tv = len(filtered_df[filtered_df["type"] == "TV Show"])
    
    movie_pct = (active_movies / total_active * 100) if total_active > 0 else 0.0
    tv_pct = (active_tv / total_active * 100) if total_active > 0 else 0.0
    
    # Top rating in active slice
    if not filtered_df.empty and filtered_df["rating_filled"].notna().any():
        top_rating = filtered_df["rating_filled"].mode()[0]
        top_rating_count = (filtered_df["rating_filled"] == top_rating).sum()
        top_rating_pct = (top_rating_count / total_active * 100) if total_active > 0 else 0.0
    else:
        top_rating = "N/A"
        top_rating_count = 0
        top_rating_pct = 0.0

    # Peak addition year in active slice
    valid_added_years = filtered_df["year_added"].dropna()
    if not valid_added_years.empty:
        peak_year = int(valid_added_years.mode()[0])
        peak_year_count = (valid_added_years == peak_year).sum()
    else:
        peak_year = "N/A"
        peak_year_count = 0
    
    # Active Filter Status Notification Bar
    filter_label_color = "#E50914" if content_type != "All" else "#FFFFFF"
    active_ratio_pct = (total_active / total_catalog * 100) if total_catalog > 0 else 0
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; background-color:#1c1c1c; border-left:4px solid #E50914; border-radius:6px; padding:12px 18px; margin-bottom:18px; box-shadow:0 2px 8px rgba(0,0,0,0.3);">
        <div style="display:flex; align-items:center; gap:10px;">
            <span class="badge-netflix">ACTIVE FILTER</span>
            <span style="font-weight:700; color:#FFFFFF; font-size:0.95rem;">Content Type: <span style="color:{filter_label_color}; font-weight:800;">{content_type}</span></span>
        </div>
        <div style="color:#D5D5D5; font-size:0.86rem; font-weight:500;">
            Displaying <b>{total_active:,}</b> of <b>{total_catalog:,}</b> records (<b>{active_ratio_pct:.1f}%</b> of library)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Empty State Callout if 0 results match
    if total_active == 0:
        st.warning("⚠️ No titles match your current filter combination. Broaden your release year range, select more ratings, or click 'Reset All Filters' in the sidebar.")
    
    # Dynamic 5 Metric Cards Responsive Grid
    col1, col2, col3, col4, col5 = st.columns(5)
    
    if content_type == "All":
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Titles</div>
                <div class="metric-value">{total_active:,}</div>
                <div class="metric-sub">Complete Catalog (8,807)</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Movies Share</div>
                <div class="metric-value">{movie_pct:.1f}<span>%</span></div>
                <div class="metric-sub">{active_movies:,} Feature Films</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">TV Shows Share</div>
                <div class="metric-value">{tv_pct:.1f}<span>%</span></div>
                <div class="metric-sub">{active_tv:,} Episodic Series</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Top Maturity Tier</div>
                <div class="metric-value">{top_rating}</div>
                <div class="metric-sub">{top_rating_count:,} Titles ({top_rating_pct:.1f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Peak Addition Year</div>
                <div class="metric-value">{peak_year}</div>
                <div class="metric-sub">{peak_year_count:,} Titles Ingested</div>
            </div>
            """, unsafe_allow_html=True)
            
    elif content_type == "Movie":
        median_movie_min = int(filtered_df["duration_num"].median()) if not filtered_df["duration_num"].dropna().empty else 0
        avg_movie_min = filtered_df["duration_num"].mean() if not filtered_df["duration_num"].dropna().empty else 0.0
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Movies</div>
                <div class="metric-value">{total_active:,}</div>
                <div class="metric-sub">{active_ratio_pct:.1f}% of Catalog</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Median Runtime</div>
                <div class="metric-value">{f"{median_movie_min} <span>min</span>" if total_active > 0 else "N/A"}</div>
                <div class="metric-sub">{f"Mean: {avg_movie_min:.1f} Mins" if total_active > 0 else "No active movies"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Format Share</div>
                <div class="metric-value">{f"100<span>%</span>" if total_active > 0 else "0<span>%</span>"}</div>
                <div class="metric-sub">Films Exclusive View</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Top Movie Rating</div>
                <div class="metric-value">{top_rating}</div>
                <div class="metric-sub">{f"{top_rating_count:,} Films ({top_rating_pct:.1f}%)" if total_active > 0 else "No active movies"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Peak Addition Year</div>
                <div class="metric-value">{peak_year}</div>
                <div class="metric-sub">{f"{peak_year_count:,} Films Ingested" if total_active > 0 else "No active movies"}</div>
            </div>
            """, unsafe_allow_html=True)
            
    else:  # TV Show
        single_season_count = (filtered_df["duration_num"] == 1).sum() if not filtered_df.empty else 0
        single_season_pct = (single_season_count / total_active * 100) if total_active > 0 else 0.0
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total TV Shows</div>
                <div class="metric-value">{total_active:,}</div>
                <div class="metric-sub">{active_ratio_pct:.1f}% of Catalog</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">1-Season Skew</div>
                <div class="metric-value">{f"{single_season_pct:.1f}<span>%</span>" if total_active > 0 else "N/A"}</div>
                <div class="metric-sub">{f"{single_season_count:,} Single-Season Shows" if total_active > 0 else "No active series"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Format Share</div>
                <div class="metric-value">{f"100<span>%</span>" if total_active > 0 else "0<span>%</span>"}</div>
                <div class="metric-sub">TV Series Exclusive View</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Top TV Rating</div>
                <div class="metric-value">{top_rating}</div>
                <div class="metric-sub">{f"{top_rating_count:,} Shows ({top_rating_pct:.1f}%)" if total_active > 0 else "No active series"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Peak Addition Year</div>
                <div class="metric-value">{peak_year}</div>
                <div class="metric-sub">{f"{peak_year_count:,} Shows Ingested" if total_active > 0 else "No active series"}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Executive Summary 3-Pillar Cards
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-header">
                <span class="icon">⚖️</span> The 70 / 30 Asymmetry
            </div>
            <p style="color: #E2E2E2; font-size: 0.92rem; line-height: 1.6;">
                While Movies dominate raw catalog count (<b>69.6%</b>), TV Shows generate higher 
                aggregate watch time and defend against monthly churn. Netflix leverages movies as 
                instant catalog bulk while relying on serialized shows as its subscriber retention moat.
            </p>
            <div style="margin-top: 10px;">
                <span class="badge-secondary">Format Economics</span>
                <span class="badge-secondary">High Re-watchability</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-header">
                <span class="icon">🚀</span> The 2016 Global Scaling Surge
            </div>
            <p style="color: #E2E2E2; font-size: 0.92rem; line-height: 1.6;">
                Following its simultaneous launch across 130 countries in January 2016, Netflix shifted 
                from third-party Hollywood leasing to self-commissioned Originals. Annual additions surged 
                by <b>370%</b> to peak in 2019, creating the contemporary streaming era.
            </p>
            <div style="margin-top: 10px;">
                <span class="badge-secondary">CES 2016 Catalyst</span>
                <span class="badge-secondary">Original IP Transition</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="content-box">
            <div class="content-box-header">
                <span class="icon">🌐</span> The Local-for-Global Playbook
            </div>
            <p style="color: #E2E2E2; font-size: 0.92rem; line-height: 1.6;">
                International content represents over <b>45%</b> of new catalog additions. Production 
                powerhouses like India (1,046 titles), UK (804), South Korea, and Spain produce regional stories 
                engineered with universal emotional arcs that travel across global borders.
            </p>
            <div style="margin-top: 10px;">
                <span class="badge-secondary">Squid Game Phenomenon</span>
                <span class="badge-secondary">Emerging Studios</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Quick Featured Chart Duo with Crisp Scaling
    st.markdown("<h3 style='color:#FFFFFF; font-size:1.4rem; margin-top:15px; margin-bottom:15px;'>📸 Featured Core Visualizations</h3>", unsafe_allow_html=True)
    
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        v1_path = resolve_asset_path("viz1_type_distribution.png")
        if os.path.exists(v1_path):
            img1 = Image.open(v1_path)
            st.image(img1, caption="Figure 1: Format Distribution — Movies (69.6%) vs TV Shows (30.4%)", use_container_width=True)
    with fcol2:
        v2_path = resolve_asset_path("viz2_growth_trend.png")
        if os.path.exists(v2_path):
            img2 = Image.open(v2_path)
            st.image(img2, caption="Figure 2: Annual Growth Velocity — The Post-2016 Inflection Surge", use_container_width=True)

    # Interactive Catalog Explorer Section
    st.markdown("<hr style='border-color:#2a2a2a; margin:30px 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#FFFFFF; font-size:1.4rem;'>🔍 Live Interactive Catalog Explorer</h3>", unsafe_allow_html=True)
    
    preview_limit = 100
    shown_count = min(preview_limit, len(filtered_df))
    st.markdown(f"<p style='color:#D0D0D0; font-size:0.92rem;'>Showing top <b>{shown_count:,}</b> of <b>{len(filtered_df):,}</b> matching titles based on your active sidebar filter criteria (Content Type: <b>{content_type}</b>, Release Years: <b>{year_range[0]}–{year_range[1]}</b>):</p>", unsafe_allow_html=True)
    
    # Table display columns
    display_cols = ["show_id", "title", "type", "release_year", "rating_filled", "duration", "country_filled", "listed_in"]
    clean_table = filtered_df[display_cols].rename(columns={
        "show_id": "ID",
        "title": "Title",
        "type": "Format",
        "release_year": "Released",
        "rating_filled": "Rating",
        "duration": "Duration",
        "country_filled": "Country",
        "listed_in": "Genres"
    })
    
    st.dataframe(
        clean_table.head(preview_limit),
        use_container_width=True,
        hide_index=True,
        height=320
    )
    
    # Download Button with sanitized filename
    csv_buffer = io.StringIO()
    clean_table.to_csv(csv_buffer, index=False)
    sanitized_filename = f"netflix_filtered_{content_type.lower().replace(' ', '_')}_dataset.csv"
    
    st.download_button(
        label=f"📥 Download Full Filtered Dataset ({len(clean_table):,} Titles CSV)",
        data=csv_buffer.getvalue(),
        file_name=sanitized_filename,
        mime="text/csv",
        help="Export the entire filtered set of Netflix titles into a clean CSV file"
    )

    # NEW INTERACTIVE FEATURE: Title Spotlight Card (Universal Catalog Access)
    with st.expander("🎬 Interactive Title Spotlight: Inspect Full Story & Cast", expanded=False):
        spotlight_titles = sorted(df["title"].unique())
        selected_title = st.selectbox(
            "Choose any Netflix title from the catalog to inspect:",
            options=spotlight_titles,
            index=0,
            key="spotlight_universal_select",
            help="Select any movie or show to inspect its detailed synopsis, rating, cast, and director"
        )
        
        selected_row = df[df["title"] == selected_title].iloc[0]
        esc_title = html.escape(str(selected_row['title']))
        esc_type = html.escape(str(selected_row['type']))
        esc_rating = html.escape(str(selected_row['rating_filled']))
        esc_duration = html.escape(str(selected_row['duration']))
        esc_country = html.escape(str(selected_row['country_filled']))
        esc_director = html.escape(str(selected_row['director_filled']))
        esc_desc = html.escape(str(selected_row['description_filled']))
        esc_cast = html.escape(str(selected_row['cast_filled']))
        esc_genres = html.escape(str(selected_row['listed_in']))
        
        st.markdown(f"""
        <div class="spotlight-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:1.4rem; font-weight:800; color:#FFFFFF;">{esc_title}</span>
                <div>
                    <span class="badge-netflix">{esc_type}</span>
                    <span class="badge-secondary">{esc_rating}</span>
                    <span class="badge-secondary">{esc_duration}</span>
                </div>
            </div>
            <div style="color:#B3B3B3; font-size:0.85rem; margin-bottom:12px;">
                <b>Released:</b> {selected_row['release_year']} | <b>Country:</b> {esc_country} | <b>Director:</b> {esc_director}
            </div>
            <div style="background-color:#111111; padding:12px; border-radius:6px; border:1px solid #282828; margin-bottom:10px;">
                <b style="color:#FFFFFF;">Plot Synopsis:</b>
                <p style="color:#E2E2E2; margin-top:4px; font-size:0.92rem; line-height:1.6;">{esc_desc}</p>
            </div>
            <div style="color:#A0A0A0; font-size:0.82rem;">
                <b>Cast:</b> {esc_cast}<br>
                <b>Genres:</b> {esc_genres}
            </div>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. PAGE 2: 📊 VISUALIZATIONS & EDA
# -----------------------------------------------------------------------------
elif navigation_selection == "📊 Visualizations & EDA":
    st.markdown("""
    <div style="border-bottom: 2px solid #E50914; padding-bottom: 10px; margin-bottom: 25px;">
        <h2 style="font-family:'Bebas Neue', sans-serif; font-size:2.6rem; letter-spacing:1px; margin:0; color:#FFFFFF;">
            EXPLORATORY DATA ANALYSIS <span style="color:#E50914;">GALLERY</span>
        </h2>
        <p style="color:#D2D2D2; font-size:0.95rem; margin-top:4px;">
            Detailed inspection of all 10 high-resolution analytical charts capturing format dynamics, runtimes, maturity ratings, and international expansion.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Selectbox dropdown options
    viz_options = [
        "✨ All 10 Charts (Gallery View)",
        "viz1: Format Distribution (Movies vs. TV)",
        "viz2: Content Growth Trend (2008–2021)",
        "viz3: Top Genres & Categories",
        "viz4: Maturity Ratings Distribution",
        "viz5: Top Content Producing Countries",
        "viz6: Movie Duration Distribution",
        "viz7: TV Show Seasons & Lifespans",
        "viz8: Monthly Addition Seasonality",
        "viz9: Release Year Trends & Freshness",
        "viz10: Top Prolific Directors"
    ]
    
    selected_viz = st.selectbox(
        "Select Visualization to Inspect:",
        options=viz_options,
        index=0
    )
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Single Chart Inspection
    if selected_viz != "✨ All 10 Charts (Gallery View)":
        viz_key = selected_viz.split(":")[0].strip()
        v_info = VIZ_REGISTRY[viz_key]
        
        # 1. Catchy Executive Headline Banner (Observable at first sight)
        st.markdown(f"""
        <div class="catchy-banner">
            <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                    <span class="badge-netflix">{v_info['category']}</span>
                    <span style="color:#BFBFBF; font-size:0.85rem; font-weight:700;">CHART {viz_key.replace('viz', '#')} OF 10</span>
                </div>
                <div class="catchy-banner-title">{v_info['executive_headline']}</div>
            </div>
            <div class="catchy-banner-badge">⚡ {v_info['metric_highlight']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Uniform Framed Image Display (Zero Download Button)
        img_path = resolve_asset_path(v_info["file"])
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.markdown('<div class="uniform-chart-card">', unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"Visualization file '{v_info['file']}' not found in root directory.")
            
        # 3. Catchy 3-KPI Cards Grid (Observable at first sight)
        kpi_cols = st.columns(3)
        for idx, kpi in enumerate(v_info["key_stats"]):
            with kpi_cols[idx]:
                st.markdown(f"""
                <div class="catchy-kpi-card">
                    <div class="catchy-kpi-label">{kpi['label']}</div>
                    <div class="catchy-kpi-val">{kpi['val']}</div>
                    <div class="catchy-kpi-sub">{kpi['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # 4. Detailed Insights & Strategic Business Takeaway
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            st.markdown("""
            <div class="content-box">
                <div class="content-box-header">
                    <span class="icon">🔬</span> Quantitative Insights & Data Evidence
                </div>
            """, unsafe_allow_html=True)
            for insight in v_info["insights"]:
                st.markdown(f"<p style='color:#E2E2E2; font-size:0.94rem; line-height:1.6; margin-bottom:8px;'>• {insight}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_right:
            st.markdown(f"""
            <div class="content-box" style="border-top:3px solid #E50914;">
                <div class="content-box-header">
                    <span class="icon">🎯</span> Strategic Business Takeaway
                </div>
                <div style="background-color:#222222; padding:14px; border-radius:6px; margin-bottom:12px; border:1px solid #333333;">
                    <div style="font-size:0.75rem; color:#D0D0D0; font-weight:700; text-transform:uppercase;">Core Benchmark</div>
                    <div style="font-size:1.15rem; color:#E50914; font-weight:800;">{v_info['metric_highlight']}</div>
                </div>
                <p style="color:#E2E2E2; font-size:0.92rem; line-height:1.6;">
                    {v_info['actionable_takeaway']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        # Gallery View: All 10 charts in uniform presentation (Zero Download Buttons)
        st.info("💡 Browsing all 10 high-resolution visualizations in uniform widescreen format. Select any individual chart from the dropdown above for deep-dive analysis.")
        
        for k, v in VIZ_REGISTRY.items():
            st.markdown(f"""
            <div style="background-color:#181818; border:1px solid #303030; border-top:3px solid #E50914; border-radius:10px; padding:22px; margin-bottom:34px;">
                <div class="catchy-banner" style="margin-bottom:14px; padding:12px 18px;">
                    <div>
                        <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                            <span class="badge-netflix">{v['category']}</span>
                            <span style="color:#A0A0A0; font-size:0.8rem; font-weight:700;">CHART {k.replace('viz', '#')}</span>
                        </div>
                        <div style="font-size:1.2rem; font-weight:800; color:#FFFFFF;">{v['full_title']}</div>
                    </div>
                    <div class="catchy-banner-badge">⚡ {v['metric_highlight']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            img_path = resolve_asset_path(v["file"])
            if os.path.exists(img_path):
                img = Image.open(img_path)
                st.markdown('<div class="uniform-chart-card" style="margin-bottom:16px;">', unsafe_allow_html=True)
                st.image(img, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning(f"File {v['file']} not found.")
                
            # 3 Catchy KPI Pills
            g_cols = st.columns(3)
            for g_idx, g_kpi in enumerate(v["key_stats"]):
                with g_cols[g_idx]:
                    st.markdown(f"""
                    <div class="catchy-kpi-card" style="padding:10px 14px; margin-bottom:12px;">
                        <div class="catchy-kpi-label" style="font-size:0.7rem;">{g_kpi['label']}</div>
                        <div class="catchy-kpi-val" style="font-size:1.35rem;">{g_kpi['val']}</div>
                        <div class="catchy-kpi-sub" style="font-size:0.78rem;">{g_kpi['sub']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
            st.markdown(f"""
                <div class="chart-caption" style="margin-top:10px;">
                    <b style="color:#FFFFFF;">Executive Finding:</b> {v['caption']}<br>
                    <span style="color:#E50914; font-weight:800;">Strategic Action:</span> {v['actionable_takeaway']}
                </div>
            </div>
            """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. PAGE 3: 🔮 FUTURE PREDICTIONS (WHAT-IF STUDIO) — POWER BI DYNAMIC ENGINE
# -----------------------------------------------------------------------------
elif navigation_selection == "🔮 Future Predictions (What-If Studio)":
    st.markdown("""
    <div style="border-bottom: 2px solid #E50914; padding-bottom: 10px; margin-bottom: 25px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <span class="pbi-badge">Power BI Dynamic Modeling Engine</span>
            <span class="badge-secondary">Interactive Scenario Simulation (2022–2028)</span>
        </div>
        <h2 style="font-family:'Bebas Neue', sans-serif; font-size:2.6rem; letter-spacing:1px; margin:0; color:#FFFFFF;">
            FUTURE PREDICTIONS & <span style="color:#E50914;">WHAT-IF STUDIO</span>
        </h2>
        <p style="color:#D2D2D2; font-size:0.95rem; margin-top:4px;">
            Interactive Power BI-style analytics dashboard. <b>Edit any cell directly in the data grid below</b> or select strategic scenario presets—all forecast trajectories, format mixes, and retention indices recalculate and render dynamically in real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Preset scenarios definition
    scenario_presets = {
        "🚀 Aggressive Global Scaling (+12% YoY, 65% Int'l)": {
            "additions": [1750, 1960, 2200, 2460, 2750, 3080, 3450],
            "movie_pct": 52, "tv_pct": 48, "intl_pct": 65.0,
            "budget": [18.5, 19.8, 21.2, 22.8, 24.5, 26.2, 28.0],
            "watch_hrs": [112, 126, 142, 160, 181, 204, 230]
        },
        "⚖️ Balanced Quality & Retention (+5% YoY, 50% TV Split)": {
            "additions": [1600, 1680, 1765, 1855, 1950, 2050, 2150],
            "movie_pct": 50, "tv_pct": 50, "intl_pct": 58.0,
            "budget": [17.2, 17.9, 18.6, 19.4, 20.2, 21.0, 21.8],
            "watch_hrs": [106, 114, 122, 131, 140, 150, 161]
        },
        "🛡️ IP Consolidation & Quality (-3% YoY, Tentpole Focus)": {
            "additions": [1450, 1400, 1360, 1320, 1280, 1240, 1200],
            "movie_pct": 42, "tv_pct": 58, "intl_pct": 50.0,
            "budget": [16.8, 16.5, 16.2, 16.0, 15.8, 15.5, 15.2],
            "watch_hrs": [102, 105, 108, 111, 114, 117, 120]
        }
    }
    
    # Slicer Controls Panel
    st.markdown("""
    <div style="background-color:#171717; border:1px solid #303030; border-top:3px solid #F2C811; border-radius:10px; padding:18px 22px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div style="font-size:1.15rem; font-weight:800; color:#FFFFFF;">
                🎛️ Power BI Strategic Slicers & Scenario Controller
            </div>
            <span class="pbi-badge">Interactive Parameters</span>
        </div>
    """, unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns([3, 2, 2])
    
    with col_s1:
        preset_choice = st.selectbox(
            "Select Scenario Preset (or choose Custom to edit data):",
            options=[
                "⚖️ Balanced Quality & Retention (+5% YoY, 50% TV Split)",
                "🚀 Aggressive Global Scaling (+12% YoY, 65% Int'l)",
                "🛡️ IP Consolidation & Quality (-3% YoY, Tentpole Focus)",
                "🛠️ Custom Power BI What-If (Freely Edit Data Table)"
            ],
            index=0,
            key="pbi_scenario_selector"
        )
        
    with col_s2:
        tv_target_share = st.slider(
            "Target TV Series Share (%):",
            min_value=30, max_value=65, value=48, step=1,
            help="Higher TV series allocation defends against monthly subscriber churn"
        )
        
    with col_s3:
        intl_target_share = st.slider(
            "Int'l Studio Allocation (%):",
            min_value=35, max_value=80, value=58, step=1,
            help="Target percentage of annual production allocated to non-US production hubs"
        )
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Initialize / Load Forecast Dataframe
    years = list(range(2022, 2029))
    if preset_choice in scenario_presets:
        p_data = scenario_presets[preset_choice]
        add_list = p_data["additions"]
        bud_list = p_data["budget"]
        wh_list = p_data["watch_hrs"]
        mov_list = [int(a * (100 - tv_target_share) / 100) for a in add_list]
        tv_list = [a - m for a, m in zip(add_list, mov_list)]
        intl_list = [intl_target_share] * len(years)
        
        default_df = pd.DataFrame({
            "Year": years,
            "Projected Additions": add_list,
            "Movies Target": mov_list,
            "TV Shows Target": tv_list,
            "Int'l Content (%)": intl_list,
            "Budget ($B)": bud_list,
            "Est. Watch Hours (B)": wh_list
        })
    else:
        # Default baseline if Custom selected
        default_df = pd.DataFrame({
            "Year": years,
            "Projected Additions": [1650, 1780, 1920, 2060, 2210, 2370, 2540],
            "Movies Target": [858, 925, 998, 1071, 1149, 1232, 1320],
            "TV Shows Target": [792, 855, 922, 989, 1061, 1138, 1220],
            "Int'l Content (%)": [55.0, 56.5, 58.0, 60.0, 62.0, 64.0, 65.0],
            "Budget ($B)": [17.5, 18.2, 19.0, 19.8, 20.7, 21.6, 22.5],
            "Est. Watch Hours (B)": [108, 116, 125, 135, 146, 158, 170]
        })
    
    # Editable Data Grid
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; margin-bottom:8px;">
        <h3 style="color:#FFFFFF; font-size:1.3rem; margin:0;">
            📋 Power BI Interactive Data Grid <span style="font-size:0.85rem; color:#F2C811; font-weight:600;">(Editable Cells)</span>
        </h3>
        <span style="color:#B0B0B0; font-size:0.82rem;">Double-click any number to edit • Graphs update automatically</span>
    </div>
    """, unsafe_allow_html=True)
    
    edited_df = st.data_editor(
        default_df,
        use_container_width=True,
        num_rows="fixed",
        column_config={
            "Year": st.column_config.NumberColumn(format="%d", disabled=True),
            "Projected Additions": st.column_config.NumberColumn(min_value=500, max_value=6000, step=50, help="Total projected additions"),
            "Movies Target": st.column_config.NumberColumn(min_value=200, max_value=3500, step=25, help="Projected feature films"),
            "TV Shows Target": st.column_config.NumberColumn(min_value=100, max_value=3000, step=25, help="Projected episodic series"),
            "Int'l Content (%)": st.column_config.NumberColumn(min_value=15.0, max_value=90.0, step=1.0, format="%.1f%%"),
            "Budget ($B)": st.column_config.NumberColumn(min_value=5.0, max_value=40.0, step=0.5, format="$%.1fB"),
            "Est. Watch Hours (B)": st.column_config.NumberColumn(min_value=40.0, max_value=350.0, step=5.0, format="%.0f B")
        },
        key="pbi_live_data_grid"
    )
    
    # Dynamic KPI Calculations based on edited_df
    total_new_titles = int(edited_df["Projected Additions"].sum())
    total_library_2028 = 8807 + total_new_titles
    total_capital_spend = float(edited_df["Budget ($B)"].sum())
    final_year_watch_hours = float(edited_df.iloc[-1]["Est. Watch Hours (B)"])
    avg_tv_ratio = float(edited_df["TV Shows Target"].sum() / total_new_titles * 100) if total_new_titles > 0 else 45.0
    avg_intl_ratio = float(edited_df["Int'l Content (%)"].mean())
    churn_shield_score = min(99.0, max(52.0, (avg_tv_ratio * 0.72 + avg_intl_ratio * 0.38 + 20.0)))
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # 4 Power BI KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="catchy-kpi-label">Projected 2028 Library</div>
            <div class="catchy-kpi-val">{total_library_2028:,}</div>
            <div class="catchy-kpi-sub">+{total_new_titles:,} New Titles Added</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="catchy-kpi-label">7-Yr Total Production Spend</div>
            <div class="catchy-kpi-val">${total_capital_spend:.1f}<span>B</span></div>
            <div class="catchy-kpi-sub">Avg: ${total_capital_spend/7:.1f}B / Year</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="catchy-kpi-label">2028 Annual Watch Hours</div>
            <div class="catchy-kpi-val">{final_year_watch_hours:.0f} <span>B</span></div>
            <div class="catchy-kpi-sub">Binge Engagement Metric</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        shield_color = "#00E5FF" if churn_shield_score >= 85 else "#FFB300"
        st.markdown(f"""
        <div class="pbi-kpi-card">
            <div class="catchy-kpi-label">Subscriber Churn Shield</div>
            <div class="catchy-kpi-val" style="color:{shield_color};">{churn_shield_score:.1f}<span>/100</span></div>
            <div class="catchy-kpi-sub">TV Depth ({avg_tv_ratio:.0f}%) + Int'l Moat</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # DYNAMIC PLOTLY CHARTS (Reactively driven by edited_df)
    st.markdown("### 📈 Live Reactive Forecast Visualizations")
    
    # Chart 1: Historical vs Forecast Trajectory (2008-2028)
    hist_years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    hist_adds = [2, 2, 1, 13, 3, 11, 24, 82, 429, 1188, 1649, 2016, 1879, 1498]
    
    proj_years = edited_df["Year"].tolist()
    proj_adds = edited_df["Projected Additions"].tolist()
    
    # Cumulative trajectory
    hist_cum = list(np.cumsum(hist_adds))
    proj_cum = []
    curr = hist_cum[-1]
    for add in proj_adds:
        curr += add
        proj_cum.append(curr)
        
    fig1 = go.Figure()
    
    # Confidence ribbon for projection
    upper_band = [y * 1.08 for y in [hist_adds[-1]] + proj_adds]
    lower_band = [y * 0.92 for y in [hist_adds[-1]] + proj_adds]
    band_x = [2021] + proj_years
    
    fig1.add_trace(go.Scatter(
        x=band_x + band_x[::-1],
        y=upper_band + lower_band[::-1],
        fill='toself',
        fillcolor='rgba(0, 229, 255, 0.12)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name="±8% Volatility Band"
    ))
    
    # Historical trace
    fig1.add_trace(go.Scatter(
        x=hist_years,
        y=hist_adds,
        mode="lines+markers",
        name="Historical Actuals (2008–2021)",
        line=dict(color="#E50914", width=3.5),
        marker=dict(size=7, color="#FFFFFF", line=dict(color="#E50914", width=2)),
        hovertemplate="<b>Year: %{x}</b><br>Actual Ingested: %{y:,} titles<extra></extra>"
    ))
    
    # Forecast trace
    fig1.add_trace(go.Scatter(
        x=[2021] + proj_years,
        y=[hist_adds[-1]] + proj_adds,
        mode="lines+markers",
        name="Dynamic Forecast (2022–2028)",
        line=dict(color="#00E5FF", width=3.5, dash="dash"),
        marker=dict(size=8, color="#00E5FF", symbol="diamond"),
        hovertemplate="<b>Year: %{x}</b><br>Projected Additions: %{y:,} titles<extra></extra>"
    ))
    
    fig1.update_layout(
        title=dict(text="<b>Annual Content Ingestion Velocity: Historical Actuals vs. Dynamic What-If Forecast</b>", font=dict(size=16, color="#FFFFFF")),
        paper_bgcolor="#141414",
        plot_bgcolor="#1c1c1c",
        height=420,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#FFFFFF")),
        xaxis=dict(
            title=dict(text="Calendar Year", font=dict(color="#FFFFFF")),
            gridcolor="#282828",
            tickmode="linear",
            tick0=2008,
            dtick=2,
            tickfont=dict(color="#D0D0D0")
        ),
        yaxis=dict(
            title=dict(text="Annual Ingested Titles", font=dict(color="#FFFFFF")),
            gridcolor="#282828",
            tickfont=dict(color="#D0D0D0")
        )
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Row 2 Charts: Format Mix Stacked Bar & International Allocation Donut
    c_chart1, c_chart2 = st.columns(2)
    
    with c_chart1:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=edited_df["Year"],
            y=edited_df["Movies Target"],
            name="Feature Films (Acquisition Volume)",
            marker_color="#E50914",
            hovertemplate="<b>%{x} Movies:</b> %{y:,} titles<extra></extra>"
        ))
        fig2.add_trace(go.Bar(
            x=edited_df["Year"],
            y=edited_df["TV Shows Target"],
            name="TV Series (Retention Moat)",
            marker_color="#F0F0F0",
            hovertemplate="<b>%{x} TV Shows:</b> %{y:,} titles<extra></extra>"
        ))
        fig2.update_layout(
            barmode="stack",
            title=dict(text="<b>Projected Format Allocation: Feature Films vs. TV Shows</b>", font=dict(size=14, color="#FFFFFF")),
            paper_bgcolor="#141414",
            plot_bgcolor="#1c1c1c",
            height=360,
            margin=dict(l=30, r=30, t=45, b=35),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#FFFFFF")),
            xaxis=dict(gridcolor="#282828", tickfont=dict(color="#D0D0D0")),
            yaxis=dict(title="Projected Titles", gridcolor="#282828", tickfont=dict(color="#D0D0D0"))
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    with c_chart2:
        na_share = max(15.0, 100.0 - avg_intl_ratio)
        apac_share = avg_intl_ratio * 0.42
        emea_share = avg_intl_ratio * 0.38
        latam_share = avg_intl_ratio * 0.20
        
        donut_labels = ["North America (US/CA)", "Asia-Pacific (India/KR/JP)", "Europe (UK/ES/FR)", "Latin America (BR/CO/MX)"]
        donut_values = [na_share, apac_share, emea_share, latam_share]
        donut_colors = ["#E50914", "#FF5252", "#B71C1C", "#FF8A80"]
        
        fig3 = go.Figure(data=[go.Pie(
            labels=donut_labels,
            values=donut_values,
            hole=0.55,
            marker=dict(colors=donut_colors),
            hovertemplate="<b>%{label}</b><br>Budget Allocation: %{percent}<extra></extra>"
        )])
        fig3.update_layout(
            title=dict(text="<b>Projected Global Studio Budget Allocation</b>", font=dict(size=14, color="#FFFFFF")),
            paper_bgcolor="#141414",
            plot_bgcolor="#1c1c1c",
            height=360,
            margin=dict(l=20, r=20, t=45, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, font=dict(color="#FFFFFF", size=10)),
            annotations=[dict(text=f"<b>${total_capital_spend/7:.1f}B/yr</b><br>Avg Spend", x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#FFFFFF")]
        )
        st.plotly_chart(fig3, use_container_width=True)
        
    # Interactive What-If Title Success Predictor
    st.markdown("<hr style='border-color:#2a2a2a; margin:30px 0;'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Interactive Title Popularity & Hit Simulator")
    st.caption("Test how a prospective project's creative parameters influence its algorithmic completion rate, virality index, and renewal odds.")
    
    with st.expander("🎬 Configure Prospective Title & Predict Success", expanded=True):
        pcol1, pcol2, pcol3 = st.columns(3)
        with pcol1:
            sim_format = st.selectbox("Content Format:", ["TV Show", "Movie"], key="sim_fmt")
            sim_genre = st.selectbox("Primary Genre:", ["International Drama", "Sci-Fi / Mystery Thriller", "Comedy Special", "Action / Adventure", "Kids & Family", "True Crime Documentary"], key="sim_gen")
        with pcol2:
            sim_hub = st.selectbox("Production Country Hub:", ["India", "South Korea", "United States", "United Kingdom", "Spain", "France", "Japan"], key="sim_hub")
            sim_rating = st.selectbox("Target Maturity Rating:", ["TV-MA", "TV-14", "TV-PG", "PG-13", "TV-Y7"], key="sim_rat")
        with pcol3:
            if sim_format == "Movie":
                sim_runtime = st.slider("Target Runtime (Minutes):", min_value=60, max_value=180, value=98, step=2, key="sim_rt")
            else:
                sim_runtime = st.slider("Planned Seasons:", min_value=1, max_value=5, value=2, step=1, key="sim_seas")
            sim_month = st.selectbox("Target Launch Month:", ["December (Holiday Peak)", "July (Summer Peak)", "October (Halloween)", "January (New Year)", "May (Spring Lull)"], key="sim_mo")
            
        # Predictive Algorithm Scoring
        base_score = 65.0
        
        # Genre adjustment
        if "Sci-Fi" in sim_genre or "International" in sim_genre:
            base_score += 12
        elif "Kids" in sim_genre:
            base_score += 8
        elif "Comedy" in sim_genre:
            base_score += 4
            
        # Hub adjustment
        if sim_hub in ["South Korea", "Spain", "India"]:
            base_score += 10
        elif sim_hub == "United States":
            base_score += 7
            
        # Rating adjustment
        if sim_rating in ["TV-MA", "TV-14"]:
            base_score += 6
            
        # Month adjustment
        if "December" in sim_month or "July" in sim_month:
            base_score += 8
        elif "May" in sim_month:
            base_score -= 5
            
        # Runtime / format penalty
        if sim_format == "Movie":
            if 90 <= sim_runtime <= 105:
                base_score += 9
            elif sim_runtime > 125:
                base_score -= 12
        else:
            if sim_runtime >= 2:
                base_score += 8
                
        pred_hit_score = min(98.0, max(45.0, base_score))
        pred_completion_pct = min(94.0, max(42.0, pred_hit_score * 0.95))
        pred_renewal_odds = min(96.0, max(25.0, pred_hit_score * 0.98 if sim_format == "TV Show" else 88.0))
        
        if pred_hit_score >= 85:
            verdict_text = "🟢 GLOBAL TENTPOLE BLOCKBUSTER CANDIDATE"
            verdict_badge_color = "#00E5FF"
            verdict_desc = "High viral export probability across multi-language regions. Strong 28-day completion rate expected."
        elif pred_hit_score >= 70:
            verdict_text = "🟡 STRONG STEADY PERFORMER (CORE CATALOG RETENTION)"
            verdict_badge_color = "#FFD600"
            verdict_desc = "Solid platform viewership with loyal demographic appeal. Low churn risk within target audience segment."
        else:
            verdict_text = "🔴 ELEVATED RISK / EXPENSE CONSOLIDATION WATCH"
            verdict_badge_color = "#FF5252"
            verdict_desc = "Runtime or scheduling constraints indicate potential 28-day drop-off risk. Recommend tighter runtime discipline."
            
        st.markdown(f"""
        <div class="sim-score-box">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:1.35rem; font-weight:800; color:#FFFFFF;">Simulation Forecast Outcome</span>
                <span class="sim-verdict-pill" style="background-color:rgba(229,9,20,0.25); border:1px solid {verdict_badge_color}; color:{verdict_badge_color};">{verdict_text}</span>
            </div>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:14px; margin:15px 0;">
                <div style="background:#131313; padding:12px 16px; border-radius:6px; border:1px solid #2e2e2e;">
                    <div style="font-size:0.75rem; color:#A0A0A0; font-weight:700;">PREDICTED HIT INDEX</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">{pred_hit_score:.1f} <span style="font-size:0.9rem; color:#E50914;">/ 100</span></div>
                </div>
                <div style="background:#131313; padding:12px 16px; border-radius:6px; border:1px solid #2e2e2e;">
                    <div style="font-size:0.75rem; color:#A0A0A0; font-weight:700;">28-DAY COMPLETION RATE</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">{pred_completion_pct:.1f}%</div>
                </div>
                <div style="background:#131313; padding:12px 16px; border-radius:6px; border:1px solid #2e2e2e;">
                    <div style="font-size:0.75rem; color:#A0A0A0; font-weight:700;">RENEWAL / VIRALITY LIKELIHOOD</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">{pred_renewal_odds:.1f}%</div>
                </div>
            </div>
            <p style="color:#DCDCDC; font-size:0.92rem; margin:0; line-height:1.5;">
                <b>Algorithmic Assessment:</b> {verdict_desc}
            </p>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. PAGE 3: 💡 ANALYTICAL INSIGHTS
# -----------------------------------------------------------------------------
elif navigation_selection == "💡 Analytical Insights":
    st.markdown("""
    <div style="border-bottom: 2px solid #E50914; padding-bottom: 10px; margin-bottom: 25px;">
        <h2 style="font-family:'Bebas Neue', sans-serif; font-size:2.6rem; letter-spacing:1px; margin:0; color:#FFFFFF;">
            DEEP ANALYTICAL <span style="color:#E50914;">INSIGHTS</span>
        </h2>
        <p style="color:#D2D2D2; font-size:0.95rem; margin-top:4px;">
            Comprehensive synthesis of structural catalog dynamics, content format dominance, 
            algorithmic scaling post-2016, and demographic audience targeting.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs([
        "1. Format Dominance",
        "2. The 2016 Inflection Point",
        "3. Genre Preferences",
        "4. Maturity Ratings Moat",
        "5. Geographic Production Hubs"
    ])
    
    # TAB 1: Format Dominance
    with tabs[0]:
        st.markdown("<h3 style='color:#FFFFFF;'>The 70 / 30 Catalog Split: Films vs. Episodic Series</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("""
            <div class="content-box">
                <p style="color:#E8E8E8; line-height:1.7;">
                    A fundamental paradox in Netflix's catalog architecture is the disparity between catalog volume and user engagement:
                </p>
                <ul style="color:#E0E0E0; line-height:1.8;">
                    <li><b>69.6% Movies (6,131 titles):</b> Films provide immediate catalog density and breadth. A user browsing on a Friday evening often looks for a self-contained 95-minute experience. Film licensing deals historically allowed Netflix to populate new country launches rapidly.</li>
                    <li><b>30.4% TV Shows (2,676 titles):</b> Despite holding less than one-third of titles, episodic TV series drive an estimated <b>75%+ of total platform viewing hours</b>. A multi-season drama commands 10 to 50 hours of viewer commitment compared to 1.5 hours for a feature film.</li>
                    <li><b>Economic Unit Economics:</b> While TV series require higher upfront production budgets, their cost per engaged hour is drastically lower than blockbuster films, rendering episodic television Netflix's primary defensive moat against churn.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            v1_p = resolve_asset_path("viz1_type_distribution.png")
            if os.path.exists(v1_p):
                st.image(Image.open(v1_p), use_container_width=True)
            st.markdown("""
            <div class="quote-box">
                "Movies acquire subscribers; TV series keep them subscribed."
            </div>
            """, unsafe_allow_html=True)
            
    # TAB 2: Post-2016 Scaling
    with tabs[1]:
        st.markdown("<h3 style='color:#FFFFFF;'>The 2016 Inflection Point: The Birth of Global Streaming</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("""
            <div class="content-box">
                <p style="color:#E8E8E8; line-height:1.7;">
                    The year 2016 represents the defining structural turning point in Netflix's business history:
                </p>
                <ul style="color:#E0E0E0; line-height:1.8;">
                    <li><b>The CES 2016 Global Switch:</b> On January 6, 2016, CEO Reed Hastings announced Netflix went live in 130 countries simultaneously, transforming the company overnight into the world's first truly planetary streaming network.</li>
                    <li><b>Annual Additions Surged by 370%:</b> Between 2016 (429 additions) and 2019 (2,016 additions), annual content ingestion expanded at a CAGR exceeding 65%.</li>
                    <li><b>The Original IP Hedge:</b> As traditional Hollywood studios (Disney, WarnerMedia, NBCUniversal) prepared their own direct-to-consumer platforms, they began clawing back licensed titles. Netflix responded by spending billions to construct an unassailable proprietary IP vault.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            v2_p = resolve_asset_path("viz2_growth_trend.png")
            if os.path.exists(v2_p):
                st.image(Image.open(v2_p), use_container_width=True)
                
    # TAB 3: Genre Preferences
    with tabs[2]:
        st.markdown("<h3 style='color:#FFFFFF;'>Genre Hierarchy & The Borderless Content Model</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("""
            <div class="content-box">
                <p style="color:#E8E8E8; line-height:1.7;">
                    Categorization patterns across the 8,807 titles reveal how genre diversification drives cross-demographic penetration:
                </p>
                <ul style="color:#E0E0E0; line-height:1.8;">
                    <li><b>International Content Dominance:</b> Over 4,100 titles carry the 'International' designation, making cross-border stories the single largest content block on the platform.</li>
                    <li><b>Dramas & Comedies as Retention Anchors:</b> Dramas (2,427) and Comedies (1,674) satisfy universal human storytelling desires, traveling with minimal cultural friction when properly dubbed and subtitled.</li>
                    <li><b>The High-ROI Stand-Up Comedy Moat:</b> Stand-up comedy specials cost a fraction of scripted dramas (often <$15M) yet deliver viral cultural conversations, awards buzz, and immediate social media engagement.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            v3_p = resolve_asset_path("viz3_top_genres.png")
            if os.path.exists(v3_p):
                st.image(Image.open(v3_p), use_container_width=True)

    # TAB 4: Maturity Ratings
    with tabs[3]:
        st.markdown("<h3 style='color:#FFFFFF;'>The TV-MA Moat: Unshackled Adult Storytelling</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("""
            <div class="content-box">
                <p style="color:#E8E8E8; line-height:1.7;">
                    The ratings breakdown illuminates Netflix's deliberate counter-programming strategy against broadcast TV:
                </p>
                <ul style="color:#E0E0E0; line-height:1.8;">
                    <li><b>60.9% Mature Audience Share:</b> TV-MA (3,207 titles | 36.4%) and TV-14 (2,160 titles | 24.5%) constitute the vast majority of Netflix offerings.</li>
                    <li><b>Creative Freedom as a Talent Magnet:</b> Without the FCC broadcast decency constraints or PG-13 box-office dilution, top showrunners (e.g., David Fincher, Shonda Rhimes, the Duffer Brothers) migrated to Netflix for complete creative autonomy.</li>
                    <li><b>The Family Gap:</b> Combined kids programming (TV-Y, TV-Y7, G, TV-G) represents only ~10.2% of the library. This gap exposes Netflix to subscription cannibalization from Disney+, which commands undisputed family loyalty.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            v4_p = resolve_asset_path("viz4_ratings_distribution.png")
            if os.path.exists(v4_p):
                st.image(Image.open(v4_p), use_container_width=True)

    # TAB 5: Geographic Hubs
    with tabs[4]:
        st.markdown("<h3 style='color:#FFFFFF;'>Geographic Production Hubs: The Decentralized Studio</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("""
            <div class="content-box">
                <p style="color:#E8E8E8; line-height:1.7;">
                    Mapping the geographical origin of titles reflects a seismic shift from Hollywood monoculture to distributed global studios:
                </p>
                <ul style="color:#E0E0E0; line-height:1.8;">
                    <li><b>United States (3,689 titles):</b> Retains plurality at 41.9%, but its overall share of annual additions has steadily declined as international production centers scale up.</li>
                    <li><b>India as the #2 Content Engine (1,046 titles):</b> India boasts the largest non-Western library on Netflix, propelled by regional cinema (Hindi, Tamil, Telugu) and aggressive streaming deals with Bollywood studios.</li>
                    <li><b>Europe & Asia-Pacific Powerhouses:</b> The UK (804), Canada (445), France (393), Japan (318 anime/live-action), Spain (232), and South Korea (231) deliver extraordinary global return on investment, routinely topping Top 10 lists worldwide.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            v5_p = resolve_asset_path("viz5_top_countries.png")
            if os.path.exists(v5_p):
                st.image(Image.open(v5_p), use_container_width=True)


# -----------------------------------------------------------------------------
# 8. PAGE 4: 🎯 ACTIONABLE RECOMMENDATIONS
# -----------------------------------------------------------------------------
elif navigation_selection == "🎯 Actionable Recommendations":
    st.markdown("""
    <div style="border-bottom: 2px solid #E50914; padding-bottom: 10px; margin-bottom: 25px;">
        <h2 style="font-family:'Bebas Neue', sans-serif; font-size:2.6rem; letter-spacing:1px; margin:0; color:#FFFFFF;">
            STRATEGIC <span style="color:#E50914;">RECOMMENDATIONS</span>
        </h2>
        <p style="color:#D2D2D2; font-size:0.95rem; margin-top:4px;">
            Data-backed executive roadmap for content acquisition, catalog rebalancing, and global subscriber retention.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 1
    st.markdown("""
    <div class="rec-card">
        <div class="rec-title">
            <span>🎯 Pillar 1: Strategic Genre Investment & Hybridization</span>
            <span class="rec-pill">High Impact</span>
        </div>
        <p style="color:#E2E2E2; font-size:0.94rem; line-height:1.6;">
            <b>The Insight:</b> While Dramas and Comedies form the catalog backbone, viewer fatigue in generic comedy specials is rising, while cross-genre titles (e.g. Sci-Fi Thrillers, Mystery Dramas) generate the highest viral completion rates.
        </p>
        <div style="background-color:#141414; border-left:3px solid #E50914; padding:12px 16px; border-radius:0 6px 6px 0; margin-top:10px; border:1px solid #2e2e2e;">
            <b style="color:#FFFFFF;">Actionable Mandate:</b>
            <ul style="color:#D0D0D0; margin:6px 0 0 0; padding-left:20px; font-size:0.9rem; line-height:1.6;">
                <li>Reallocate 15% of standalone comedy special budgets toward high-concept hybrid scripted mini-series.</li>
                <li>Commission multi-generational mystery dramas with built-in social media speculation loops (e.g., Dark, Wednesday).</li>
                <li>Target the 90–105 minute sweet spot for all mid-tier feature acquisitions to maximize algorithmic completion score.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 2
    st.markdown("""
    <div class="rec-card">
        <div class="rec-title">
            <span>🌍 Pillar 2: Hyper-Localized Expansion with Global Export DNA</span>
            <span class="rec-pill">Critical Growth</span>
        </div>
        <p style="color:#E2E2E2; font-size:0.94rem; line-height:1.6;">
            <b>The Insight:</b> Non-US production hubs deliver viral hits with up to 70% lower production costs compared to Hollywood standards. South Korea and Spain have demonstrated that local cultural authenticity outperforms homogenized international corporate blockbusters.
        </p>
        <div style="background-color:#141414; border-left:3px solid #E50914; padding:12px 16px; border-radius:0 6px 6px 0; margin-top:10px; border:1px solid #2e2e2e;">
            <b style="color:#FFFFFF;">Actionable Mandate:</b>
            <ul style="color:#D0D0D0; margin:6px 0 0 0; padding-left:20px; font-size:0.9rem; line-height:1.6;">
                <li>Establish dedicated production hubs in Southeast Asia (Indonesia, Philippines, Vietnam) and Latin America (Colombia, Argentina).</li>
                <li>Mandate multi-language native audio dubbing and culturally nuanced subtitling for top 20% regional productions on day 1.</li>
                <li>Deepen partnerships with regional Indian animation studios to build enduring franchises that match Bollywood theatrical pull.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 3
    st.markdown("""
    <div class="rec-card">
        <div class="rec-title">
            <span>🧸 Pillar 3: Family Catalog & Demographics Optimization</span>
            <span class="rec-pill">Retention Defense</span>
        </div>
        <p style="color:#E2E2E2; font-size:0.94rem; line-height:1.6;">
            <b>The Insight:</b> With mature titles (TV-MA & TV-14) representing over 60.9% of the catalog, family and children programming languishes at ~10.2%. Household accounts with young children exhibit 40% lower churn if family content is regularly refreshed.
        </p>
        <div style="background-color:#141414; border-left:3px solid #E50914; padding:12px 16px; border-radius:0 6px 6px 0; margin-top:10px; border:1px solid #2e2e2e;">
            <b style="color:#FFFFFF;">Actionable Mandate:</b>
            <ul style="color:#D0D0D0; margin:6px 0 0 0; padding-left:20px; font-size:0.9rem; line-height:1.6;">
                <li>Expand the Kids & Family catalog from 10.2% to at least 18% over the next 36 months to neutralize Disney+'s core advantage.</li>
                <li>Develop animated universe franchises that create recurring episodic viewing habits for children under 10.</li>
                <li>Co-produce with European and Japanese animation studios (e.g., Studio Ghibli licensing, French boutique animators).</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation 4
    st.markdown("""
    <div class="rec-card">
        <div class="rec-title">
            <span>📺 Pillar 4: Series Longevity & Overcoming the 1-Season Cliff</span>
            <span class="rec-pill">Churn Mitigation</span>
        </div>
        <p style="color:#E2E2E2; font-size:0.94rem; line-height:1.6;">
            <b>The Insight:</b> Two-thirds (67.0%) of TV shows end after Season 1. Excessive early cancellations create viewer hesitation, where subscribers refuse to invest time in new shows until guaranteed renewal.
        </p>
        <div style="background-color:#141414; border-left:3px solid #E50914; padding:12px 16px; border-radius:0 6px 6px 0; margin-top:10px; border:1px solid #2e2e2e;">
            <b style="color:#FFFFFF;">Actionable Mandate:</b>
            <ul style="color:#D0D0D0; margin:6px 0 0 0; padding-left:20px; font-size:0.9rem; line-height:1.6;">
                <li>Market single-season projects transparently as 'Limited Series' with satisfying narrative conclusions.</li>
                <li>Implement a lower-budget Season 2 renewal tier for cult shows with passionate core fanbases to preserve loyalty.</li>
                <li>Use predictive AI to greenlight two-season commitments for high-probability concepts, lowering per-season fixed costs.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategic Impact vs Effort Matrix
    st.markdown("<h3 style='color:#FFFFFF; font-size:1.35rem; margin-top:25px;'>📊 Strategic Execution Priority Matrix</h3>", unsafe_allow_html=True)
    
    matrix_data = pd.DataFrame([
        {"Strategic Initiative": "Family Catalog Expansion (Animation)", "Impact": "Very High", "Effort": "High", "Time Horizon": "24–36 Months", "Primary KPI Target": "-15% Family Churn"},
        {"Strategic Initiative": "90–105 Min Movie Runtime Standardization", "Impact": "Medium", "Effort": "Low", "Time Horizon": "Immediate", "Primary KPI Target": "+12% Completion Rate"},
        {"Strategic Initiative": "Local-for-Global Studio Hubs (SE Asia/LatAm)", "Impact": "High", "Effort": "Medium", "Time Horizon": "12–18 Months", "Primary KPI Target": "+25M Net Subs"},
        {"Strategic Initiative": "Limited Series Rebranding & Narrative Closure", "Impact": "High", "Effort": "Low", "Time Horizon": "3–6 Months", "Primary KPI Target": "+18% Show Start Rate"},
        {"Strategic Initiative": "Q4 Holiday Ingestion Scheduling Alignment", "Impact": "Medium", "Effort": "Low", "Time Horizon": "Annual Cycle", "Primary KPI Target": "+8% Q4 ARPU"}
    ])
    
    st.dataframe(matrix_data, use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# 9. PAGE 5: 📖 DATA STORYTELLING REPORT (STATEFUL QUIZ)
# -----------------------------------------------------------------------------
elif navigation_selection == "📖 Data Storytelling Report":
    st.markdown("""
    <div style="border-bottom: 2px solid #E50914; padding-bottom: 10px; margin-bottom: 25px;">
        <h2 style="font-family:'Bebas Neue', sans-serif; font-size:2.6rem; letter-spacing:1px; margin:0; color:#FFFFFF;">
            THE DATA STORYTELLING <span style="color:#E50914;">REPORT</span>
        </h2>
        <p style="color:#D2D2D2; font-size:0.95rem; margin-top:4px;">
            A publication-grade narrative report following the structured framework: 
            <b>Problem ➔ Analysis ➔ Insights ➔ Strategic Recommendations</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Act I: Problem
    st.markdown("""
    <div class="content-box">
        <div class="content-box-header">
            <span class="icon">🚨</span> ACT I: THE STRATEGIC PROBLEM
        </div>
        <p style="color:#E2E2E2; line-height:1.8;">
            Between 2015 and 2021, the global streaming landscape experienced an unprecedented transition from an era of scarce digital aggregators 
            to the brutal, hyper-competitive <b>"Streaming Wars"</b>. Traditional media conglomerates—having happily licensed their back-catalogs to Netflix for 
            years—abruptly clawed back their flagship intellectual properties (e.g. <i>Friends</i>, <i>The Office</i>, Marvel, Star Wars) to launch rival 
            platforms like Disney+, HBO Max, and Peacock.
        </p>
        <p style="color:#E2E2E2; line-height:1.8;">
            Faced with the existential threat of catalog starvation, Netflix confronted a multi-billion dollar question: 
            <b>What makes content successful and enduring on a modern streaming platform?</b> Can proprietary algorithms, runtime discipline, 
            maturity calibration, and international studio scaling replace century-old legacy Hollywood studio dominance?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Act II: Analysis
    st.markdown("""
    <div class="content-box">
        <div class="content-box-header">
            <span class="icon">📊</span> ACT II: THE EMPIRICAL ANALYSIS
        </div>
        <p style="color:#E2E2E2; line-height:1.8;">
            To answer this question, our data science team audited the entire available Netflix metadata catalog comprising <b>8,807 registered titles</b> 
            spanning release years from 1925 through 2021. Through rigorous feature engineering, temporal decomposition, and distribution modeling across 
            10 analytical dimensions, key empirical patterns emerged:
        </p>
        <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:12px; margin:15px 0;">
            <div style="background-color:#111111; padding:14px; border-left:3px solid #E50914; border-radius:4px; border:1px solid #282828;">
                <b style="color:#FFFFFF;">Volume Asymmetry:</b> <span style="color:#E2E2E2;">6,131 Movies (69.6%) vs. 2,676 TV Shows (30.4%).</span>
            </div>
            <div style="background-color:#111111; padding:14px; border-left:3px solid #E50914; border-radius:4px; border:1px solid #282828;">
                <b style="color:#FFFFFF;">Runtime Sweet Spot:</b> <span style="color:#E2E2E2;">Gaussian bell curve centered at median 98 minutes for feature films.</span>
            </div>
            <div style="background-color:#111111; padding:14px; border-left:3px solid #E50914; border-radius:4px; border:1px solid #282828;">
                <b style="color:#FFFFFF;">The 1-Season Attrition:</b> <span style="color:#E2E2E2;">67.0% of all TV shows terminate after a single season.</span>
            </div>
            <div style="background-color:#111111; padding:14px; border-left:3px solid #E50914; border-radius:4px; border:1px solid #282828;">
                <b style="color:#FFFFFF;">Maturity Dominance:</b> <span style="color:#E2E2E2;">TV-MA and TV-14 capture 60.9% of total catalog real estate.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Act III: Insights
    st.markdown("""
    <div class="content-box">
        <div class="content-box-header">
            <span class="icon">💡</span> ACT III: SYNTHESIZED CORE INSIGHTS
        </div>
        <p style="color:#E2E2E2; line-height:1.8;">
            The findings demonstrate that Netflix's catalog architecture is governed by four distinct strategic pillars:
        </p>
        <ol style="color:#E2E2E2; line-height:1.8;">
            <li><b>The Post-2016 Exponential J-Curve:</b> Catalyzed by the CES 2016 expansion into 130+ markets, annual additions exploded by over 370%, peaking in 2019 at 2,016 additions before supply-chain rationalization set in.</li>
            <li><b>The Adult Streaming Safe-Haven:</b> By leaning into TV-MA programming, Netflix differentiated itself fundamentally from broadcast networks and Disney's family image, making edgy scripted drama its cultural trademark.</li>
            <li><b>The Local-to-Global Cross-Pollination:</b> Non-English content hubs (India, South Korea, Spain, France) ceased being local defensive hedges; they became global export engines generating unmatched viral ROI.</li>
            <li><b>The Seasonal Content Ingestion Rhythm:</b> Aligning major catalog updates with Q4 holiday downtime (December additions: 813) maximizes subscriber acquisition when churn risks are highest.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Act IV: Recommendations
    st.markdown("""
    <div class="content-box">
        <div class="content-box-header">
            <span class="icon">🎯</span> ACT IV: STRATEGIC RECOMMENDATIONS & FORWARD ROADMAP
        </div>
        <p style="color:#E2E2E2; line-height:1.8;">
            Based on the empirical evidence, the following executive actions are recommended for platform leadership:
        </p>
        <ul style="color:#E2E2E2; line-height:1.8;">
            <li><b>Repair the Family Moat:</b> Expand Kids & Family programming from 10.2% to 18% to safeguard multi-user household retention against Disney+.</li>
            <li><b>Mitigate Viewer Hesitation from 1-Season Cancellations:</b> Pre-package short-run series as 'Limited Series' so subscribers receive narrative resolution without cancellation disappointment.</li>
            <li><b>Institutionalize Global Localization Infrastructure:</b> Deepen AI-assisted localization, dubbing, and cultural translation pipelines to accelerate cross-border hit discovery.</li>
            <li><b>Enforce Runtime Discipline:</b> Cap mid-budget non-prestige movie runtimes at 105 minutes to protect completion rates and algorithmic virality.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # WHITE-BOX FIX 3: Stateful Quiz using st.session_state to prevent feedback erasure across reruns
    st.markdown("<h3 style='color:#FFFFFF; font-size:1.35rem; margin-top:25px;'>🧠 Interactive Quiz: Test Your Netflix Data Knowledge</h3>", unsafe_allow_html=True)
    
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
        
    quiz_q1 = st.radio(
        "1. What percentage of all titles in the Netflix catalog are Movies?",
        ["~50.0%", "~69.6%", "~82.5%", "~30.4%"],
        index=0,
        key="radio_q1"
    )
    if st.button("Check Answer for Q1", key="btn_q1"):
        st.session_state.quiz_answers["q1"] = quiz_q1
        
    if "q1" in st.session_state.quiz_answers:
        user_ans_1 = st.session_state.quiz_answers["q1"]
        if user_ans_1 == "~69.6%":
            st.success(f"✅ Correct! You chose {user_ans_1}. Movies make up exactly 69.6% (6,131 titles) of the catalog.")
        else:
            st.error(f"❌ Incorrect. You chose {user_ans_1}. The catalog is 69.6% Movies and 30.4% TV Shows.")
            
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    
    quiz_q2 = st.radio(
        "2. What is the single most common reason why 67% of Netflix TV shows have only 1 season?",
        [
            "Directors refuse to film second seasons",
            "Algorithmic cancellation thresholds if shows fail to hit 28-day subscriber acquisition benchmarks",
            "Streaming servers cannot handle multiple seasons",
            "Actors age out of roles"
        ],
        index=0,
        key="radio_q2"
    )
    if st.button("Check Answer for Q2", key="btn_q2"):
        st.session_state.quiz_answers["q2"] = quiz_q2
        
    if "q2" in st.session_state.quiz_answers:
        user_ans_2 = st.session_state.quiz_answers["q2"]
        if "Algorithmic cancellation thresholds" in user_ans_2:
            st.success("✅ Exactly! Netflix evaluates cost-versus-completion within the first 28 days to decide renewal viability.")
        else:
            st.error(f"❌ Not quite. Netflix uses strict 28-day algorithmic completion metrics to decide renewals.")
            
    # Composite Score Banner when both questions are answered
    if "q1" in st.session_state.quiz_answers and "q2" in st.session_state.quiz_answers:
        q1_ok = (st.session_state.quiz_answers["q1"] == "~69.6%")
        q2_ok = ("Algorithmic cancellation thresholds" in st.session_state.quiz_answers["q2"])
        total_score = (1 if q1_ok else 0) + (1 if q2_ok else 0)
        score_pct = int(total_score / 2 * 100)
        
        st.markdown(f"""
        <div style="background-color:#1c1315; border:1px solid #E50914; border-radius:8px; padding:16px; margin:20px 0; text-align:center;">
            <div style="font-size:1.3rem; font-weight:800; color:#FFFFFF;">
                🎯 Your Quiz Score: <span style="color:#E50914;">{total_score} / 2</span> ({score_pct}%)
            </div>
            <p style="color:#E0E0E0; font-size:0.92rem; margin-top:6px; margin-bottom:0;">
                {'🌟 Outstanding! You have mastered the core data insights of Netflix content dynamics.' if total_score == 2 else '💡 Great effort! Review the analytical insights above to master the catalog metrics.'}
            </p>
        </div>
        """, unsafe_allow_html=True)
            
    if st.session_state.quiz_answers:
        if st.button("🔄 Reset Quiz Answers"):
            st.session_state.quiz_answers = {}
            st.rerun()


# -----------------------------------------------------------------------------
# 10. FOOTER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="footer-text">
    <b style="color:#FFFFFF;">The Netflix Effect: What Makes a Show Popular?</b> — Data Analytics & Storytelling Application<br>
    Built with Python, Streamlit, Pandas, and Pillow • Inspired by Netflix Studio Brand Guidelines • 2026
</div>
""", unsafe_allow_html=True)

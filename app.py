# app.py  –  Apni Sehat v1.2
# Complete rewrite: wizard onboarding, profile card, 4-tab layout, Urdu support.

import os
import re
import hashlib
from datetime import datetime, date
from typing import List, Optional

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config import APP, CARB, TRIAGE
from triage import triage_profile
from planner import generate_week_plan
from llm import generate_swaps, coach_on_actual_meal, chat_with_assistant
from translations import T, get_tip

st.set_page_config(
    page_title="Apni Sehat — اپنی صحت",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Secrets ───────────────────────────────────────────────────────────────────
def _sget(k, d=""):
    try:
        return str(st.secrets.get(k, d)).strip()
    except Exception:
        return d

os.environ["GROQ_API_KEY"]  = _sget("GROQ_API_KEY",  os.getenv("GROQ_API_KEY",  ""))
os.environ["GROQ_BASE_URL"] = _sget("GROQ_BASE_URL", os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"))
os.environ["GROQ_MODEL"]    = _sget("GROQ_MODEL",    os.getenv("GROQ_MODEL",    "llama-3.3-70b-versatile"))
os.environ["DATABASE_URL"]  = _sget("DATABASE_URL",  os.getenv("DATABASE_URL",  ""))
os.environ["PHONE_SALT"]    = _sget("PHONE_SALT",    os.getenv("PHONE_SALT",    "dev-salt-change-me"))

from storage import (
    init_db, get_profile, upsert_profile,
    add_glucose_log, fetch_glucose_logs,
    add_daily_checkin, fetch_checkins,
)
init_db()

# ═══════════════════════════════════════════════════════════════════════════════
# CSS — Warm Clinic Theme
# Designed for elderly / low-literacy users in Pakistan.
# • Forced light mode — overrides any dark system preference
# • Noto fonts — beautiful Urdu rendering + warm Latin pairing
# • Very large base font (18px) — easy to read on mobile and desktop
# • High contrast — dark ink on warm cream / white
# • Generous tap targets — 52px+ button height
# • Warm forest green (#1A5C36) + golden amber (#D4861A) accent
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Fonts: Noto Serif for headings, Noto Sans for body, Noto Nastaliq for Urdu ── */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif:wght@600;700&family=Noto+Sans:wght@400;500;600;700&family=Noto+Nastaliq+Urdu:wght@400;600;700&display=swap');

/* ════════════════════════════════════
   FORCE LIGHT MODE — every dark surface
   ════════════════════════════════════ */
:root {
    color-scheme: light !important;
}
*, *::before, *::after {
    color-scheme: light !important;
}
html, body {
    background-color: #FAFAF7 !important;
    color: #1A1A1A !important;
    font-family: 'Noto Sans', sans-serif !important;
    font-size: 18px !important;
}
/* All Streamlit wrappers */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="block-container"],
.main, .main > div,
section.main, section.main > div,
div.block-container {
    background-color: #FAFAF7 !important;
    color: #1A1A1A !important;
}

/* ════════════════════════════════════
   TYPOGRAPHY
   ════════════════════════════════════ */
p, li, span, div, label,
.stMarkdown p, .stMarkdown li {
    font-family: 'Noto Sans', sans-serif !important;
    font-size: 1.1rem !important;
    line-height: 1.9 !important;
    color: #1A1A1A !important;
}
/* Urdu text — use Nastaliq where applied */
.urdu-text, [lang="ur"] {
    font-family: 'Noto Nastaliq Urdu', serif !important;
    direction: rtl !important;
    line-height: 2.2 !important;
}
h1 {
    font-family: 'Noto Serif', serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #1A5C36 !important;
    letter-spacing: -0.5px !important;
    line-height: 1.3 !important;
}
h2 {
    font-family: 'Noto Serif', serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #1A5C36 !important;
    line-height: 1.4 !important;
}
h3 {
    font-family: 'Noto Sans', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: #1A1A1A !important;
}
/* Caption / small text — still readable */
.stCaption, [data-testid="stCaptionContainer"] p, small, caption {
    font-size: 0.92rem !important;
    color: #5A5A5A !important;
    font-family: 'Noto Sans', sans-serif !important;
}

/* ════════════════════════════════════
   SIDEBAR
   ════════════════════════════════════ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background-color: #EEF7F1 !important;
    border-right: 2px solid #B8DDCA !important;
}
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #1A1A1A !important;
    font-family: 'Noto Sans', sans-serif !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1A5C36 !important;
    font-family: 'Noto Serif', serif !important;
}

/* ════════════════════════════════════
   BUTTONS
   ════════════════════════════════════ */
/* Primary — forest green */
.stButton > button[kind="primary"],
button[kind="primary"] {
    background: #1A5C36 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    font-family: 'Noto Sans', sans-serif !important;
    padding: 0.85rem 2rem !important;
    min-height: 52px !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(26,92,54,0.30) !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    background: #23784A !important;
    box-shadow: 0 6px 20px rgba(26,92,54,0.40) !important;
    transform: translateY(-1px) !important;
}
/* Secondary — outlined */
.stButton > button {
    background: #FFFFFF !important;
    color: #1A5C36 !important;
    border: 2px solid #1A5C36 !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    font-family: 'Noto Sans', sans-serif !important;
    min-height: 46px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #EEF7F1 !important;
}

/* ════════════════════════════════════
   FORM INPUTS
   ════════════════════════════════════ */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 2px solid #B8DDCA !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    font-family: 'Noto Sans', sans-serif !important;
    padding: 0.65rem 1rem !important;
    min-height: 50px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #1A5C36 !important;
    box-shadow: 0 0 0 3px rgba(26,92,54,0.15) !important;
}
[data-baseweb="input"] { background-color: #FFFFFF !important; }

/* Select boxes */
[data-baseweb="select"] > div,
[data-baseweb="select"] div[aria-selected] {
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 2px solid #B8DDCA !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
}
/* Dropdown menu */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
    border: 1px solid #B8DDCA !important;
}
[data-baseweb="menu"] li,
[data-baseweb="popover"] li {
    color: #1A1A1A !important;
    font-size: 1.05rem !important;
}

/* Radio buttons */
.stRadio > label { color: #1A1A1A !important; font-size: 1.05rem !important; }
.stRadio div[role="radiogroup"] label { color: #1A1A1A !important; }

/* Checkboxes */
.stCheckbox label, .stCheckbox span,
[data-testid="stCheckbox"] label {
    color: #1A1A1A !important;
    font-size: 1.05rem !important;
}

/* Toggle */
.stToggle label p, .stToggle span { color: #1A1A1A !important; }

/* Date / time pickers */
[data-baseweb="datepicker"] input,
input[type="date"], input[type="time"] {
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 2px solid #B8DDCA !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
}

/* Input labels */
[data-testid="stFormLabel"] p,
.stTextInput label, .stNumberInput label,
.stTextArea label, .stSelectbox label,
.stDateInput label, .stTimeInput label,
.stRadio label, .stMultiSelect label {
    color: #1A1A1A !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

/* ════════════════════════════════════
   TABS
   ════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF !important;
    border-bottom: 2px solid #B8DDCA !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-size: 1rem !important;
    font-weight: 600 !important;
    font-family: 'Noto Sans', sans-serif !important;
    padding: 14px 20px !important;
    color: #5A5A5A !important;
    background: transparent !important;
    border-bottom: 3px solid transparent !important;
    min-height: 52px !important;
}
.stTabs [aria-selected="true"] {
    color: #1A5C36 !important;
    border-bottom: 3px solid #1A5C36 !important;
    font-weight: 700 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #FAFAF7 !important;
    padding-top: 24px !important;
}

/* ════════════════════════════════════
   EXPANDERS
   ════════════════════════════════════ */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 2px solid #B8DDCA !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
.streamlit-expanderHeader p {
    color: #1A5C36 !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    font-family: 'Noto Sans', sans-serif !important;
}
[data-testid="stExpander"] summary:hover { background: #EEF7F1 !important; }
[data-testid="stExpander"] > div > div {
    background: #FFFFFF !important;
    color: #1A1A1A !important;
}

/* ════════════════════════════════════
   METRICS
   ════════════════════════════════════ */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 2px solid #B8DDCA !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
}
[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #1A5C36 !important;
    font-family: 'Noto Serif', serif !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.95rem !important;
    color: #5A5A5A !important;
    font-weight: 600 !important;
}
[data-testid="stMetricDelta"] { color: #5A5A5A !important; }

/* ════════════════════════════════════
   ALERT BOXES
   ════════════════════════════════════ */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 1.05rem !important;
    font-family: 'Noto Sans', sans-serif !important;
}
[data-testid="stAlert"][data-baseweb="notification"][kind="info"],
div[data-testid="stInfo"] {
    background-color: #E3F0FF !important;
    color: #0D3B66 !important;
    border-left: 5px solid #3B82F6 !important;
}
div[data-testid="stSuccess"], .stSuccess {
    background-color: #E8F5EE !important;
    color: #1A5C36 !important;
    border-left: 5px solid #1A5C36 !important;
}
div[data-testid="stWarning"], .stWarning {
    background-color: #FFF6E6 !important;
    color: #92400E !important;
    border-left: 5px solid #D4861A !important;
}
div[data-testid="stError"], .stError {
    background-color: #FFF0F0 !important;
    color: #991B1B !important;
    border-left: 5px solid #DC2626 !important;
}
/* Force text inside alerts to be visible */
div[data-testid="stSuccess"] *,
div[data-testid="stWarning"] *,
div[data-testid="stError"] *,
div[data-testid="stInfo"] * {
    color: inherit !important;
}

/* ════════════════════════════════════
   DATAFRAME / TABLE
   ════════════════════════════════════ */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] table,
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] td {
    background-color: #FFFFFF !important;
    color: #1A1A1A !important;
}

/* ════════════════════════════════════
   DIVIDER
   ════════════════════════════════════ */
hr { border-color: #C8E2D0 !important; margin: 20px 0 !important; }

/* ════════════════════════════════════
   CUSTOM COMPONENTS
   ════════════════════════════════════ */

/* ── Tip banner ── */
.tip-banner {
    background: linear-gradient(135deg, #1A5C36 0%, #23784A 100%);
    color: #FFFFFF !important;
    border-radius: 18px;
    padding: 22px 28px;
    margin-bottom: 24px;
    font-size: 1.1rem;
    line-height: 1.9;
    box-shadow: 0 6px 24px rgba(26,92,54,0.25);
}
.tip-banner * { color: #FFFFFF !important; }
.tip-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: 8px;
    font-family: 'Noto Sans', sans-serif !important;
}

/* ── Profile card ── */
.profile-card {
    background: #FFFFFF !important;
    border: 2px solid #B8DDCA !important;
    border-left: 6px solid #1A5C36 !important;
    border-radius: 16px;
    padding: 20px 26px;
    margin-bottom: 22px;
    box-shadow: 0 2px 12px rgba(26,92,54,0.08);
}
.profile-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: #1A5C36 !important;
    font-family: 'Noto Serif', serif !important;
}
.profile-detail {
    font-size: 1.05rem;
    color: #3A3A3A !important;
    margin-top: 6px;
    font-family: 'Noto Sans', sans-serif !important;
}

/* ── Status badges ── */
.badge-g {
    background: #D1FAE5; color: #065F46 !important;
    border: 1.5px solid #6EE7B7;
    border-radius: 8px; padding: 5px 16px;
    font-weight: 700; font-size: 0.95rem; display: inline-block;
}
.badge-a {
    background: #FEF3C7; color: #92400E !important;
    border: 1.5px solid #FCD34D;
    border-radius: 8px; padding: 5px 16px;
    font-weight: 700; font-size: 0.95rem; display: inline-block;
}
.badge-r {
    background: #FEE2E2; color: #991B1B !important;
    border: 1.5px solid #FCA5A5;
    border-radius: 8px; padding: 5px 16px;
    font-weight: 700; font-size: 0.95rem; display: inline-block;
}
.badge-n {
    background: #F3F4F6; color: #4B5563 !important;
    border: 1.5px solid #D1D5DB;
    border-radius: 8px; padding: 5px 16px;
    font-weight: 700; font-size: 0.95rem; display: inline-block;
}

/* ── Chat bubbles ── */
.bubble-user {
    background: #D1FAE5 !important;
    border-radius: 20px 20px 4px 20px;
    padding: 16px 22px;
    margin: 12px 0;
    margin-left: 8%;
    font-size: 1.1rem;
    line-height: 1.9;
    color: #1A1A1A !important;
    border: 1px solid #6EE7B7;
}
.bubble-bot {
    background: #F0F4F8 !important;
    border-radius: 20px 20px 20px 4px;
    padding: 16px 22px;
    margin: 12px 0;
    margin-right: 8%;
    font-size: 1.1rem;
    line-height: 1.9;
    color: #1A1A1A !important;
    border: 1px solid #D1D5DB;
}
.bubble-user *, .bubble-bot * { color: #1A1A1A !important; }
.bubble-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #5A5A5A !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

/* ── Wizard box ── */
.wizard-box {
    background: #FFFFFF !important;
    border: 2px solid #B8DDCA !important;
    border-top: 6px solid #1A5C36 !important;
    border-radius: 20px;
    padding: 34px 38px;
    margin: 0 auto;
    max-width: 620px;
    box-shadow: 0 8px 32px rgba(26,92,54,0.12);
    color: #1A1A1A !important;
}
.wizard-box h2 { color: #1A5C36 !important; }
.wizard-box p  { color: #3A3A3A !important; }
.step-pill {
    background: #D1FAE5 !important;
    color: #065F46 !important;
    border-radius: 20px;
    padding: 6px 18px;
    font-size: 0.88rem;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 18px;
    border: 1px solid #6EE7B7;
    font-family: 'Noto Sans', sans-serif !important;
}

/* ── Feature list card (entry screen right col) ── */
.feature-card {
    background: #FFFFFF !important;
    border: 2px solid #B8DDCA !important;
    border-radius: 18px;
    padding: 28px;
    color: #1A1A1A !important;
    box-shadow: 0 4px 18px rgba(26,92,54,0.10);
}
.feature-card p { color: #1A1A1A !important; }
.feature-card .disc { font-size: 0.95rem; color: #5A5A5A !important; }

/* ── Meal plan expander card ── */
.meal-slot-label {
    font-weight: 700;
    font-size: 1.05rem;
    color: #1A5C36 !important;
}

/* ── Footer disclaimer ── */
.footer-disclaimer {
    font-size: 0.9rem;
    color: #6B7280 !important;
    text-align: center;
    padding: 14px 0;
    border-top: 1px solid #D1D5DB;
    margin-top: 36px;
    font-family: 'Noto Sans', sans-serif !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #1A5C36 !important; }
[data-testid="stSpinner"] p { color: #1A5C36 !important; }

/* ── Selectbox text (opened) ── */
[data-baseweb="select"] span { color: #1A1A1A !important; }

/* ── Multiselect tags ── */
[data-baseweb="tag"] {
    background: #D1FAE5 !important;
    color: #065F46 !important;
}

/* ── Number input +/- buttons ── */
.stNumberInput button {
    background: #EEF7F1 !important;
    color: #1A5C36 !important;
    border-color: #B8DDCA !important;
    min-height: 38px !important;
}

/* ── Toggle switch ── */
[data-testid="stToggleSwitch"] {
    accent-color: #1A5C36 !important;
}

/* ── Balloons / success animations pass-through ── */
.balloons { z-index: 9999 !important; }
</style>
""", unsafe_allow_html=True)


# ── Core helpers ──────────────────────────────────────────────────────────────
ss = st.session_state

def normalize_phone(p): return re.sub(r"[^\d+]", "", p.strip())
def user_key_from_phone(p):
    salt = os.getenv("PHONE_SALT", "dev-salt-change-me")
    return hashlib.sha256((salt + p).encode()).hexdigest()
def last4(p):
    d = re.sub(r"\D", "", p)
    return d[-4:] if len(d) >= 4 else d

def _lang(): return ss.get("lang", "en")
def t(k):    return T[_lang()].get(k, T["en"].get(k, k))

def _lang_toggle(key_suffix=""):
    if st.button(t("lang_btn"), key=f"lang_{key_suffix}_{ss.get('_lc',0)}"):
        ss["lang"] = "ur" if _lang() == "en" else "en"
        ss["_lc"]  = ss.get("_lc", 0) + 1
        ss["current_tip"] = get_tip(_lang())
        st.rerun()

def _get_user(): return ss.get("user_key", "").strip()
def _triage_level(): return ss.get("triage_level")
def _blocked(): return _triage_level() == "RED"
def _parse_fastings(vals): return [v for v in vals if v and v > 0]

def _profile_context() -> str:
    parts = []
    if ss.get("name"):              parts.append(f"Name: {ss['name']}")
    if ss.get("age"):               parts.append(f"Age: {ss['age']}")
    if ss.get("diabetes_type"):     parts.append(f"Diabetes: {ss['diabetes_type']}")
    if ss.get("has_hypertension"):  parts.append("Has hypertension")
    if ss.get("has_high_cholesterol"): parts.append("Has high cholesterol")
    if ss.get("triage_level"):      parts.append(f"Triage: {ss['triage_level']}")
    if ss.get("week_plan"):
        day1 = ss["week_plan"]["days"][0] if isinstance(ss["week_plan"], dict) else ss["week_plan"][0]
        slots = ss["week_plan"].get("slots", ["breakfast","lunch","dinner"]) if isinstance(ss["week_plan"], dict) else ["breakfast","lunch","dinner"]
        items = [f"{s}: {day1[s]['name']}" for s in slots if s in day1]
        parts.append("Today's plan: " + ", ".join(items))
    return " | ".join(parts)

def _run_triage(
    diabetes_type, has_hypertension, has_high_cholesterol,
    bp_sys=None, bp_dia=None, a1c=None,
    fasting_readings=None, total_chol=None, other_major=False
):
    level, flags = triage_profile(
        diabetes_type=diabetes_type,
        has_hypertension=has_hypertension,
        has_high_cholesterol=has_high_cholesterol,
        bp_sys=bp_sys, bp_dia=bp_dia, a1c=a1c,
        fasting_readings=fasting_readings or [],
        total_cholesterol=total_chol,
        other_major_conditions=other_major,
    )
    ss["triage_level"] = level
    ss["triage_flags"] = flags
    return level, flags

# Helper: get days list from plan (handles both old list and new dict format)
def _plan_days():
    plan = ss.get("week_plan")
    if not plan:
        return []
    if isinstance(plan, dict):
        return plan.get("days", [])
    return plan  # legacy list format

def _plan_slots():
    plan = ss.get("week_plan")
    if isinstance(plan, dict):
        return plan.get("slots", ["breakfast", "lunch", "dinner", "snack"])
    return ["breakfast", "lunch", "dinner", "snack"]

def _plan_profile():
    plan = ss.get("week_plan")
    if isinstance(plan, dict):
        return plan.get("profile")
    return None


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def _sidebar():
    with st.sidebar:
        _lang_toggle("sb")
        st.divider()
        st.markdown(f"## 🩺 {t('app_title')}")
        st.caption(t("app_subtitle"))

        if _get_user():
            name = ss.get("name") or ss.get("display_name", "")
            st.success(f"**{t('hi_user')}**, {name}!")

            level = _triage_level()
            if level:
                cls = {"GREEN": "badge-g", "AMBER": "badge-a", "RED": "badge-r"}.get(level, "badge-n")
                lbl = {"GREEN": t("status_green"), "AMBER": t("status_amber"), "RED": t("status_red")}.get(level, "")
                st.markdown(f'<span class="{cls}">{lbl}</span>', unsafe_allow_html=True)

            st.divider()
            if st.button(t("logout_btn"), use_container_width=True):
                ss["_confirm_logout"] = True
            if ss.get("_confirm_logout"):
                st.warning(t("logout_confirm"))
                c1, c2 = st.columns(2)
                if c1.button(t("yes"), key="ly"):
                    for k in list(ss.keys()):
                        del ss[k]
                    st.rerun()
                if c2.button(t("no"), key="ln"):
                    ss["_confirm_logout"] = False
                    st.rerun()

        st.divider()
        with st.expander(t("disclaimer_title")):
            st.markdown(t("disclaimer_text"))
        st.caption(t("version"))

_sidebar()


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if "user_key" not in ss:
    top_l, top_r = st.columns([5, 1])
    with top_r:
        _lang_toggle("entry")

    st.markdown(f"# 🩺 {t('app_title')}")
    st.markdown(f"### {t('entry_heading')}")
    st.caption(t("entry_subtitle"))
    st.divider()

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        name  = st.text_input(t("entry_name"),  placeholder=t("entry_name_hint"))
        phone = st.text_input(t("entry_phone"),  placeholder=t("entry_phone_ph"))
        st.caption(t("entry_phone_hint"))
        st.caption(t("entry_privacy"))

        if st.button(t("entry_btn"), type="primary"):
            pn = normalize_phone(phone)
            if not name.strip():
                st.error(t("name_error")); st.stop()
            if not pn.startswith("+") or len(pn) < 8:
                st.error(t("phone_error")); st.stop()

            with st.spinner(t("finding_plan")):
                uk = user_key_from_phone(pn)
                ss["user_key"]     = uk
                ss["display_name"] = name.strip()
                ss["phone_last4"]  = last4(pn)

                try:
                    prof = get_profile(uk)
                except Exception:
                    st.error(t("db_error")); st.stop()

                if prof and prof.get("age"):
                    ss.update({
                        "name":                 prof.get("full_name") or name.strip(),
                        "age":                  prof.get("age") or 30,
                        "gender":               prof.get("gender") or "Prefer not to say",
                        "height_cm":            prof.get("height_cm") or 0,
                        "weight_kg":            prof.get("weight_kg") or 0.0,
                        "family_history":       prof.get("family_history") or [],
                        "diabetes_type":        prof.get("diabetes_type") or "Type 2",
                        "has_hypertension":     bool(prof.get("has_hypertension") or 0),
                        "has_high_cholesterol": bool(prof.get("has_high_cholesterol") or 0),
                        "phone_last4":          prof.get("phone_last4") or last4(pn),
                        "prefer_desi":          True,
                        "veg_only":             False,
                        "profile_complete":     True,
                        "setup_step":           "done",
                        "on_insulin":           ss.get("on_insulin", False),
                        "hypo_episodes":        ss.get("hypo_episodes", False),
                        "weakness_between":     ss.get("weakness_between", False),
                    })
                    h = prof.get("height_cm") or 0
                    w = prof.get("weight_kg") or 0
                    if h > 0 and w > 0:
                        ss["bmi"] = w / ((h / 100) ** 2)
                    st.success(f"{t('welcome_back')}, {ss['name']}! 👋")
                else:
                    upsert_profile(uk, {
                        "full_name":      name.strip(),
                        "phone_last4":    last4(pn),
                        "family_history": [],
                    })
                    ss.update({
                        "name":             name.strip(),
                        "profile_complete": False,
                        "setup_step":       1,
                        "prefer_desi":      True,
                        "veg_only":         False,
                    })
                    st.info(t("new_user_found"))
            st.rerun()

    with col2:
        lang = _lang()
        features = [
            ("✅", "Bilingual health chatbot — English & Urdu" if lang == "en" else "اردو اور انگریزی میں صحت کا مددگار"),
            ("🥗", "Personalised 7-day desi meal plan"         if lang == "en" else "ذاتی 7 دن کا دیسی کھانے کا منصوبہ"),
            ("📊", "Blood sugar tracker with trend chart"       if lang == "en" else "بلڈ شوگر ٹریکر"),
            ("💡", "AI healthy food swap suggestions"           if lang == "en" else "AI سے صحت مند کھانے کی تجاویز"),
        ]
        disc = ("This app supports healthy habits. It does <b>not</b> replace your doctor."
                if lang == "en" else
                "یہ ایپ صحت مند عادات میں مدد کرتی ہے۔ یہ آپ کے <b>ڈاکٹر کی جگہ نہیں لیتی</b>۔")
        rows_html = "".join(
            f'<p style="margin:10px 0;font-size:1.1rem;color:#1A1A1A;">'
            f'<span style="font-size:1.3rem;">{ico}</span>&nbsp; {txt}</p>'
            for ico, txt in features
        )
        st.markdown(
            f'<div class="feature-card">'
            f'{rows_html}'
            f'<hr style="border:none;border-top:1.5px solid #B8DDCA;margin:16px 0;">'
            f'<p class="disc">⚠️ {disc}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# WIZARD  (new users only)
# ══════════════════════════════════════════════════════════════════════════════
if ss.get("setup_step") in (1, 2):
    step = ss["setup_step"]

    wl, wr = st.columns([5, 1])
    with wr:
        _lang_toggle("wiz")

    st.markdown(f"# 🩺 {t('app_title')}")

    _, mid, _ = st.columns([1, 3, 1])
    with mid:
        heading = t("wizard_step1_heading") if step == 1 else t("wizard_step2_heading")
        caption = t("wizard_step1_caption") if step == 1 else t("wizard_step2_caption")
        pill    = f"{'1' if step == 1 else '2'} / 2"

        st.markdown(
            f'<div class="wizard-box">'
            f'<div class="step-pill">Step {pill}</div>'
            f'<h2>{heading}</h2>'
            f'<p style="color:#4A4A4A;margin-bottom:22px;">{caption}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if step == 1:
            name_val = st.text_input(t("wizard_name"), value=ss.get("name", ""))
            age_val  = st.number_input(t("wizard_age"), 1, 110,
                                       value=int(ss.get("age", 50)),
                                       help=t("wizard_age_note"))
            d_opts_disp = t("wizard_diabetes_opts")
            d_opts_en   = T["en"]["wizard_diabetes_opts"]
            saved_d     = ss.get("diabetes_type", "Type 2")
            d_idx       = d_opts_en.index(saved_d) if saved_d in d_opts_en else 0
            dtype_disp  = st.selectbox(t("wizard_diabetes"), d_opts_disp, index=d_idx)

            pref_desi = st.checkbox(t("wizard_desi"), value=ss.get("prefer_desi", True))
            veg_only  = st.checkbox(t("wizard_veg"),  value=ss.get("veg_only", False))

            if st.button(t("wizard_next"), type="primary"):
                if not name_val.strip():
                    st.error(t("name_error")); st.stop()
                dtype_en = d_opts_en[d_opts_disp.index(dtype_disp)]
                ss.update({
                    "name":          name_val.strip(),
                    "age":           int(age_val),
                    "diabetes_type": dtype_en,
                    "prefer_desi":   pref_desi,
                    "veg_only":      veg_only,
                    "setup_step":    2,
                })
                st.rerun()

        else:
            has_hypert = st.checkbox(t("wizard_hypert"), value=ss.get("has_hypertension", False))
            has_chol   = st.checkbox(t("wizard_chol"),   value=ss.get("has_high_cholesterol", False))
            other_maj  = st.checkbox(t("wizard_other"))

            st.divider()
            st.markdown(f"**{'Meal frequency questions' if _lang()=='en' else 'کھانے کی تعداد کے سوالات'}**")

            on_insulin  = st.checkbox(t("q_insulin"),  value=ss.get("on_insulin",  False), help=t("q_insulin_help"))
            hypo_ep     = st.checkbox(t("q_hypo"),     value=ss.get("hypo_episodes", False), help=t("q_hypo_help"))
            weakness_bw = st.checkbox(t("q_weakness"), value=ss.get("weakness_between", False), help=t("q_weakness_help"))

            c1, c2 = st.columns(2)
            with c1:
                if st.button(t("wizard_back")):
                    ss["setup_step"] = 1; st.rerun()
            with c2:
                if st.button(t("wizard_finish"), type="primary"):
                    with st.spinner(t("wizard_saving")):
                        ss.update({
                            "has_hypertension":     has_hypert,
                            "has_high_cholesterol": has_chol,
                            "on_insulin":           on_insulin,
                            "hypo_episodes":        hypo_ep,
                            "weakness_between":     weakness_bw,
                            "gender":               "Prefer not to say",
                            "height_cm":            0,
                            "weight_kg":            0.0,
                            "family_history":       [],
                            "bmi":                  None,
                        })
                        _run_triage(ss["diabetes_type"], has_hypert, has_chol, other_major=other_maj)
                        upsert_profile(ss["user_key"], {
                            "full_name":            ss["name"],
                            "phone_last4":          ss.get("phone_last4"),
                            "age":                  ss["age"],
                            "gender":               "Prefer not to say",
                            "diabetes_type":        ss["diabetes_type"],
                            "has_hypertension":     1 if has_hypert else 0,
                            "has_high_cholesterol": 1 if has_chol  else 0,
                            "family_history":       [],
                        })
                        ss["week_plan"] = generate_week_plan(
                            prefer_desi=ss.get("prefer_desi", True),
                            veg_only=ss.get("veg_only", False),
                            has_hypertension=has_hypert,
                            has_high_cholesterol=has_chol,
                            on_insulin=on_insulin,
                            hypo_episodes=hypo_ep,
                            weakness_between=weakness_bw,
                            bmi=ss.get("bmi"),
                            diabetes_type=ss["diabetes_type"],
                        )
                        ss["profile_complete"] = True
                        ss["setup_step"]       = "done"

                    st.success(t("wizard_done_msg"))
                    st.rerun()
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
if "current_tip"     not in ss: ss["current_tip"]     = get_tip(_lang())
if "chat_history"    not in ss: ss["chat_history"]     = []
if "editing_profile" not in ss: ss["editing_profile"]  = False

tl, tr = st.columns([6, 1])
with tr:
    _lang_toggle("main")

if not ss.get("week_plan"):
    with st.spinner(t("loading_plan")):
        ss["week_plan"] = generate_week_plan(
            prefer_desi=ss.get("prefer_desi", True),
            veg_only=ss.get("veg_only", False),
            has_hypertension=ss.get("has_hypertension", False),
            has_high_cholesterol=ss.get("has_high_cholesterol", False),
            on_insulin=ss.get("on_insulin", False),
            hypo_episodes=ss.get("hypo_episodes", False),
            weakness_between=ss.get("weakness_between", False),
            bmi=ss.get("bmi"),
            diabetes_type=ss.get("diabetes_type", "Type 2"),
        )

tabs = st.tabs([t("tab_plan"), t("tab_chat"), t("tab_glucose"), t("tab_dashboard")])

# Slot display config
SLOT_ICONS = {
    "breakfast":  ("🌅", "Breakfast",        "ناشتہ"),
    "snack_am":   ("🍎", "Mid-Morning Snack", "دوپہر سے پہلے کا ناشتہ"),
    "lunch":      ("☀️", "Lunch",             "دوپہر کا کھانا"),
    "snack_pm":   ("🍊", "Afternoon Snack",   "شام کا ناشتہ"),
    "dinner":     ("🌙", "Dinner",            "رات کا کھانا"),
    "snack_bed":  ("🌛", "Bedtime Snack",     "سونے سے پہلے کا ناشتہ"),
    # legacy key
    "snack":      ("🍎", "Snack",             "ناشتہ"),
}


# ══════════════════════════════════════════════════════════════════════════════
# TAB 0 — MY PLAN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:

    # ── Profile card ──────────────────────────────────────────────────────────
    level     = _triage_level()
    badge_cls = {"GREEN": "badge-g", "AMBER": "badge-a", "RED": "badge-r"}.get(level or "", "badge-n")
    badge_lbl = {
        "GREEN": t("status_green"),
        "AMBER": t("status_amber"),
        "RED":   t("status_red"),
    }.get(level or "", t("status_none"))

    conditions = []
    if ss.get("has_hypertension"):     conditions.append("Hypertension" if _lang()=="en" else "ہائی بلڈ پریشر")
    if ss.get("has_high_cholesterol"): conditions.append("High Cholesterol" if _lang()=="en" else "زیادہ کولیسٹرول")
    cond_str  = ", ".join(conditions) if conditions else t("no_conditions")
    name_disp = ss.get("name", ss.get("display_name", ""))
    age_disp  = ss.get("age", "")
    dtype_disp = ss.get("diabetes_type", "")

    pc1, pc2 = st.columns([5, 1])
    with pc1:
        st.markdown(
            f'<div class="profile-card">'
            f'<div class="profile-name">👤 {name_disp}'
            + (f", {age_disp}" if age_disp else "") +
            f'</div>'
            f'<div class="profile-detail">'
            + (f'{dtype_disp} · ' if dtype_disp else "") +
            f'{cond_str}</div>'
            f'<div style="margin-top:12px;"><span class="{badge_cls}">{badge_lbl}</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with pc2:
        st.write("")
        st.write("")
        if st.button(t("edit_profile_btn"), use_container_width=True):
            ss["editing_profile"] = not ss.get("editing_profile", False)
            st.rerun()

    # ── Profile edit form ─────────────────────────────────────────────────────
    if ss.get("editing_profile"):
        with st.expander("", expanded=True):
            st.markdown(f"#### ✏️ {'Edit Profile' if _lang()=='en' else 'پروفائل تبدیل کریں'}")

            ef1, ef2 = st.columns(2)
            with ef1:
                e_name = st.text_input(t("pf_name"), value=ss.get("name", ""), key="e_name")
                e_age  = st.number_input(t("pf_age"), 1, 110, int(ss.get("age", 50) or 50), key="e_age")
            with ef2:
                e_g_opts  = t("pf_gender_opts"); e_g_en = T["en"]["pf_gender_opts"]
                e_g_saved = ss.get("gender", "Prefer not to say")
                e_g_idx   = e_g_en.index(e_g_saved) if e_g_saved in e_g_en else 0
                e_gender  = st.selectbox(t("pf_gender"), e_g_opts, index=e_g_idx, key="e_gender")

                e_d_opts  = t("pf_diabetes_opts"); e_d_en = T["en"]["pf_diabetes_opts"]
                e_d_saved = ss.get("diabetes_type", "Type 2")
                e_d_idx   = e_d_en.index(e_d_saved) if e_d_saved in e_d_en else 0
                e_dtype   = st.selectbox(t("pf_diabetes"), e_d_opts, index=e_d_idx, key="e_dtype")

            ef3, ef4 = st.columns(2)
            with ef3:
                e_height = st.number_input(t("pf_height"), 0, 250, int(ss.get("height_cm", 0) or 0), key="e_h")
            with ef4:
                e_weight = st.number_input(t("pf_weight"), 0.0, 400.0, float(ss.get("weight_kg", 0.0) or 0.0), 0.5, key="e_w")

            e_bmi = None
            if e_height > 0 and e_weight > 0:
                e_bmi = e_weight / ((e_height / 100) ** 2)
                st.caption(f"{t('pf_bmi')}: **{e_bmi:.1f}** {t('pf_bmi_note')}")

            e_family = st.multiselect(t("pf_family"), T["en"]["pf_family_opts"],
                                      default=ss.get("family_history", []), key="e_fam")

            ec1, ec2, ec3 = st.columns(3)
            with ec1: e_hypert = st.checkbox(t("pf_hypert"), value=ss.get("has_hypertension", False), key="e_hy")
            with ec2: e_chol   = st.checkbox(t("pf_chol"),   value=ss.get("has_high_cholesterol", False), key="e_ch")
            with ec3: e_other  = st.checkbox(t("pf_other"),  key="e_ot")

            st.divider()
            st.markdown(f"**{'Meal frequency questions' if _lang()=='en' else 'کھانے کی تعداد کے سوالات'}**")
            ef_c1, ef_c2, ef_c3 = st.columns(3)
            with ef_c1: e_insulin  = st.checkbox(t("q_insulin"),  value=ss.get("on_insulin", False),       key="e_ins", help=t("q_insulin_help"))
            with ef_c2: e_hypo     = st.checkbox(t("q_hypo"),     value=ss.get("hypo_episodes", False),     key="e_hyp", help=t("q_hypo_help"))
            with ef_c3: e_weakness = st.checkbox(t("q_weakness"), value=ss.get("weakness_between", False),  key="e_wkn", help=t("q_weakness_help"))

            with st.expander(t("pf_advanced")):
                st.caption(t("pf_advanced_note"))
                ea1, ea2, ea3 = st.columns(3)
                with ea1:
                    e_bps = st.number_input(t("pf_bp_sys"), 0, 300, 130 if e_hypert else 0, key="e_bps")
                    e_bpd = st.number_input(t("pf_bp_dia"), 0, 200, 80  if e_hypert else 0, key="e_bpd")
                with ea2:
                    e_a1c = st.number_input(t("pf_a1c"), 0.0, 20.0, 0.0, 0.1, key="e_a1c")
                with ea3:
                    e_tc  = st.number_input(t("pf_chol_val"), 0.0, 600.0, 0.0, 1.0, key="e_tc")
                st.markdown(f"**{t('pf_fasting_head')}**")
                st.caption(t("pf_fasting_note"))
                ef1c, ef2c, ef3c = st.columns(3)
                with ef1c: e_f1 = st.number_input(t("pf_day3"), 0.0, 600.0, 0.0, 1.0, key="e_f1")
                with ef2c: e_f2 = st.number_input(t("pf_day2"), 0.0, 600.0, 0.0, 1.0, key="e_f2")
                with ef3c: e_f3 = st.number_input(t("pf_day1"), 0.0, 600.0, 0.0, 1.0, key="e_f3")

            if st.button(t("save_profile_btn"), type="primary", key="save_profile"):
                with st.spinner(t("saving_profile")):
                    gender_en = T["en"]["pf_gender_opts"][T[_lang()]["pf_gender_opts"].index(e_gender)]
                    dtype_en  = T["en"]["pf_diabetes_opts"][T[_lang()]["pf_diabetes_opts"].index(e_dtype)]
                    ss.update({
                        "name": e_name.strip(), "age": int(e_age),
                        "gender": gender_en, "diabetes_type": dtype_en,
                        "height_cm": int(e_height), "weight_kg": float(e_weight),
                        "family_history": e_family, "bmi": e_bmi,
                        "has_hypertension": e_hypert, "has_high_cholesterol": e_chol,
                        "on_insulin": e_insulin, "hypo_episodes": e_hypo,
                        "weakness_between": e_weakness,
                    })
                    _run_triage(
                        dtype_en, e_hypert, e_chol,
                        bp_sys=float(e_bps) if e_bps > 0 else None,
                        bp_dia=float(e_bpd) if e_bpd > 0 else None,
                        a1c=float(e_a1c) if e_a1c > 0 else None,
                        fasting_readings=_parse_fastings([e_f1, e_f2, e_f3]),
                        total_chol=float(e_tc) if e_tc > 0 else None,
                        other_major=e_other,
                    )
                    upsert_profile(ss["user_key"], {
                        "full_name": e_name.strip(), "phone_last4": ss.get("phone_last4"),
                        "age": int(e_age), "gender": gender_en,
                        "height_cm": int(e_height) if e_height else None,
                        "weight_kg": float(e_weight) if e_weight else None,
                        "family_history": e_family, "diabetes_type": dtype_en,
                        "has_hypertension": 1 if e_hypert else 0,
                        "has_high_cholesterol": 1 if e_chol else 0,
                    })
                    ss["week_plan"] = generate_week_plan(
                        prefer_desi=ss.get("prefer_desi", True),
                        veg_only=ss.get("veg_only", False),
                        has_hypertension=e_hypert, has_high_cholesterol=e_chol,
                        on_insulin=e_insulin, hypo_episodes=e_hypo,
                        weakness_between=e_weakness, bmi=e_bmi, diabetes_type=dtype_en,
                    )
                    ss["editing_profile"] = False
                st.success(t("profile_saved"))
                st.rerun()

            if ss.get("triage_level"):
                lv = ss["triage_level"]
                if lv == "GREEN":   st.success(t("green_result"))
                elif lv == "AMBER": st.warning(t("amber_result"))
                else:               st.error(t("red_result"))
                for f in ss.get("triage_flags", []):
                    st.write("•", f)

    st.divider()

    # ── Tip banner ────────────────────────────────────────────────────────────
    tc, tb = st.columns([5, 1])
    with tc:
        st.markdown(
            f'<div class="tip-banner">'
            f'<div class="tip-label">{t("tip_title")}</div>'
            f'{ss["current_tip"]}'
            f'</div>',
            unsafe_allow_html=True,
        )
    with tb:
        st.write(""); st.write("")
        if st.button(t("tip_new"), use_container_width=True, key="new_tip"):
            ss["current_tip"] = get_tip(_lang())
            st.rerun()

    # ── Meal structure banner ─────────────────────────────────────────────────
    plan_profile = _plan_profile()
    if plan_profile:
        lang = _lang()
        reason = plan_profile.get("reason_en" if lang=="en" else "reason_ur", "")
        label  = plan_profile.get("label_en"  if lang=="en" else "label_ur",  "")
        portion = plan_profile.get("portion_note_en" if lang=="en" else "portion_note_ur", "")
        if reason:
            st.info(f"**{t('meal_structure')}: {label}**\n\n{reason}" + (f"\n\n📏 {portion}" if portion else ""))
        # Reminders for high-risk profiles
        if ss.get("on_insulin") or ss.get("hypo_episodes"):
            st.warning(t("insulin_reminder") if ss.get("on_insulin") else "")
            if ss.get("hypo_episodes"):
                st.warning(t("hypo_reminder"))

    # ── 7-Day Meal Plan ───────────────────────────────────────────────────────
    st.markdown(f"## 🥗 {t('plan_heading')}")

    if _blocked():
        st.error(t("plan_blocked"))
    else:
        pc1, pc2, pc3 = st.columns([2, 2, 2])
        with pc1: prefer_desi = st.toggle(t("desi_toggle"), value=ss.get("prefer_desi", True), key="pd_tog")
        with pc2: veg_only    = st.toggle(t("veg_toggle"),  value=ss.get("veg_only", False),   key="vo_tog")
        with pc3:
            if st.button(t("regen_btn")):
                with st.spinner(t("building_plan")):
                    ss["week_plan"] = generate_week_plan(
                        prefer_desi=prefer_desi, veg_only=veg_only,
                        has_hypertension=ss.get("has_hypertension", False),
                        has_high_cholesterol=ss.get("has_high_cholesterol", False),
                        on_insulin=ss.get("on_insulin", False),
                        hypo_episodes=ss.get("hypo_episodes", False),
                        weakness_between=ss.get("weakness_between", False),
                        bmi=ss.get("bmi"), diabetes_type=ss.get("diabetes_type", "Type 2"),
                    )
                ss["prefer_desi"] = prefer_desi
                ss["veg_only"]    = veg_only
                st.rerun()
        ss["prefer_desi"] = prefer_desi
        ss["veg_only"]    = veg_only

        days  = _plan_days()
        slots = _plan_slots()
        lang  = _lang()

        for day in days:
            day_carbs = sum(
                day[s]["carb_servings"] * CARB["carb_serving_grams"]
                for s in slots if s in day
            )
            with st.expander(f"📅 {t('day_label')} {day['day']}  —  ~{day_carbs:.0f}g {t('carbs_label')}"):
                for slot in slots:
                    if slot not in day:
                        continue
                    meal = day[slot]
                    cfg  = SLOT_ICONS.get(slot, ("🍽️", slot.title(), slot.title()))
                    icon, lbl_en, lbl_ur = cfg
                    lbl  = lbl_en if lang == "en" else lbl_ur
                    cg   = meal["carb_servings"] * CARB["carb_serving_grams"]
                    st.markdown(
                        f'<p class="meal-slot-label">{icon} {lbl}</p>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**{meal['name']}**")
                    st.caption(f"~{cg}g carbs  |  {meal['notes']}")
                    st.markdown("---")

                if st.button(t("swaps_btn"), key=f"sw_{day['day']}"):
                    slot_names = [day[s]['name'] for s in slots if s in day]
                    txt = "; ".join(slot_names)
                    with st.spinner(t("getting_swaps")):
                        swaps = generate_swaps(txt)
                    st.markdown(f"**{t('swaps_heading')}**")
                    for s in swaps:
                        st.write("•", s)

    st.divider()

    # ── Daily Check-In ────────────────────────────────────────────────────────
    st.markdown(f"### {t('checkin_heading')}")
    user = _get_user()

    if not _blocked():
        ci_date  = st.date_input(t("checkin_date"), value=date.today(), key="ci_date")
        followed = st.radio(t("followed_q"), [t("yes_opt"), t("no_opt")], horizontal=True, key="ci_rad")

        if followed == t("yes_opt"):
            if st.button(t("save_ci_btn"), type="primary", key="ci_yes"):
                with st.spinner("Saving..."):
                    add_daily_checkin(user, ci_date, followed_plan=True, actual_meals="")
                st.success(t("ci_saved"))
                st.balloons()
        else:
            actual = st.text_area(t("ate_label"), placeholder=t("ate_ph"), height=110, key="ci_ate")
            if st.button(t("save_suggest_btn"), type="primary", key="ci_no"):
                if not actual.strip():
                    st.warning(t("describe_ate"))
                else:
                    with st.spinner(t("saving_suggest")):
                        add_daily_checkin(user, ci_date, followed_plan=False, actual_meals=actual.strip())
                        tips = coach_on_actual_meal(actual.strip())
                    st.success(t("suggest_saved"))
                    for tip in tips:
                        st.write("•", tip)
                    st.caption(t("suggest_note"))

    st.markdown(
        f'<div class="footer-disclaimer">⚠️ {APP["disclaimer"]}</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ASK (Chatbot)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown(f"## 💬 {t('chat_heading')}")
    st.caption(t("chat_caption"))
    st.divider()

    if not ss["chat_history"]:
        greeting = t("chat_greeting_en").replace("\n", "<br>")
        st.markdown(
            f'<div class="bubble-bot">'
            f'<div class="bubble-label">🩺 Sehat Saathi / صحت ساتھی</div>'
            f'{greeting}</div>',
            unsafe_allow_html=True,
        )

    uname = ss.get("name", ss.get("display_name", "You"))
    for msg in ss["chat_history"]:
        content = msg["content"].replace("\n", "<br>")
        if msg["role"] == "user":
            st.markdown(
                f'<div class="bubble-user">'
                f'<div class="bubble-label">👤 {uname}</div>{content}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="bubble-bot">'
                f'<div class="bubble-label">🩺 Sehat Saathi</div>{content}</div>',
                unsafe_allow_html=True,
            )

    user_input = st.chat_input(t("chat_placeholder"))
    if user_input:
        ss["chat_history"].append({"role": "user", "content": user_input})
        with st.spinner(t("chat_thinking")):
            reply = chat_with_assistant(
                ss["chat_history"],
                lang=_lang(),
                user_profile=_profile_context(),
            )
        ss["chat_history"].append({"role": "assistant", "content": reply})
        st.rerun()

    if ss["chat_history"]:
        if st.button(t("chat_clear"), key="clr_chat"):
            ss["chat_history"] = []
            st.rerun()

    st.caption(t("chat_note"))


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LOG SUGAR
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown(f"## 📊 {t('glucose_heading')}")
    user = _get_user()

    if _blocked():
        st.error(t("blocked_msg"))
    else:
        c1, c2 = st.columns(2)
        with c1:
            r_type = st.selectbox(t("reading_lbl"), t("reading_types"),
                                  help="Fasting = no food 8+ hours. Post-meal = 1-2h after eating.")
            m_date = st.date_input(t("date_lbl"), value=date.today())
            m_time = st.time_input(t("time_lbl"), value=datetime.now().time())
        with c2:
            value     = st.number_input(t("value_lbl"), 0.0, 600.0, 110.0, 1.0)
            meal_note = st.text_input(t("note_lbl"), placeholder=t("note_ph"))
            st.caption(t("ref_ranges").format(h=TRIAGE["hypo"], vh=TRIAGE["very_high"]))
            if value >= TRIAGE["very_high"]:
                st.error(t("very_high_alert"))
            elif 0 < value < TRIAGE["hypo"]:
                st.warning(t("low_alert"))

        if st.button(t("save_reading_btn"), type="primary"):
            with st.spinner(t("saving_reading")):
                add_glucose_log(user, datetime.combine(m_date, m_time), r_type, value, meal_note)
            st.success(t("reading_saved"))

    st.markdown(
        f'<div class="footer-disclaimer">⚠️ {APP["disclaimer"]}</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PROGRESS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown(f"## 📈 {t('dash_heading')}")
    st.caption(t("dash_caption"))
    user = _get_user()

    c1, c2 = st.columns(2)
    rows = None

    with c1:
        st.markdown(f"### {t('adh_section')}")
        checkins = fetch_checkins(user)
        if checkins:
            cdf = pd.DataFrame(checkins, columns=["date", "followed_plan", "actual_meals"])
            cdf["date"] = pd.to_datetime(cdf["date"]).dt.date
            adh = (cdf["followed_plan"].sum() / len(cdf)) * 100
            st.metric(t("adh_metric"), f"{adh:.0f}%",
                      delta=t("adh_delta").format(n=len(cdf)))
            st.dataframe(
                cdf[["date", "followed_plan"]].rename(columns={
                    "date": t("col_date"), "followed_plan": t("col_fol")
                }),
                use_container_width=True,
            )
        else:
            st.info(t("no_checkins"))

    with c2:
        st.markdown(f"### {t('gluc_section')}")
        rows = fetch_glucose_logs(user)
        if rows:
            df  = pd.DataFrame(rows, columns=["measured_at", "type", "value", "meal_note"])
            df["measured_at"] = pd.to_datetime(df["measured_at"])
            avg = df["value"].mean()
            std = df["value"].std()
            hc  = int((df["value"] >= TRIAGE["very_high"]).sum())
            lc  = int((df["value"] < TRIAGE["hypo"]).sum())
            m1, m2, m3 = st.columns(3)
            m1.metric(t("avg_lbl"),   f"{avg:.0f} mg/dL")
            m2.metric(t("var_lbl"),   f"±{std:.0f}")
            m3.metric(t("total_lbl"), len(df))
            if hc: st.warning(t("high_alert_d").format(n=hc))
            if lc: st.warning(t("low_alert_d").format(n=lc))
        else:
            st.info(t("no_glucose"))

    if rows:
        st.markdown(f"### {t('trend_head')}")
        fig, ax = plt.subplots(figsize=(10, 3.2))
        fig.patch.set_facecolor("#FAFAF7")
        ax.set_facecolor("#FFFFFF")
        ax.plot(df["measured_at"], df["value"],
                marker="o", lw=2.5, color="#1A5C36", ms=6, zorder=3)
        ax.fill_between(df["measured_at"], df["value"],
                        alpha=0.10, color="#1A5C36")
        ax.axhline(TRIAGE["very_high"], color="#DC2626", ls="--", lw=1.5, alpha=0.7,
                   label=f"Very high ({TRIAGE['very_high']})")
        ax.axhline(TRIAGE["hypo"],      color="#D4861A", ls="--", lw=1.5, alpha=0.7,
                   label=f"Low ({TRIAGE['hypo']})")
        ax.set_ylabel("mg/dL", fontsize=12, color="#1A1A1A")
        ax.tick_params(colors="#1A1A1A", labelsize=10)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        ax.spines["left"].set_color("#C8E2D0")
        ax.spines["bottom"].set_color("#C8E2D0")
        ax.legend(fontsize=9, labelcolor="#1A1A1A")
        plt.xticks(rotation=30, fontsize=9, color="#1A1A1A")
        plt.tight_layout()
        st.pyplot(fig)
        st.caption(t("trend_note"))
        with st.expander(t("view_all")):
            st.dataframe(df.rename(columns={
                "measured_at": t("col_time"), "type": t("col_type"),
                "value": t("col_val"), "meal_note": t("col_note"),
            }), use_container_width=True)

    st.markdown(
        f'<div class="footer-disclaimer">⚠️ {APP["disclaimer"]}</div>',
        unsafe_allow_html=True,
    )

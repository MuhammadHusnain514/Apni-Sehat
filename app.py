# app.py  –  Apni Sehat v1.2
import os, re, hashlib
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
    try:    return str(st.secrets.get(k, d)).strip()
    except: return d

os.environ["GROQ_API_KEY"]  = _sget("GROQ_API_KEY",  os.getenv("GROQ_API_KEY",  ""))
os.environ["GROQ_BASE_URL"] = _sget("GROQ_BASE_URL", os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"))
os.environ["GROQ_MODEL"]    = _sget("GROQ_MODEL",    os.getenv("GROQ_MODEL",    "llama-3.3-70b-versatile"))
os.environ["DATABASE_URL"]  = _sget("DATABASE_URL",  os.getenv("DATABASE_URL",  ""))
os.environ["PHONE_SALT"]    = _sget("PHONE_SALT",    os.getenv("PHONE_SALT",    "dev-salt-change-me"))

from storage import (init_db, get_profile, upsert_profile,
                     add_glucose_log, fetch_glucose_logs,
                     add_daily_checkin, fetch_checkins)
init_db()

st.markdown("""
<style>
/* Inter font only — do NOT import Material Icons/Symbols.
   When those fonts fail to load they render raw ligature text as fallback. */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* ═══ 0. Colour tokens ═══ */
:root {
    --bg:       #0F1117;
    --bg2:      #181C27;
    --bg3:      #1E2436;
    --border:   #2A3147;
    --green:    #22C55E;
    --green-dk: #16A34A;
    --green-hi: #4ADE80;
    --amber:    #F59E0B;
    --red:      #EF4444;
    --txt:      #E2E8F0;
    --txt2:     #94A3B8;
    --txt3:     #64748B;
    color-scheme: dark;
}

/* ═══ 1. Sidebar + Expander icon fix — nuclear edition ═══ */
/* Completely eliminate Material Symbols / Icons ligature text */
html body .stApp .material-symbols-rounded,
html body .material-symbols-rounded,
.material-symbols-rounded,
span.material-symbols-rounded,
button span.material-symbols-rounded,
[data-testid] span.material-symbols-rounded {
    font-size: 0 !important;
    width: 0 !important;
    max-width: 0 !important;
    height: 0 !important;
    max-height: 0 !important;
    display: inline-block !important;
    overflow: hidden !important;
    color: transparent !important;
    line-height: 0 !important;
    opacity: 0 !important;
    visibility: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    pointer-events: none !important;
}
/* Also kill the sidebar collapse icon text specifically */
[data-testid="stSidebarCollapseButton"] button p,
[data-testid="collapsedControl"] button p {
    font-size: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
    color: transparent !important;
}
/* Sidebar */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="collapsedControl"] svg { fill: var(--txt2) !important; }

/* ═══ 2. Expander layout ═══ */
[data-testid="stExpander"] summary {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    list-style: none !important;
}
[data-testid="stExpander"] summary::-webkit-details-marker { display: none !important; }
[data-testid="stExpander"] summary > * {
    /* kill any direct child that isn't the <p> label */
    flex-shrink: 0;
}
[data-testid="stExpander"] summary p {
    margin: 0 !important;
    flex: 1 !important;
    color: var(--txt) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    order: 1 !important;
}
/* Force icon span to order:0 (before label) but with zero footprint */
[data-testid="stExpander"] summary span {
    order: 0 !important;
    font-size: 0px !important;
    width: 0px !important;
    height: 0px !important;
    overflow: hidden !important;
    opacity: 0 !important;
}
[data-testid="stExpander"] summary::after {
    content: '';
    order: 2 !important;
    flex-shrink: 0;
    display: block;
    width: 7px; height: 7px;
    border-right: 2px solid var(--green);
    border-bottom: 2px solid var(--green);
    transform: rotate(45deg);
    transition: transform 0.2s ease;
    margin-left: 12px;
}
[data-testid="stExpander"] details[open] summary::after {
    transform: rotate(-135deg);
    margin-top: 3px;
}

/* ═══ 3. Base ═══ */
html, body { background:var(--bg) !important; font-family:'Inter',sans-serif !important; }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"],
[data-testid="block-container"], div.block-container, .main { background:var(--bg) !important; }

/* ═══ 4. Typography ═══ */
p, li, span, div, label, .stMarkdown p, .stMarkdown li {
    font-family:'Inter',sans-serif !important;
    font-size:0.98rem !important;
    line-height:1.75 !important;
    color:var(--txt) !important;
}
h1 { font-size:1.9rem !important; font-weight:800 !important; color:var(--green) !important; letter-spacing:-0.5px !important; }
h2 { font-size:1.4rem !important; font-weight:700 !important; color:var(--green) !important; }
h3 { font-size:1.1rem !important; font-weight:700 !important; color:var(--txt) !important; }
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2 { color:var(--green) !important; }
.stCaption, [data-testid="stCaptionContainer"] p { font-size:0.82rem !important; color:var(--txt3) !important; }

/* ═══ 5. Sidebar ═══ */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div, [data-testid="stSidebarContent"] {
    background:var(--bg2) !important; border-right:1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color:var(--txt) !important; font-family:'Inter',sans-serif !important; }
[data-testid="stSidebar"] h2 { color:var(--green) !important; font-size:1.1rem !important; font-weight:700 !important; }
[data-testid="stSidebar"] .stCaption p { color:var(--txt3) !important; font-size:0.78rem !important; }
[data-testid="stSidebar"] hr { border-color:var(--border) !important; margin:12px 0 !important; }

/* ═══ 6. Buttons ═══ */
.stButton > button[kind="primary"] {
    background:var(--green) !important; color:#0a1a0f !important; border:none !important;
    border-radius:10px !important; font-family:'Inter',sans-serif !important;
    font-size:0.95rem !important; font-weight:700 !important;
    padding:0.6rem 1.8rem !important; min-height:44px !important;
    width:auto !important; letter-spacing:0.01em !important; transition:all 0.18s ease !important;
}
.stButton > button[kind="primary"]:hover {
    background:var(--green-hi) !important; transform:translateY(-1px) !important;
    box-shadow:0 4px 16px rgba(34,197,94,0.35) !important;
}
.stButton > button {
    background:var(--bg3) !important; color:var(--green) !important;
    border:1px solid var(--border) !important; border-radius:10px !important;
    font-family:'Inter',sans-serif !important; font-size:0.9rem !important;
    font-weight:600 !important; min-height:40px !important;
    padding:0.5rem 1.2rem !important; transition:all 0.15s ease !important;
}
.stButton > button:hover { background:#1E2D1E !important; border-color:var(--green) !important; }

/* Day-accordion full-width header button */
.day-acc-row .stButton > button {
    width: 100% !important;
    text-align: left !important;
    justify-content: flex-start !important;
    color: var(--txt) !important;
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    letter-spacing: 0 !important;
}

/* ═══ 7. Inputs ═══ */
.stTextInput > div > div > input, .stNumberInput > div > div > input,
.stTextArea textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
    background:var(--bg3) !important; color:var(--txt) !important;
    border:1px solid var(--border) !important; border-radius:8px !important;
    font-family:'Inter',sans-serif !important; font-size:0.95rem !important;
    padding:0.55rem 0.9rem !important; min-height:44px !important;
}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
    border-color:var(--green) !important; box-shadow:0 0 0 2px rgba(34,197,94,0.18) !important;
}
[data-baseweb="input"] { background:var(--bg3) !important; }
.stTextInput label, .stNumberInput label, .stTextArea label, .stSelectbox label,
.stDateInput label, .stTimeInput label, .stRadio label > div > p,
.stMultiSelect label, [data-testid="stFormLabel"] p {
    color:var(--txt2) !important; font-size:0.83rem !important; font-weight:600 !important;
    letter-spacing:0.04em !important; text-transform:uppercase !important;
}

/* ═══ 8. Selectbox ═══ */
[data-baseweb="select"] > div {
    background:var(--bg3) !important; color:var(--txt) !important;
    border:1px solid var(--border) !important; border-radius:8px !important;
}
[data-baseweb="select"] span, [data-baseweb="select"] div { color:var(--txt) !important; }
[data-baseweb="popover"] [role="listbox"], [data-baseweb="menu"] {
    background:var(--bg3) !important; border:1px solid var(--border) !important; border-radius:8px !important;
}
[data-baseweb="menu"] li { color:var(--txt) !important; font-size:0.95rem !important; }
[data-baseweb="menu"] li:hover { background:#1E2D1E !important; }

/* ═══ 9. Checkboxes / Radio / Toggle ═══ */
.stCheckbox label, .stCheckbox span, [data-testid="stCheckbox"] label {
    color:var(--txt) !important; font-size:0.95rem !important;
    font-weight:400 !important; text-transform:none !important;
}
.stRadio label, .stRadio div[role="radiogroup"] label { color:var(--txt) !important; font-size:0.95rem !important; }
.stToggle label p { color:var(--txt) !important; font-size:0.95rem !important; }

/* ═══ 10. Date / Time ═══ */
input[type="date"], input[type="time"] {
    background:var(--bg3) !important; color:var(--txt) !important;
    border:1px solid var(--border) !important; border-radius:8px !important;
}

/* ═══ 11. Tabs ═══ */
.stTabs [data-baseweb="tab-list"] {
    background:var(--bg2) !important; border-bottom:1px solid var(--border) !important; gap:2px !important;
}
.stTabs [data-baseweb="tab"] {
    background:transparent !important; color:var(--txt3) !important;
    font-family:'Inter',sans-serif !important; font-size:0.88rem !important;
    font-weight:600 !important; padding:12px 18px !important;
    border-bottom:2px solid transparent !important; min-height:46px !important;
}
.stTabs [aria-selected="true"] {
    color:var(--green) !important; border-bottom:2px solid var(--green) !important; font-weight:700 !important;
}
.stTabs [data-baseweb="tab-panel"] { background:var(--bg) !important; padding-top:20px !important; }

/* ═══ 12. Expander container styling ═══ */
[data-testid="stExpander"] {
    background:var(--bg2) !important; border:1px solid var(--border) !important;
    border-radius:10px !important; overflow:hidden !important;
}
[data-testid="stExpander"] summary { padding:12px 16px !important; }
[data-testid="stExpander"] summary:hover { background:#1a2030 !important; }
[data-testid="stExpander"] > div > div { background:var(--bg2) !important; padding:12px 16px !important; }

/* ═══ 13. Metrics ═══ */
[data-testid="stMetric"] {
    background:var(--bg2) !important; border:1px solid var(--border) !important;
    border-radius:12px !important; padding:14px 18px !important;
}
[data-testid="stMetricValue"] { font-size:1.8rem !important; font-weight:800 !important; color:var(--green) !important; }
[data-testid="stMetricLabel"] { color:var(--txt2) !important; font-size:0.8rem !important; font-weight:600 !important; text-transform:uppercase !important; letter-spacing:0.05em !important; }
[data-testid="stMetricDelta"]  { color:var(--txt3) !important; }

/* ═══ 14. Alerts ═══ */
div[data-testid="stSuccess"] { background:#052e16 !important; border-left:4px solid var(--green) !important; border-radius:8px !important; }
div[data-testid="stSuccess"] * { color:#86EFAC !important; }
div[data-testid="stInfo"]    { background:#0c1a3a !important; border-left:4px solid #3B82F6 !important; border-radius:8px !important; }
div[data-testid="stInfo"]    * { color:#93C5FD !important; }
div[data-testid="stWarning"] { background:#1c1000 !important; border-left:4px solid var(--amber) !important; border-radius:8px !important; }
div[data-testid="stWarning"] * { color:#FCD34D !important; }
div[data-testid="stError"]   { background:#1a0505 !important; border-left:4px solid var(--red) !important; border-radius:8px !important; }
div[data-testid="stError"]   * { color:#FCA5A5 !important; }

/* ═══ 15. Misc ═══ */
hr { border-color:var(--border) !important; margin:16px 0 !important; }
[data-testid="stDataFrame"], [data-testid="stDataFrame"] th, [data-testid="stDataFrame"] td {
    background:var(--bg2) !important; color:var(--txt) !important;
}
[data-baseweb="tag"] { background:#1a2e1a !important; color:var(--green-hi) !important; }
.stNumberInput button { background:var(--bg3) !important; color:var(--green) !important; border-color:var(--border) !important; }
[data-testid="stSpinner"] p { color:var(--green) !important; }

/* ════════════ CUSTOM COMPONENTS ════════════ */

.login-hero { text-align:center; padding:48px 20px 32px; margin-bottom:4px; }
.login-hero-logo {
    font-family:'Inter',sans-serif !important;
    font-size:4.2rem !important; font-weight:900 !important;
    color:var(--green) !important; letter-spacing:-2px !important;
    line-height:1.05 !important; display:block !important;
    text-shadow:0 0 40px rgba(34,197,94,0.25);
}
.login-hero-urdu {
    font-size:2.1rem !important; color:var(--green-hi) !important;
    font-weight:700 !important; display:block !important;
    margin-top:4px !important; letter-spacing:0 !important;
}
.login-hero-sub {
    font-size:1.08rem !important; color:var(--txt2) !important;
    margin-top:12px !important; display:block !important; font-weight:400 !important;
}

.tip-banner {
    background:linear-gradient(135deg,#052e16,#0f3d1c);
    border:1px solid #16A34A; border-radius:14px;
    padding:18px 22px; margin-bottom:20px;
    font-size:0.96rem; line-height:1.75;
    box-shadow:0 2px 12px rgba(34,197,94,0.12);
}
.tip-banner * { color:#D1FAE5 !important; }
.tip-label {
    font-size:0.68rem; font-weight:700; letter-spacing:0.14em;
    text-transform:uppercase; color:var(--green-hi) !important;
    margin-bottom:6px; display:block;
}

.profile-card {
    background:var(--bg2); border:1px solid var(--border);
    border-left:4px solid var(--green); border-radius:12px;
    padding:16px 22px; margin-bottom:18px;
}
.profile-name { font-size:1.1rem; font-weight:700; color:#F0FFF4 !important; }
.profile-detail { font-size:0.88rem; color:var(--txt2) !important; margin-top:4px; }

.badge-g { background:#052e16; color:#4ADE80 !important; border:1px solid #16A34A; border-radius:6px; padding:3px 12px; font-weight:700; font-size:0.82rem; display:inline-block; }
.badge-a { background:#1c1000; color:#FCD34D !important; border:1px solid #F59E0B; border-radius:6px; padding:3px 12px; font-weight:700; font-size:0.82rem; display:inline-block; }
.badge-r { background:#1a0505; color:#FCA5A5 !important; border:1px solid #EF4444; border-radius:6px; padding:3px 12px; font-weight:700; font-size:0.82rem; display:inline-block; }
.badge-n { background:var(--bg3); color:var(--txt3) !important; border:1px solid var(--border); border-radius:6px; padding:3px 12px; font-weight:700; font-size:0.82rem; display:inline-block; }

.bubble-user {
    background:#1a2e1a; border:1px solid #16A34A; border-radius:16px 16px 4px 16px;
    padding:14px 18px; margin:8px 0; margin-left:10%;
    font-size:0.96rem; line-height:1.75; color:#D1FAE5 !important;
}
.bubble-bot {
    background:var(--bg2); border:1px solid var(--border); border-radius:16px 16px 16px 4px;
    padding:14px 18px; margin:8px 0; margin-right:10%;
    font-size:0.96rem; line-height:1.75; color:var(--txt) !important;
}
.bubble-label { font-size:0.68rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--txt3) !important; margin-bottom:4px; }

.wizard-box {
    background:var(--bg2); border:1px solid var(--border);
    border-top:4px solid var(--green); border-radius:16px;
    padding:28px 32px; margin:0 auto; max-width:580px;
}
.wizard-box h2 { color:var(--green) !important; margin-bottom:6px; }
.wizard-box p  { color:var(--txt2) !important; margin-bottom:0; }
.step-pill {
    background:#052e16; color:var(--green-hi) !important;
    border:1px solid #16A34A; border-radius:20px;
    padding:4px 14px; font-size:0.75rem; font-weight:700;
    display:inline-block; margin-bottom:14px; letter-spacing:0.04em;
}

.feature-card {
    background:var(--bg2); border:1px solid var(--border); border-radius:14px;
    padding:24px 26px; height:100%;
}
.feature-card p { color:var(--txt) !important; font-size:0.96rem !important; margin:8px 0 !important; }
.feature-card .disc { color:var(--txt3) !important; font-size:0.83rem !important; }

.sb-disc {
    background:#110e00; border:1px solid #3a2800;
    border-left:3px solid var(--amber);
    border-radius:8px; padding:12px 14px; margin-top:2px;
}
.sb-disc p { color:var(--txt2) !important; font-size:0.78rem !important; line-height:1.65 !important; margin:2px 0 !important; text-transform:none !important; letter-spacing:0 !important; }
.sb-disc strong { color:#FCD34D !important; }
.sb-disc-title { font-size:0.82rem !important; font-weight:700 !important; color:var(--amber) !important; margin-bottom:6px !important; }

.meal-slot { font-size:0.82rem; font-weight:700; color:var(--green) !important; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:2px; }
.section-label {
    font-size:0.72rem; font-weight:700; color:var(--txt3) !important;
    text-transform:uppercase; letter-spacing:0.1em;
    border-bottom:1px solid var(--border); padding-bottom:6px; margin-bottom:14px;
}

.footer { font-size:0.78rem; color:var(--txt3) !important; text-align:center; padding:12px 0; border-top:1px solid var(--border); margin-top:32px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
ss = st.session_state

def normalize_phone(p): return re.sub(r"[^\d+]", "", p.strip())
def user_key_from_phone(p):
    salt = os.getenv("PHONE_SALT", "dev-salt-change-me")
    return hashlib.sha256((salt + p).encode()).hexdigest()
def last4(p):
    d = re.sub(r"\D", "", p)
    return d[-4:] if len(d) >= 4 else d

def _lang():  return ss.get("lang", "en")
def t(k):     return T[_lang()].get(k, T["en"].get(k, k))
def _get_user():     return ss.get("user_key", "").strip()
def _triage_level(): return ss.get("triage_level")
def _blocked():      return _triage_level() == "RED"
def _parse_fastings(v): return [x for x in v if x and x > 0]

def _lang_toggle(suffix=""):
    lbl = "🌐 اردو" if _lang() == "en" else "🌐 English"
    if st.button(lbl, key=f"lt_{suffix}_{ss.get('_lc',0)}"):
        ss["lang"] = "ur" if _lang() == "en" else "en"
        ss["_lc"]  = ss.get("_lc", 0) + 1
        ss["current_tip"] = get_tip(_lang())
        st.rerun()

def _profile_context():
    p = []
    for k, v in [("name",ss.get("name")), ("age",ss.get("age")),
                 ("diabetes_type",ss.get("diabetes_type"))]:
        if v: p.append(f"{k}: {v}")
    if ss.get("has_hypertension"):     p.append("hypertension")
    if ss.get("has_high_cholesterol"): p.append("high cholesterol")
    if ss.get("triage_level"):         p.append(f"triage: {ss['triage_level']}")
    plan = ss.get("week_plan")
    if plan:
        days  = plan.get("days", []) if isinstance(plan, dict) else plan
        slots = plan.get("slots", ["breakfast","lunch","dinner"]) if isinstance(plan, dict) else ["breakfast","lunch","dinner"]
        if days:
            d1 = days[0]
            p.append("today: " + ", ".join(f"{s}={d1[s]['name']}" for s in slots if s in d1))
    return " | ".join(p)

def _run_triage(dtype, hy, ch, bp_sys=None, bp_dia=None, a1c=None,
                fasting_readings=None, total_chol=None, other_major=False):
    lv, fl = triage_profile(
        diabetes_type=dtype, has_hypertension=hy, has_high_cholesterol=ch,
        bp_sys=bp_sys, bp_dia=bp_dia, a1c=a1c,
        fasting_readings=fasting_readings or [],
        total_cholesterol=total_chol, other_major_conditions=other_major)
    ss["triage_level"] = lv; ss["triage_flags"] = fl
    return lv, fl

def _plan_days():
    p = ss.get("week_plan")
    return p.get("days", []) if isinstance(p, dict) else (p or [])
def _plan_slots():
    p = ss.get("week_plan")
    return p.get("slots", ["breakfast","lunch","dinner","snack"]) if isinstance(p, dict) else ["breakfast","lunch","dinner","snack"]
def _plan_profile():
    p = ss.get("week_plan")
    return p.get("profile") if isinstance(p, dict) else None

SLOT_CFG = {
    "breakfast": ("🌅","Breakfast","ناشتہ"),
    "snack_am":  ("🍎","Mid-Morning Snack","دوپہر سے پہلے کا ناشتہ"),
    "lunch":     ("☀️","Lunch","دوپہر کا کھانا"),
    "snack_pm":  ("🍊","Afternoon Snack","شام کا ناشتہ"),
    "dinner":    ("🌙","Dinner","رات کا کھانا"),
    "snack_bed": ("🌛","Bedtime Snack","سونے سے پہلے کا ناشتہ"),
    "snack":     ("🍎","Snack","ناشتہ"),
}


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def _sidebar():
    pass


def _sidebar():
    with st.sidebar:
        _lang_toggle("sb")
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.markdown(f"## 🩺 {t('app_title')}")
        st.caption(t("app_subtitle"))

        if _get_user():
            name = ss.get("name") or ss.get("display_name","")
            st.success(f"**{t('hi_user')}**, {name}!")
            lv = _triage_level()
            if lv:
                cls = {"GREEN":"badge-g","AMBER":"badge-a","RED":"badge-r"}.get(lv,"badge-n")
                lbl = {"GREEN":t("status_green"),"AMBER":t("status_amber"),"RED":t("status_red")}.get(lv,"")
                st.markdown(f'<span class="{cls}">{lbl}</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-n">⬤ Not assessed</span>', unsafe_allow_html=True)
            st.divider()
            if st.button(t("logout_btn"), use_container_width=True):
                ss["_confirm_logout"] = True
            if ss.get("_confirm_logout"):
                st.warning(t("logout_confirm"))
                c1, c2 = st.columns(2)
                if c1.button(t("yes"), key="ly"): [ss.__delitem__(k) for k in list(ss)]; st.rerun()
                if c2.button(t("no"),  key="ln"): ss["_confirm_logout"] = False; st.rerun()

        st.divider()
        lang = _lang()
        if lang == "en":
            st.markdown("""
<div class="sb-disc">
<p class="sb-disc-title">⚠️ Medical Disclaimer</p>
<p>For information only — not medical advice.</p>
<p>• Does not diagnose or prescribe</p>
<p>• Does not replace your doctor</p>
<p>• Glucose above <strong>180 mg/dL</strong> repeatedly? See your doctor</p>
<p>• <strong>Low sugar signs:</strong> shakiness, sweating, dizziness → get help immediately</p>
<p>• Emergency? Call emergency services now</p>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div class="sb-disc">
<p class="sb-disc-title">⚠️ طبی وضاحت</p>
<p>صرف معلومات — طبی مشورہ نہیں۔</p>
<p>• تشخیص یا دوائی تجویز نہیں کرتی</p>
<p>• ڈاکٹر کی جگہ نہیں لیتی</p>
<p>• شوگر <strong>180 mg/dL</strong> سے بار بار اوپر؟ ڈاکٹر سے ملیں</p>
<p>• ہنگامی صورت میں ایمرجنسی کو کال کریں</p>
</div>""", unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.caption(t("version"))

_sidebar()


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if "user_key" not in ss:
    h1, h2 = st.columns([5, 1])
    with h2: _lang_toggle("entry")

    lang = _lang()
    st.markdown(
        f'<div class="login-hero">'
        f'<span class="login-hero-logo">🩺 Apni Sehat</span>'
        f'<span class="login-hero-urdu">اپنی صحت</span>'
        f'<span class="login-hero-sub">{"Your personal diabetes health companion" if lang=="en" else "آپ کا ذاتی ذیابیطس صحت ساتھی"}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown(f'<div class="section-label">{"Your details" if lang=="en" else "آپ کی تفصیلات"}</div>', unsafe_allow_html=True)
        name  = st.text_input(t("entry_name"),  placeholder=t("entry_name_hint"), label_visibility="collapsed")
        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
        phone = st.text_input(t("entry_phone"), placeholder=t("entry_phone_ph"),  label_visibility="collapsed")
        st.caption(t("entry_phone_hint"))
        st.caption(t("entry_privacy"))
        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        go_col, _ = st.columns([1, 2])
        with go_col:
            go = st.button(t("entry_btn"), type="primary", use_container_width=True)

        if go:
            pn = normalize_phone(phone)
            if not name.strip(): st.error(t("name_error")); st.stop()
            if not pn.startswith("+") or len(pn) < 8: st.error(t("phone_error")); st.stop()

            with st.spinner(t("finding_plan")):
                uk = user_key_from_phone(pn)
                ss["user_key"]     = uk
                ss["display_name"] = name.strip()
                ss["phone_last4"]  = last4(pn)
                try:    prof = get_profile(uk)
                except: st.error(t("db_error")); st.stop()

                if prof and prof.get("age"):
                    ss.update({
                        "name": prof.get("full_name") or name.strip(),
                        "age": prof.get("age", 30),
                        "gender": prof.get("gender", "Prefer not to say"),
                        "height_cm": prof.get("height_cm", 0),
                        "weight_kg": prof.get("weight_kg", 0.0),
                        "family_history": prof.get("family_history", []),
                        "diabetes_type": prof.get("diabetes_type", "Type 2"),
                        "has_hypertension": bool(prof.get("has_hypertension", 0)),
                        "has_high_cholesterol": bool(prof.get("has_high_cholesterol", 0)),
                        "phone_last4": prof.get("phone_last4", last4(pn)),
                        "prefer_desi": True, "veg_only": False,
                        "profile_complete": True, "setup_step": "done",
                        "on_insulin": False, "hypo_episodes": False, "weakness_between": False,
                    })
                    h = prof.get("height_cm") or 0
                    w = prof.get("weight_kg") or 0
                    if h > 0 and w > 0:
                        ss["bmi"] = w / ((h / 100) ** 2)
                    _run_triage(
                        ss.get("diabetes_type", "Type 2"),
                        ss.get("has_hypertension", False),
                        ss.get("has_high_cholesterol", False),
                    )
                    st.success(f"{t('welcome_back')}, {ss['name']}! 👋")
                else:
                    upsert_profile(uk, {"full_name": name.strip(), "phone_last4": last4(pn), "family_history": []})
                    ss.update({"name": name.strip(), "profile_complete": False, "setup_step": 1,
                               "prefer_desi": True, "veg_only": False})
                    st.info(t("new_user_found"))
            st.rerun()

    with right:
        feats = [
            ("✅","Bilingual health chatbot — English & Urdu" if lang=="en" else "اردو اور انگریزی میں صحت کا مددگار"),
            ("🥗","Personalised 7-day desi meal plan"         if lang=="en" else "ذاتی 7 دن کا دیسی کھانے کا منصوبہ"),
            ("📊","Blood sugar tracker with trend chart"       if lang=="en" else "بلڈ شوگر ٹریکر"),
            ("💡","AI food swap suggestions"                   if lang=="en" else "AI سے کھانے کی تجاویز"),
        ]
        rows = "".join(f'<p><span style="margin-right:10px;">{i}</span>{txt}</p>' for i,txt in feats)
        disc = ("This app supports healthy habits — it does <strong>not</strong> replace your doctor."
                if lang=="en" else
                "یہ ایپ صحت مند عادات میں مدد کرتی ہے — آپ کے <strong>ڈاکٹر کی جگہ نہیں لیتی</strong>۔")
        st.markdown(
            f'<div class="feature-card">'
            f'<div class="section-label">{"What you get" if lang=="en" else "کیا ملتا ہے"}</div>'
            f'{rows}'
            f'<hr style="border:none;border-top:1px solid #2A3147;margin:16px 0 12px;">'
            f'<p class="disc">⚠️ {disc}</p></div>',
            unsafe_allow_html=True,
        )
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  WIZARD
# ══════════════════════════════════════════════════════════════════════════════
if ss.get("setup_step") in (1, 2):
    step = ss["setup_step"]
    wl, wr = st.columns([5,1])
    with wr: _lang_toggle("wiz")
    st.markdown(f"# 🩺 {t('app_title')}")

    _, mid, _ = st.columns([1,3,1])
    with mid:
        heading = t("wizard_step1_heading") if step==1 else t("wizard_step2_heading")
        caption = t("wizard_step1_caption") if step==1 else t("wizard_step2_caption")
        st.markdown(
            f'<div class="wizard-box">'
            f'<span class="step-pill">Step {"1" if step==1 else "2"} / 2</span>'
            f'<h2>{heading}</h2><p>{caption}</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        if step == 1:
            name_v  = st.text_input(t("wizard_name"), value=ss.get("name",""))
            age_v   = st.number_input(t("wizard_age"), 1, 110, int(ss.get("age",50)))
            d_disp  = t("wizard_diabetes_opts"); d_en = T["en"]["wizard_diabetes_opts"]
            saved   = ss.get("diabetes_type","Type 2")
            d_idx   = d_en.index(saved) if saved in d_en else 0
            dtype_d = st.selectbox(t("wizard_diabetes"), d_disp, index=d_idx)
            pref    = st.checkbox(t("wizard_desi"), value=ss.get("prefer_desi",True))
            veg     = st.checkbox(t("wizard_veg"),  value=ss.get("veg_only",False))
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            nc, _ = st.columns([1,2])
            with nc:
                if st.button(t("wizard_next"), type="primary", use_container_width=True):
                    if not name_v.strip(): st.error(t("name_error")); st.stop()
                    dn = d_en[d_disp.index(dtype_d)]
                    ss.update({"name":name_v.strip(),"age":int(age_v),"diabetes_type":dn,
                               "prefer_desi":pref,"veg_only":veg,"setup_step":2})
                    st.rerun()
        else:
            hy    = st.checkbox(t("wizard_hypert"), value=ss.get("has_hypertension",False))
            ch    = st.checkbox(t("wizard_chol"),   value=ss.get("has_high_cholesterol",False))
            other = st.checkbox(t("wizard_other"))
            st.divider()
            st.markdown(f"**{'Meal frequency questions' if _lang()=='en' else 'کھانے کی تعداد کے سوالات'}**")
            ins  = st.checkbox(t("q_insulin"),  value=ss.get("on_insulin",False),       help=t("q_insulin_help"))
            hypo = st.checkbox(t("q_hypo"),     value=ss.get("hypo_episodes",False),    help=t("q_hypo_help"))
            wkn  = st.checkbox(t("q_weakness"), value=ss.get("weakness_between",False), help=t("q_weakness_help"))
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            bc, fc, _ = st.columns([1,1,1])
            with bc:
                if st.button(t("wizard_back"), use_container_width=True):
                    ss["setup_step"] = 1; st.rerun()
            with fc:
                if st.button(t("wizard_finish"), type="primary", use_container_width=True):
                    with st.spinner(t("wizard_saving")):
                        ss.update({"has_hypertension":hy,"has_high_cholesterol":ch,
                                   "on_insulin":ins,"hypo_episodes":hypo,"weakness_between":wkn,
                                   "gender":"Prefer not to say","height_cm":0,"weight_kg":0.0,
                                   "family_history":[],"bmi":None})
                        _run_triage(ss["diabetes_type"],hy,ch,other_major=other)
                        upsert_profile(ss["user_key"],{
                            "full_name":ss["name"],"phone_last4":ss.get("phone_last4"),
                            "age":ss["age"],"gender":"Prefer not to say",
                            "diabetes_type":ss["diabetes_type"],
                            "has_hypertension":1 if hy else 0,
                            "has_high_cholesterol":1 if ch else 0,"family_history":[],
                        })
                        ss["week_plan"] = generate_week_plan(
                            prefer_desi=ss.get("prefer_desi",True),
                            veg_only=ss.get("veg_only",False),
                            has_hypertension=hy,has_high_cholesterol=ch,
                            on_insulin=ins,hypo_episodes=hypo,weakness_between=wkn,
                            bmi=ss.get("bmi"),diabetes_type=ss["diabetes_type"])
                        ss["profile_complete"] = True; ss["setup_step"] = "done"
                    st.success(t("wizard_done_msg")); st.rerun()
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
if "current_tip"     not in ss: ss["current_tip"]     = get_tip(_lang())
if "chat_history"    not in ss: ss["chat_history"]    = []
if "editing_profile" not in ss: ss["editing_profile"] = False

tl, tr = st.columns([6,1])
with tr: _lang_toggle("main")

if not ss.get("week_plan"):
    with st.spinner(t("loading_plan")):
        ss["week_plan"] = generate_week_plan(
            prefer_desi=ss.get("prefer_desi",True), veg_only=ss.get("veg_only",False),
            has_hypertension=ss.get("has_hypertension",False),
            has_high_cholesterol=ss.get("has_high_cholesterol",False),
            on_insulin=ss.get("on_insulin",False), hypo_episodes=ss.get("hypo_episodes",False),
            weakness_between=ss.get("weakness_between",False),
            bmi=ss.get("bmi"), diabetes_type=ss.get("diabetes_type","Type 2"))


# Late CSS injection — appears after Streamlit's own styles in DOM, guaranteed to win
st.markdown("""
<style>
/* Late override — CSS layer */
html body .material-symbols-rounded,
html body span.material-symbols-rounded,
button span.material-symbols-rounded {
    font-size: 0 !important;
    width: 0 !important;
    max-width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    opacity: 0 !important;
    visibility: hidden !important;
    color: transparent !important;
    display: inline-block !important;
    padding: 0 !important;
    margin: 0 !important;
}
[data-testid="stExpanderToggleIcon"],
[data-testid="stExpanderToggleIcon"] * {
    font-size: 0 !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    opacity: 0 !important;
    position: absolute !important;
    color: transparent !important;
}
/* Day accordion full-width header button */
.day-acc-row .stButton > button {
    width: 100% !important;
    text-align: left !important;
    justify-content: flex-start !important;
    color: var(--txt) !important;
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    letter-spacing: 0 !important;
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 4px !important;
}
.day-acc-row .stButton > button:hover {
    background: #1a2030 !important;
    border-color: var(--green) !important;
    color: var(--txt) !important;
}
</style>
<script>
// JS is the only reliable way to kill Material Icons ligature text in sidebar buttons.
// CSS font-size:0 loses when Streamlit sets inline styles; JS wins unconditionally.
(function hideMaterialIcons() {
    function kill() {
        document.querySelectorAll(
            '.material-symbols-rounded, [data-testid="stExpanderToggleIcon"]'
        ).forEach(function(el) {
            el.style.setProperty('font-size',   '0',       'important');
            el.style.setProperty('width',       '0',       'important');
            el.style.setProperty('max-width',   '0',       'important');
            el.style.setProperty('height',      '0',       'important');
            el.style.setProperty('overflow',    'hidden',  'important');
            el.style.setProperty('opacity',     '0',       'important');
            el.style.setProperty('visibility',  'hidden',  'important');
            el.style.setProperty('color',       'transparent', 'important');
            el.style.setProperty('padding',     '0',       'important');
            el.style.setProperty('margin',      '0',       'important');
            el.style.setProperty('line-height', '0',       'important');
        });
    }
    kill();
    // Watch for Streamlit dynamically inserting new elements (sidebar toggle, etc.)
    var obs = new MutationObserver(kill);
    obs.observe(document.documentElement, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)

tabs = st.tabs([t("tab_plan"), t("tab_chat"), t("tab_glucose"), t("tab_dashboard")])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 0 — MY PLAN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    lv       = _triage_level()
    bcls     = {"GREEN":"badge-g","AMBER":"badge-a","RED":"badge-r"}.get(lv or "","badge-n")
    blbl     = {"GREEN":t("status_green"),"AMBER":t("status_amber"),"RED":t("status_red")}.get(lv or "",t("status_none"))
    conds    = ([("Hypertension" if _lang()=="en" else "ہائی بلڈ پریشر")] if ss.get("has_hypertension") else []) + \
               ([("High Cholesterol" if _lang()=="en" else "زیادہ کولیسٹرول")] if ss.get("has_high_cholesterol") else [])
    cond_str = ", ".join(conds) if conds else t("no_conditions")
    name_d   = ss.get("name", ss.get("display_name",""))
    age_d    = ss.get("age","")
    dtype_d  = ss.get("diabetes_type","")

    pc1, pc2 = st.columns([5,1])
    with pc1:
        st.markdown(
            f'<div class="profile-card">'
            f'<div class="profile-name">👤 {name_d}' + (f', {age_d}' if age_d else '') + '</div>'
            f'<div class="profile-detail">' + (f'{dtype_d} · ' if dtype_d else '') + f'{cond_str}</div>'
            f'<div style="margin-top:10px;"><span class="{bcls}">{blbl}</span></div>'
            f'</div>', unsafe_allow_html=True)
    with pc2:
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        if st.button(t("edit_profile_btn"), use_container_width=True):
            ss["editing_profile"] = not ss.get("editing_profile",False); st.rerun()

    if ss.get("editing_profile"):
        if True:  # was st.expander — removed to fix Material Icons icon bug
            ef1, ef2 = st.columns(2)
            with ef1:
                en  = st.text_input(t("pf_name"), value=ss.get("name",""), key="e_name")
                ea  = st.number_input(t("pf_age"), 1, 110, int(ss.get("age",50) or 50), key="e_age")
            with ef2:
                go  = t("pf_gender_opts"); ge = T["en"]["pf_gender_opts"]
                gs  = ss.get("gender","Prefer not to say"); gi = ge.index(gs) if gs in ge else 0
                egn = st.selectbox(t("pf_gender"), go, index=gi, key="e_gender")
                do  = t("pf_diabetes_opts"); de = T["en"]["pf_diabetes_opts"]
                ds  = ss.get("diabetes_type","Type 2"); di = de.index(ds) if ds in de else 0
                edt = st.selectbox(t("pf_diabetes"), do, index=di, key="e_dtype")

            ef3, ef4 = st.columns(2)
            with ef3: eh = st.number_input(t("pf_height"), 0, 250, int(ss.get("height_cm",0) or 0), key="e_h")
            with ef4: ew = st.number_input(t("pf_weight"), 0.0, 400.0, float(ss.get("weight_kg",0.0) or 0.0), 0.5, key="e_w")
            eb = None
            if eh > 0 and ew > 0:
                eb = ew/((eh/100)**2); st.caption(f"{t('pf_bmi')}: **{eb:.1f}** {t('pf_bmi_note')}")

            efam = st.multiselect(t("pf_family"), T["en"]["pf_family_opts"], default=ss.get("family_history",[]), key="e_fam")
            ec1, ec2, ec3 = st.columns(3)
            with ec1: ehy = st.checkbox(t("pf_hypert"), value=ss.get("has_hypertension",False),    key="e_hy")
            with ec2: ech = st.checkbox(t("pf_chol"),   value=ss.get("has_high_cholesterol",False), key="e_ch")
            with ec3: eot = st.checkbox(t("pf_other"),  key="e_ot")

            st.divider()
            st.markdown(f"**{'Meal frequency' if _lang()=='en' else 'کھانے کی تعداد'}**")
            ef_1, ef_2, ef_3 = st.columns(3)
            with ef_1: eins = st.checkbox(t("q_insulin"),  value=ss.get("on_insulin",False),       key="e_ins",help=t("q_insulin_help"))
            with ef_2: ehyp = st.checkbox(t("q_hypo"),     value=ss.get("hypo_episodes",False),    key="e_hyp",help=t("q_hypo_help"))
            with ef_3: ewkn = st.checkbox(t("q_weakness"), value=ss.get("weakness_between",False), key="e_wkn",help=t("q_weakness_help"))

            adv_key = "show_adv_" + str(ss.get("user_key",""))[:8]
            if adv_key not in ss: ss[adv_key] = False
            if st.button("➕ " + ("Add recent test results (optional)" if _lang()=="en" else "حالیہ ٹیسٹ کے نتائج شامل کریں"), key="adv_tog", use_container_width=False):
                ss[adv_key] = not ss[adv_key]; st.rerun()
            if ss.get(adv_key, False):
                st.caption(t("pf_advanced_note"))
                a1,a2,a3 = st.columns(3)
                with a1:
                    ebps = st.number_input(t("pf_bp_sys"),0,300,130 if ehy else 0,key="e_bps")
                    ebpd = st.number_input(t("pf_bp_dia"),0,200,80  if ehy else 0,key="e_bpd")
                with a2: ea1c = st.number_input(t("pf_a1c"),0.0,20.0,0.0,0.1,key="e_a1c")
                with a3: etc  = st.number_input(t("pf_chol_val"),0.0,600.0,0.0,1.0,key="e_tc")
                st.markdown(f"**{t('pf_fasting_head')}**"); st.caption(t("pf_fasting_note"))
                f1c,f2c,f3c = st.columns(3)
                with f1c: ef1 = st.number_input(t("pf_day3"),0.0,600.0,0.0,1.0,key="e_f1")
                with f2c: ef2 = st.number_input(t("pf_day2"),0.0,600.0,0.0,1.0,key="e_f2")
                with f3c: ef3 = st.number_input(t("pf_day1"),0.0,600.0,0.0,1.0,key="e_f3")

            sv_c, _ = st.columns([1,2])
            with sv_c:
                if st.button(t("save_profile_btn"), type="primary", use_container_width=True, key="sp"):
                    with st.spinner(t("saving_profile")):
                        gn = T["en"]["pf_gender_opts"][T[_lang()]["pf_gender_opts"].index(egn)]
                        dn = T["en"]["pf_diabetes_opts"][T[_lang()]["pf_diabetes_opts"].index(edt)]
                        ss.update({"name":en.strip(),"age":int(ea),"gender":gn,"diabetes_type":dn,
                                   "height_cm":int(eh),"weight_kg":float(ew),"family_history":efam,
                                   "bmi":eb,"has_hypertension":ehy,"has_high_cholesterol":ech,
                                   "on_insulin":eins,"hypo_episodes":ehyp,"weakness_between":ewkn})
                        _run_triage(dn,ehy,ech,
                                    bp_sys=float(ebps) if ebps>0 else None,
                                    bp_dia=float(ebpd) if ebpd>0 else None,
                                    a1c=float(ea1c) if ea1c>0 else None,
                                    fasting_readings=_parse_fastings([ef1,ef2,ef3]),
                                    total_chol=float(etc) if etc>0 else None, other_major=eot)
                        upsert_profile(ss["user_key"],{
                            "full_name":en.strip(),"phone_last4":ss.get("phone_last4"),
                            "age":int(ea),"gender":gn,
                            "height_cm":int(eh) if eh else None,"weight_kg":float(ew) if ew else None,
                            "family_history":efam,"diabetes_type":dn,
                            "has_hypertension":1 if ehy else 0,"has_high_cholesterol":1 if ech else 0})
                        ss["week_plan"] = generate_week_plan(
                            prefer_desi=ss.get("prefer_desi",True), veg_only=ss.get("veg_only",False),
                            has_hypertension=ehy, has_high_cholesterol=ech,
                            on_insulin=eins, hypo_episodes=ehyp, weakness_between=ewkn,
                            bmi=eb, diabetes_type=dn)
                        ss["editing_profile"] = False
                    st.success(t("profile_saved")); st.rerun()

            if ss.get("triage_level"):
                lv2 = ss["triage_level"]
                if lv2=="GREEN": st.success(t("green_result"))
                elif lv2=="AMBER": st.warning(t("amber_result"))
                else: st.error(t("red_result"))
                for f in ss.get("triage_flags",[]): st.write("•", f)

    st.divider()

    tc, tb = st.columns([5,1])
    with tc:
        st.markdown(
            f'<div class="tip-banner"><span class="tip-label">{t("tip_title")}</span>{ss["current_tip"]}</div>',
            unsafe_allow_html=True)
    with tb:
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        if st.button(t("tip_new"), use_container_width=True, key="new_tip"):
            ss["current_tip"] = get_tip(_lang()); st.rerun()

    pp = _plan_profile()
    if pp:
        lg = _lang()
        reason  = pp.get("reason_en"  if lg=="en" else "reason_ur","")
        label   = pp.get("label_en"   if lg=="en" else "label_ur","")
        portion = pp.get("portion_note_en" if lg=="en" else "portion_note_ur","")
        if reason: st.info(f"**{t('meal_structure')}: {label}**\n\n{reason}" + (f"\n\n📏 {portion}" if portion else ""))
    if ss.get("on_insulin"):    st.warning(t("insulin_reminder"))
    if ss.get("hypo_episodes"): st.warning(t("hypo_reminder"))

    st.markdown(f"## 🥗 {t('plan_heading')}")
    if _blocked():
        st.error(t("plan_blocked"))
    else:
        tc1, tc2, tc3 = st.columns([2,2,2])
        with tc1: prefer_desi = st.toggle(t("desi_toggle"), value=ss.get("prefer_desi",True), key="pd_tog")
        with tc2: veg_only    = st.toggle(t("veg_toggle"),  value=ss.get("veg_only",False),   key="vo_tog")
        with tc3:
            if st.button(t("regen_btn")):
                with st.spinner(t("building_plan")):
                    ss["week_plan"] = generate_week_plan(
                        prefer_desi=prefer_desi, veg_only=veg_only,
                        has_hypertension=ss.get("has_hypertension",False),
                        has_high_cholesterol=ss.get("has_high_cholesterol",False),
                        on_insulin=ss.get("on_insulin",False),
                        hypo_episodes=ss.get("hypo_episodes",False),
                        weakness_between=ss.get("weakness_between",False),
                        bmi=ss.get("bmi"), diabetes_type=ss.get("diabetes_type","Type 2"))
                ss["prefer_desi"] = prefer_desi; ss["veg_only"] = veg_only; st.rerun()
        ss["prefer_desi"] = prefer_desi; ss["veg_only"] = veg_only

        days  = _plan_days(); slots = _plan_slots(); lg = _lang()
        # Manual accordion — no st.expander() so no Material Icons fallback text
        if "open_days" not in ss:
            ss["open_days"] = set()

        for day in days:
            day_carbs = sum(day[s]["carb_servings"]*CARB["carb_serving_grams"] for s in slots if s in day)
            day_num   = day["day"]
            is_open   = day_num in ss["open_days"]
            day_label = (f"Day {day_num}  ·  ~{day_carbs:.0f}g {t('carbs_label')}"
                         if _lang()=="en" else
                         f"دن {day_num}  ·  ~{day_carbs:.0f}g {t('carbs_label')}")

            # ── Single full-width button accordion ──────────────────────────────────
            # on_click callback updates state BEFORE the natural Streamlit rerun.
            # No explicit st.rerun() needed — avoids the double-rerender that made
            # the accordion feel slow.
            arrow = "▲" if is_open else "▽"
            btn_label = f"📅  {day_label}    {arrow}"

            def _toggle_day(dn=day_num):
                if dn in ss["open_days"]:
                    ss["open_days"].discard(dn)
                else:
                    ss["open_days"].add(dn)

            st.markdown('<div class="day-acc-row">', unsafe_allow_html=True)
            st.button(
                btn_label,
                key=f"day_tog_{day_num}",
                use_container_width=True,
                on_click=_toggle_day,
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Content — only shown when open
            if is_open:
                with st.container():
                    st.markdown(
                        '<div style="background:var(--bg2);border:1px solid var(--border);'
                        'border-top:none;border-radius:0 0 10px 10px;padding:14px 18px;'
                        'margin-top:-6px;margin-bottom:10px;">',
                        unsafe_allow_html=True)
                    for slot in slots:
                        if slot not in day: continue
                        meal = day[slot]
                        ico, le, lu = SLOT_CFG.get(slot,("🍽️",slot.title(),slot.title()))
                        lbl = le if lg=="en" else lu
                        cg  = meal["carb_servings"] * CARB["carb_serving_grams"]
                        st.markdown(f'<p class="meal-slot">{ico} {lbl}</p>', unsafe_allow_html=True)
                        st.markdown(f"**{meal['name']}**")
                        st.caption(f"~{cg}g carbs · {meal['notes']}")
                        st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    sw_c, _ = st.columns([1,3])
                    with sw_c:
                        if st.button(t("swaps_btn"), key=f"sw_{day_num}", use_container_width=True):
                            names = [day[s]["name"] for s in slots if s in day]
                            with st.spinner(t("getting_swaps")):
                                swaps = generate_swaps("; ".join(names))
                            st.markdown(f"**{t('swaps_heading')}**")
                            for s in swaps: st.write("•", s)
            else:
                st.markdown('<div style="margin-bottom:4px;"></div>', unsafe_allow_html=True)


    st.divider()

    st.markdown(f"### {t('checkin_heading')}")
    user = _get_user()
    if not _blocked():
        ci_date  = st.date_input(t("checkin_date"), value=date.today(), key="ci_date")
        followed = st.radio(t("followed_q"), [t("yes_opt"), t("no_opt")], horizontal=True, key="ci_rad")
        if followed == t("yes_opt"):
            cb, _ = st.columns([1,3])
            with cb:
                if st.button(t("save_ci_btn"), type="primary", use_container_width=True, key="ci_yes"):
                    add_daily_checkin(user, ci_date, followed_plan=True, actual_meals="")
                    st.success(t("ci_saved")); st.balloons()
        else:
            actual = st.text_area(t("ate_label"), placeholder=t("ate_ph"), height=100, key="ci_ate")
            sb, _ = st.columns([1,3])
            with sb:
                if st.button(t("save_suggest_btn"), type="primary", use_container_width=True, key="ci_no"):
                    if not actual.strip(): st.warning(t("describe_ate"))
                    else:
                        with st.spinner(t("saving_suggest")):
                            add_daily_checkin(user, ci_date, followed_plan=False, actual_meals=actual.strip())
                            tips = coach_on_actual_meal(actual.strip())
                        st.success(t("suggest_saved"))
                        for tip in tips: st.write("•", tip)
                        st.caption(t("suggest_note"))

    st.markdown(f'<div class="footer">⚠️ {APP["disclaimer"]}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — CHAT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown(f"## 💬 {t('chat_heading')}")
    st.caption(t("chat_caption"))
    st.divider()

    if not ss["chat_history"]:
        st.markdown(
            f'<div class="bubble-bot"><div class="bubble-label">🩺 Sehat Saathi / صحت ساتھی</div>'
            f'{t("chat_greeting_en").replace(chr(10),"<br>")}</div>',
            unsafe_allow_html=True)

    uname = ss.get("name", ss.get("display_name","You"))
    for msg in ss["chat_history"]:
        content = msg["content"].replace("\n","<br>")
        if msg["role"] == "user":
            st.markdown(f'<div class="bubble-user"><div class="bubble-label">👤 {uname}</div>{content}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-bot"><div class="bubble-label">🩺 Sehat Saathi</div>{content}</div>',unsafe_allow_html=True)

    user_input = st.chat_input(t("chat_placeholder"))
    if user_input:
        ss["chat_history"].append({"role":"user","content":user_input})
        with st.spinner(t("chat_thinking")):
            reply = chat_with_assistant(ss["chat_history"], lang=_lang(), user_profile=_profile_context())
        ss["chat_history"].append({"role":"assistant","content":reply})
        st.rerun()

    if ss["chat_history"]:
        cl, _ = st.columns([1,4])
        with cl:
            if st.button(t("chat_clear"), key="clr_chat", use_container_width=True):
                ss["chat_history"] = []; st.rerun()

    st.caption(t("chat_note"))


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — LOG SUGAR
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown(f"## 📊 {t('glucose_heading')}")
    user = _get_user()
    if _blocked():
        st.error(t("blocked_msg"))
    else:
        c1, c2 = st.columns(2)
        with c1:
            r_type    = st.selectbox(t("reading_lbl"), t("reading_types"))
            m_date    = st.date_input(t("date_lbl"), value=date.today())
            m_time    = st.time_input(t("time_lbl"), value=datetime.now().time())
        with c2:
            value     = st.number_input(t("value_lbl"), 0.0, 600.0, 110.0, 1.0)
            meal_note = st.text_input(t("note_lbl"), placeholder=t("note_ph"))
            st.caption(t("ref_ranges").format(h=TRIAGE["hypo"], vh=TRIAGE["very_high"]))
            if value >= TRIAGE["very_high"]:   st.error(t("very_high_alert"))
            elif 0 < value < TRIAGE["hypo"]:   st.warning(t("low_alert"))

        sb, _ = st.columns([1,3])
        with sb:
            if st.button("Save Reading" if _lang()=="en" else "ریڈنگ محفوظ کریں",
                         type="primary", use_container_width=True):
                with st.spinner(t("saving_reading")):
                    add_glucose_log(user, datetime.combine(m_date, m_time), r_type, value, meal_note)
                st.success(t("reading_saved"))

    st.markdown(f'<div class="footer">⚠️ {APP["disclaimer"]}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — PROGRESS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown(f"## 📈 {t('dash_heading')}")
    st.caption(t("dash_caption"))
    user = _get_user()
    c1, c2 = st.columns(2); rows = None

    with c1:
        st.markdown(f"### {t('adh_section')}")
        checkins = fetch_checkins(user)
        if checkins:
            cdf = pd.DataFrame(checkins, columns=["date","followed_plan","actual_meals"])
            cdf["date"] = pd.to_datetime(cdf["date"]).dt.date
            adh = (cdf["followed_plan"].sum()/len(cdf))*100
            st.metric(t("adh_metric"), f"{adh:.0f}%", delta=t("adh_delta").format(n=len(cdf)))
            st.dataframe(cdf[["date","followed_plan"]].rename(
                columns={"date":t("col_date"),"followed_plan":t("col_fol")}), use_container_width=True)
        else: st.info(t("no_checkins"))

    with c2:
        st.markdown(f"### {t('gluc_section')}")
        rows = fetch_glucose_logs(user)
        if rows:
            df = pd.DataFrame(rows, columns=["measured_at","type","value","meal_note"])
            df["measured_at"] = pd.to_datetime(df["measured_at"])
            avg=df["value"].mean(); std=df["value"].std()
            hc=int((df["value"]>=TRIAGE["very_high"]).sum()); lc=int((df["value"]<TRIAGE["hypo"]).sum())
            m1,m2,m3 = st.columns(3)
            m1.metric(t("avg_lbl"), f"{avg:.0f} mg/dL")
            m2.metric(t("var_lbl"), f"±{std:.0f}")
            m3.metric(t("total_lbl"), len(df))
            if hc: st.warning(t("high_alert_d").format(n=hc))
            if lc: st.warning(t("low_alert_d").format(n=lc))
        else: st.info(t("no_glucose"))

    if rows:
        st.markdown(f"### {t('trend_head')}")
        plt.rcParams.update({"figure.facecolor":"#0F1117","axes.facecolor":"#1E2436",
                             "axes.edgecolor":"#2A3147","text.color":"#E2E8F0",
                             "xtick.color":"#64748B","ytick.color":"#64748B",
                             "axes.labelcolor":"#64748B","grid.color":"#2A3147"})
        fig, ax = plt.subplots(figsize=(10,3))
        ax.plot(df["measured_at"], df["value"], marker="o", lw=2, color="#22C55E", ms=5, zorder=3)
        ax.fill_between(df["measured_at"], df["value"], alpha=0.10, color="#22C55E")
        ax.axhline(TRIAGE["very_high"], color="#EF4444", ls="--", lw=1.2, alpha=0.7, label=f"Very high ({TRIAGE['very_high']})")
        ax.axhline(TRIAGE["hypo"],      color="#F59E0B", ls="--", lw=1.2, alpha=0.7, label=f"Low ({TRIAGE['hypo']})")
        ax.set_ylabel("mg/dL", fontsize=10); ax.grid(axis="y", alpha=0.25)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.legend(fontsize=8, labelcolor="#E2E8F0", facecolor="#1E2436", edgecolor="#2A3147")
        plt.xticks(rotation=30, fontsize=8); plt.tight_layout()
        st.pyplot(fig); plt.rcParams.update(plt.rcParamsDefault)
        st.caption(t("trend_note"))
        if st.button("📋 " + ("View all readings" if _lang()=="en" else "تمام ریڈنگز دیکھیں"), key="tog_readings"):
            ss["show_all_readings"] = not ss.get("show_all_readings", False); st.rerun()
        if ss.get("show_all_readings", False):
            st.dataframe(df.rename(columns={"measured_at":t("col_time"),"type":t("col_type"),
                                            "value":t("col_val"),"meal_note":t("col_note")}),
                         use_container_width=True)

    st.markdown(f'<div class="footer">⚠️ {APP["disclaimer"]}</div>', unsafe_allow_html=True)

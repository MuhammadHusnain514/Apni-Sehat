# triage.py  –  Apni Sehat v1.2
# Clinical safety routing logic.
# Returns GREEN / AMBER / RED based on user health data.
# Your doctor teammate can adjust thresholds in config.py without touching this file.

import math
from typing import List, Optional, Tuple
from config import TRIAGE


def _mean(xs: List[float]) -> float:
    return sum(xs) / max(len(xs), 1)


def _std(xs: List[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m   = _mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(var)


def triage_profile(
    diabetes_type: str,
    has_hypertension: bool,
    has_high_cholesterol: bool,
    bp_sys: Optional[float],
    bp_dia: Optional[float],
    a1c: Optional[float],
    fasting_readings: List[float],
    total_cholesterol: Optional[float],
    other_major_conditions: bool,
) -> Tuple[str, List[str]]:
    """
    Returns:
        level: "GREEN" | "AMBER" | "RED"
        flags: list of human-readable notes shown to the user
    """
    flags: List[str] = []
    level = "GREEN"

    # Immediate RED — other major conditions
    if other_major_conditions:
        return "RED", [
            "Other major conditions selected. "
            "Please consult a clinician before using this app for dietary changes."
        ]

    # Diabetes type note
    if diabetes_type.strip().lower() == "type 1":
        flags.append(
            "Type 1 diabetes: this app provides dietary support only — "
            "never adjust insulin or medication based on this app."
        )

    # Blood pressure
    if has_hypertension or (bp_sys is not None and bp_dia is not None):
        if bp_sys is not None and bp_dia is not None:
            if bp_sys > TRIAGE["bp_crisis_sys"] or bp_dia > TRIAGE["bp_crisis_dia"]:
                return "RED", ["Blood pressure is in a severe range. Please seek urgent medical care."]
            if bp_sys >= TRIAGE["bp_stage2_sys"] or bp_dia >= TRIAGE["bp_stage2_dia"]:
                level = "AMBER"
                flags.append("Blood pressure is elevated. Clinician follow-up recommended.")
        else:
            level = "AMBER"
            flags.append("Hypertension selected but BP values not provided — proceed with care.")

    # Cholesterol
    if has_high_cholesterol or (total_cholesterol is not None and total_cholesterol > 0):
        if total_cholesterol is not None and total_cholesterol > 0:
            if total_cholesterol >= TRIAGE["tc_high"]:
                level = "AMBER"
                flags.append("Total cholesterol is high — heart-healthy plan recommended. See your doctor.")
            elif total_cholesterol >= TRIAGE["tc_borderline"]:
                flags.append("Total cholesterol is borderline — heart-healthy plan applied.")
        else:
            level = "AMBER"
            flags.append("High cholesterol selected but value not provided — proceed with care.")

    # Glucose stability — prefer A1c, fall back to fasting readings
    if a1c is not None and a1c > 0:
        if a1c >= TRIAGE["a1c_red"]:
            return "RED", ["HbA1c is very high. Please see a clinician before making dietary changes."]
        if a1c >= TRIAGE["a1c_caution"]:
            level = "AMBER"
            flags.append("HbA1c is above the typical target — proceed with care and follow up with your doctor.")
        elif a1c > TRIAGE["a1c_goal"]:
            flags.append("HbA1c is slightly above the common target — focus on consistency.")
    else:
        fr = [x for x in fasting_readings if x is not None and x > 0]
        if fr:
            if any(x >= TRIAGE["very_high"] for x in fr):
                return "RED", ["Very high fasting glucose recorded. Please seek medical advice."]
            if any(x < TRIAGE["hypo"] for x in fr):
                level = "AMBER"
                flags.append("Low fasting glucose detected — discuss with your clinician.")
            if len(fr) >= 2:
                sd  = _std(fr)
                rng = max(fr) - min(fr)
                if rng >= TRIAGE["fasting_range_red"] or sd >= TRIAGE["fasting_std_red"]:
                    return "RED", ["Large variation in recent fasting readings — please see a clinician."]
                if sd >= TRIAGE["fasting_std_amber"] or any(x > TRIAGE["premeal_high"] for x in fr):
                    level = "AMBER"
                    flags.append("Recent fasting readings show variability or are above target — proceed with care.")
        else:
            level = "AMBER"
            flags.append("No A1c or fasting readings provided — proceed with care.")

    return level, flags

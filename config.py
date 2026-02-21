# config.py  –  Apni Sehat v1.2
# Clinical thresholds and meal structure profiles.
# Doctor teammate can adjust thresholds here without touching any other file.

TRIAGE = {
    # Blood pressure
    "bp_stage2_sys":  140,
    "bp_stage2_dia":  90,
    "bp_crisis_sys":  180,
    "bp_crisis_dia":  120,

    # Glucose (mg/dL) — awareness ranges, not diagnostic thresholds
    "hypo":           70,
    "premeal_high":   130,
    "postmeal_high":  180,
    "very_high":      300,

    # HbA1c (%)
    "a1c_goal":       7.0,
    "a1c_caution":    8.0,
    "a1c_red":        9.0,

    # Total cholesterol (mg/dL)
    "tc_borderline":  200,
    "tc_high":        240,

    # Fasting glucose variability
    "fasting_std_amber":  25.0,
    "fasting_std_red":    45.0,
    "fasting_range_red":  120.0,
}

CARB = {
    # 1 carb serving = ~15g carbs (standard exchange)
    "carb_serving_grams": 15,
}

# ── South Asian BMI thresholds (lower than Western) ──────────────────────────
# Reference: WHO expert consultation on obesity in Asian populations
BMI = {
    "underweight":  18.5,
    "normal_max":   22.9,
    "overweight":   23.0,   # South Asian overweight starts here
    "obese":        27.5,   # South Asian obese starts here
}

# ── Meal structure profiles ───────────────────────────────────────────────────
# Each profile defines which slots appear in the daily plan and their labels.
# Slots: breakfast, snack_am, lunch, snack_pm, dinner, snack_bed
# The planner uses this to build the day structure.

MEAL_PROFILES = {
    # 3 meals + 1 afternoon snack — standard for stable Type 2, no insulin
    "3M_1S": {
        "label_en": "3 meals + 1 snack",
        "label_ur": "3 کھانے + 1 ناشتہ",
        "reason_en": "Standard plan for stable blood sugar — 3 balanced meals with one snack.",
        "reason_ur": "مستحکم بلڈ شوگر کے لیے معیاری منصوبہ۔",
        "slots": ["breakfast", "lunch", "snack_pm", "dinner"],
    },

    # 3 meals + 2 snacks — for insulin users OR hypo episodes OR weakness between meals
    "3M_2S": {
        "label_en": "3 meals + 2 snacks",
        "label_ur": "3 کھانے + 2 ناشتے",
        "reason_en": (
            "You need regular fuel throughout the day to prevent blood sugar dips. "
            "A mid-morning and afternoon snack keeps your levels steady."
        ),
        "reason_ur": (
            "آپ کو بلڈ شوگر گرنے سے بچانے کے لیے دن بھر باقاعدہ کھانا ضروری ہے۔ "
            "صبح اور دوپہر کے درمیان اور شام کا ناشتہ آپ کی شوگر مستحکم رکھتا ہے۔"
        ),
        "slots": ["breakfast", "snack_am", "lunch", "snack_pm", "dinner"],
    },

    # 3 meals + 3 snacks — insulin + hypo episodes (high risk of drops)
    "3M_3S": {
        "label_en": "3 meals + 3 snacks",
        "label_ur": "3 کھانے + 3 ناشتے",
        "reason_en": (
            "Because you use insulin and experience low sugar episodes, "
            "eating every 2-3 hours is important to stay safe. "
            "Do not go more than 3 hours without eating."
        ),
        "reason_ur": (
            "چونکہ آپ انسولین لیتے ہیں اور کم شوگر کی علامات آتی ہیں، "
            "ہر 2-3 گھنٹے میں کچھ نہ کچھ کھانا ضروری ہے۔ "
            "3 گھنٹے سے زیادہ بھوکے نہ رہیں۔"
        ),
        "slots": ["breakfast", "snack_am", "lunch", "snack_pm", "dinner", "snack_bed"],
    },

    # Smaller 3 meals + 1 snack — overweight/obese Type 2, no insulin
    # Smaller carb portions, higher veg, calorie-conscious
    "SMALL_3M_1S": {
        "label_en": "3 lighter meals + 1 snack (portion-controlled)",
        "label_ur": "3 ہلکے کھانے + 1 ناشتہ (کم مقدار)",
        "reason_en": (
            "Because your BMI suggests you are carrying extra weight, "
            "your plan uses smaller portions and lighter meals "
            "to support gradual, healthy weight loss alongside blood sugar control."
        ),
        "reason_ur": (
            "آپ کا BMI اضافی وزن ظاہر کرتا ہے، اس لیے آپ کے منصوبے میں "
            "کم مقدار اور ہلکے کھانے شامل ہیں تاکہ وزن آہستہ آہستہ کم ہو "
            "اور بلڈ شوگر بھی کنٹرول میں رہے۔"
        ),
        "slots": ["breakfast", "lunch", "snack_pm", "dinner"],
        "portion_note_en": "Keep portions small — use a side plate, not a full plate.",
        "portion_note_ur": "کھانا کم مقدار میں کھائیں — بڑی پلیٹ کی بجائے چھوٹی پلیٹ استعمال کریں۔",
    },
}


def get_meal_profile(
    on_insulin: bool,
    hypo_episodes: bool,
    weakness_between: bool,
    bmi: float,
    diabetes_type: str,
) -> str:
    """
    Returns the meal profile key based on clinical inputs.
    Priority order: insulin+hypo > insulin/hypo/weakness > overweight > standard
    """
    # Highest priority: insulin AND hypo episodes → maximum meal frequency
    if on_insulin and hypo_episodes:
        return "3M_3S"

    # Insulin OR hypo episodes OR weakness between meals → 2 snacks
    if on_insulin or hypo_episodes or weakness_between:
        return "3M_2S"

    # Overweight/obese Type 2, no insulin risk → portion-controlled plan
    dtype_lower = diabetes_type.strip().lower()
    if bmi and bmi >= BMI["overweight"] and "2" in dtype_lower and not on_insulin:
        return "SMALL_3M_1S"

    # Standard
    return "3M_1S"


APP = {
    "title":   "Apni Sehat",
    "version": "1.2.0",
    "disclaimer": (
        "This app provides general dietary information only. "
        "It does not diagnose, prescribe, or replace professional medical advice. "
        "Always follow your doctor's instructions."
    ),
}

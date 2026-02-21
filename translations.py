# translations.py  –  Apni Sehat v1.2
# All user-facing strings in English and Urdu.
# Usage:  from translations import T, get_tip
#         T["en"]["key"]   or   T["ur"]["key"]

import random

TIPS = {
    "en": [
        "💧 Drink 8 glasses of water daily — it helps control blood sugar.",
        "🚶 A 15-minute walk after meals can lower blood sugar by up to 30%.",
        "🥗 Fill half your plate with vegetables at every meal.",
        "⏰ Eat at the same times each day to keep blood sugar stable.",
        "🍞 Whole wheat roti is much better than maida roti for blood sugar.",
        "🥜 A small handful of unsalted nuts makes a great low-sugar snack.",
        "😴 Poor sleep raises blood sugar — aim for 7 to 8 hours each night.",
        "📊 Log your glucose readings regularly to spot patterns.",
        "🍚 Keep rice to one small katori — no second helpings.",
        "🍬 Avoid sweet drinks like sodas and packaged juices.",
        "🧅 Add onion, garlic and fenugreek (methi) to your cooking.",
        "🍋 Squeeze lemon on food to lower its glycemic impact.",
        "🕐 Never skip breakfast — it keeps blood sugar steady all day.",
        "🫀 Controlling blood sugar also protects your heart, kidneys and eyes.",
        "🧂 Reduce salt if you have blood pressure — use lemon and herbs instead.",
    ],
    "ur": [
        "💧 روزانہ 8 گلاس پانی پئیں — یہ بلڈ شوگر کنٹرول کرتا ہے۔",
        "🚶 کھانے کے بعد 15 منٹ کی چہل قدمی بلڈ شوگر 30 فیصد تک کم کر سکتی ہے۔",
        "🥗 ہر کھانے میں آدھی پلیٹ سبزیوں سے بھریں۔",
        "⏰ روزانہ ایک ہی وقت پر کھانا کھائیں۔",
        "🍞 میدے کی روٹی کی بجائے گندم کی روٹی کھائیں۔",
        "🥜 مٹھی بھر بغیر نمک کے گری دار میوے ایک اچھا ناشتہ ہے۔",
        "😴 نیند کی کمی بلڈ شوگر بڑھاتی ہے — رات کو 7 سے 8 گھنٹے سوئیں۔",
        "📊 اپنی گلوکوز ریڈنگز باقاعدگی سے درج کریں۔",
        "🍚 چاول ایک چھوٹی کٹوری سے زیادہ نہ کھائیں۔",
        "🍬 میٹھے مشروبات اور پیکڈ جوس سے پرہیز کریں۔",
        "🧅 پکانے میں پیاز، لہسن اور میتھی شامل کریں۔",
        "🍋 کھانے پر لیموں نچوڑیں — شوگر کا اثر کم ہو گا۔",
        "🕐 ناشتہ کبھی نہ چھوڑیں — سارا دن بلڈ شوگر مستحکم رہے گی۔",
        "🫀 بلڈ شوگر کنٹرول سے دل، گردے اور آنکھیں بھی محفوظ رہتی ہیں۔",
        "🧂 بلڈ پریشر ہو تو نمک کم کریں — لیموں اور مسالے استعمال کریں۔",
    ],
}


def get_tip(lang: str = "en") -> str:
    return random.choice(TIPS.get(lang, TIPS["en"]))


T = {
    # ─────────────────────── ENGLISH ─────────────────────────────────────────
    "en": {
        # App shell
        "app_title":    "Apni Sehat",
        "app_subtitle": "Your personal health companion — اپنی صحت",
        "lang_btn":     "اردو",
        "version":      "v1.2.0 · HEC GenAI Hackathon",

        # Entry screen (no "login" language)
        "entry_heading":    "👋 Hello! Tell us who you are",
        "entry_subtitle":   "We use your phone number to remember your plan. Nothing else is stored.",
        "entry_name":       "Your Name",
        "entry_name_hint":  "e.g. Ahmed Khan",
        "entry_phone":      "Phone Number",
        "entry_phone_hint": "Include your country code, e.g. +92, +44, +1",
        "entry_phone_ph":   "+92xxxxxxxxxx",
        "entry_btn":        "Let's go →",
        "entry_privacy":    "🔒 Your phone number is never stored — only a secure code is used to find your plan.",
        "name_error":       "Please enter your name.",
        "phone_error":      "Please enter a valid phone number with country code, e.g. +92...",
        "finding_plan":     "Finding your plan...",
        "welcome_back":     "Welcome back",
        "new_user_found":   "Welcome! Let's set up your profile.",

        # Wizard
        "wizard_step1_heading":  "Step 1 of 2 — Tell us about yourself",
        "wizard_step1_caption":  "This takes about one minute and helps us build the right meal plan for you.",
        "wizard_step2_heading":  "Step 2 of 2 — Any health conditions?",
        "wizard_step2_caption":  "This helps us make sure the app is safe and appropriate for you.",
        "wizard_next":           "Next →",
        "wizard_back":           "← Back",
        "wizard_finish":         "✅ Build My Plan",
        "wizard_saving":         "Setting up your plan...",
        "wizard_done_msg":       "Great! Your personalised meal plan is ready.",
        "wizard_name":           "Your Name",
        "wizard_age":            "Your Age",
        "wizard_diabetes":       "Diabetes Type",
        "wizard_diabetes_opts":  ["Type 2", "Type 1", "Not sure"],
        "wizard_hypert":         "I have high blood pressure (hypertension)",
        "wizard_chol":           "I have high cholesterol",
        "wizard_other":          "I have other major conditions (kidney disease, pregnancy, etc.)",
        "wizard_desi":           "I prefer desi food 🍛",
        "wizard_veg":            "I prefer vegetarian meals 🥦",
        "wizard_age_note":       "You can skip age and other details for now — you can always add them later.",

        # Profile card (on plan tab)
        "profile_card_label":  "Your Profile",
        "edit_profile_btn":    "✏️ Edit",
        "save_profile_btn":    "💾 Save Changes",
        "saving_profile":      "Saving...",
        "profile_saved":       "✅ Saved! Your plan has been updated.",
        "profile_card_name":   "Name",
        "profile_card_age":    "Age",
        "profile_card_type":   "Type",
        "profile_card_conds":  "Conditions",
        "no_conditions":       "None recorded",
        "health_status":       "Health Status",
        "status_green":        "🟢 Stable",
        "status_amber":        "🟡 Caution — see doctor",
        "status_red":          "🔴 Please see a clinician",
        "status_none":         "Complete profile to check",

        # Profile edit form fields
        "pf_name":          "Full Name",
        "pf_age":           "Age",
        "pf_gender":        "Gender (optional)",
        "pf_gender_opts":   ["Prefer not to say", "Male", "Female", "Other"],
        "pf_diabetes":      "Diabetes Type",
        "pf_diabetes_opts": ["Type 2", "Type 1", "Not sure"],
        "pf_height":        "Height (cm)",
        "pf_weight":        "Weight (kg)",
        "pf_bmi":           "Estimated BMI",
        "pf_bmi_note":      "(informational only)",
        "pf_family":        "Family history (optional)",
        "pf_family_opts":   ["Diabetes", "Hypertension", "High cholesterol", "Heart disease"],
        "pf_hypert":        "I have high blood pressure",
        "pf_chol":          "I have high cholesterol",
        "pf_other":         "Other major conditions (kidney disease, pregnancy, etc.)",
        "pf_advanced":      "🔬 Add recent test results (optional)",
        "pf_advanced_note": "Fill in what you know. Leave as 0 if unsure.",
        "pf_bp_sys":        "Systolic BP (mmHg)",
        "pf_bp_dia":        "Diastolic BP (mmHg)",
        "pf_a1c":           "HbA1c (%)",
        "pf_chol_val":      "Total cholesterol (mg/dL)",
        "pf_fasting_head":  "Recent fasting glucose readings",
        "pf_fasting_note":  "Fasting = no food for 8+ hours before measuring",
        "pf_day3":          "3 days ago (mg/dL)",
        "pf_day2":          "2 days ago (mg/dL)",
        "pf_day1":          "Yesterday (mg/dL)",
        "pf_health_result": "Health Assessment",
        "green_result":     "🟢 All clear — your readings look stable.",
        "amber_result":     "🟡 Proceed with care — we recommend seeing your doctor too.",
        "red_result":       "🔴 Please see a clinician before making dietary changes.",
        "family_noted":     "📋 Family history noted:",
        "family_suffix":    "Used to personalise your plan.",

        # Sidebar
        "hi_user":          "Hi",
        "logout_btn":       "🚪 Change User",
        "logout_confirm":   "Switch to a different person?",
        "yes":              "Yes",
        "no":               "No",
        "disclaimer_title": "⚠️ Medical Disclaimer",
        "disclaimer_text":  (
            "**For informational support only — not medical advice.**\n\n"
            "- Does not diagnose or prescribe\n"
            "- Does not replace your doctor\n"
            "- Glucose above **180 mg/dL** repeatedly? See your doctor\n"
            "- **Low sugar signs:** shakiness, sweating, dizziness → get help now\n"
            "- **High sugar signs:** frequent urination, thirst, blurred vision → see doctor\n"
            "- In an emergency, call emergency services immediately"
        ),

        # Tip banner
        "tip_title": "💡 Tip of the Day",
        "tip_new":   "🔄 New Tip",

        # Tabs
        "tab_plan":      "🥗 My Plan",
        "tab_chat":      "💬 Ask",
        "tab_glucose":   "📊 Log Sugar",
        "tab_dashboard": "📈 Progress",

        # Plan tab
        "plan_heading":  "Your 7-Day Meal Plan",
        "plan_blocked":  "🔴 Your readings need medical attention first. Please see a doctor before making dietary changes.",
        "plan_no_profile": "💡 Complete your profile above to get a plan tailored to your conditions.",
        "desi_toggle":   "🍛 Prefer Desi food",
        "veg_toggle":    "🥦 Vegetarian only",
        "regen_btn":     "🔄 Refresh Plan",
        "building_plan": "Building your 7-day plan...",
        "loading_plan":  "Loading your plan...",
        "swaps_btn":     "💡 Suggest healthy swaps",
        "getting_swaps": "Getting suggestions...",
        "swaps_heading": "Swap suggestions:",
        "day_label":     "Day",
        "carbs_label":   "carbs",

        # Chat tab
        "chat_heading":  "Ask Your Health Assistant",
        "chat_caption":  "Ask anything about your diet or blood sugar — in English or Urdu.",
        "chat_greeting_en": (
            "Hello! 👋 I am **Sehat Saathi**, your friendly health assistant.\n\n"
            "I can help you with:\n"
            "• Diet tips for managing diabetes\n"
            "• Understanding your blood sugar readings\n"
            "• Healthy alternatives to your favourite desi foods\n"
            "• Any health question in simple language\n\n"
            "How can I help you today? You can also write in **اردو** if you prefer."
        ),
        "chat_placeholder": "Type your question here... (English or اردو)",
        "chat_thinking":    "Thinking...",
        "chat_clear":       "🗑️ Clear chat",
        "chat_note":        "Dietary guidance only — not medical advice. See your doctor for medical decisions.",

        # Glucose tab
        "glucose_heading":  "Log Blood Sugar Reading",
        "reading_types":    ["Fasting", "Pre-meal", "Post-meal (1-2h)", "Bedtime"],
        "reading_lbl":      "Reading type",
        "date_lbl":         "Date",
        "time_lbl":         "Time",
        "value_lbl":        "Glucose (mg/dL)",
        "note_lbl":         "Meal note (optional)",
        "note_ph":          "e.g. biryani, nihari, roti...",
        "ref_ranges":       "Reference: 🟡 Low < {h}  |  🟢 Fasting target 80-130  |  🔴 Very high ≥ {vh}",
        "very_high_alert":  "⚠️ Very high. If unwell, seek medical attention immediately.",
        "low_alert":        "⚠️ Low reading. Have something sweet and consult your doctor.",
        "save_reading_btn": "💾 Save Reading",
        "saving_reading":   "Saving...",
        "reading_saved":    "✅ Reading saved!",

        # Check-in (inside plan tab)
        "checkin_heading":  "📋 Today's Check-In",
        "checkin_date":     "Date",
        "followed_q":       "Did you follow your meal plan today?",
        "yes_opt":          "Yes ✅",
        "no_opt":           "No ❌",
        "save_ci_btn":      "Save",
        "ci_saved":         "✅ Great work! Consistency is what matters most.",
        "ate_label":        "What did you eat instead?",
        "ate_ph":           "e.g. biryani, nihari, extra roti, sweets...",
        "save_suggest_btn": "Save + Get Tips",
        "saving_suggest":   "Saving and getting personalised tips...",
        "suggest_saved":    "✅ Here are healthier approaches for next time:",
        "suggest_note":     "For dietary awareness only — not medical advice.",
        "describe_ate":     "Please describe what you ate to get suggestions.",

        # Dashboard tab
        "dash_heading":  "My Progress",
        "dash_caption":  "Share this with your doctor for better guidance.",
        "adh_section":   "📅 Plan Adherence",
        "adh_metric":    "Adherence rate",
        "adh_delta":     "of {n} days",
        "no_checkins":   "No check-ins yet — use the check-in section in My Plan to start.",
        "gluc_section":  "🩸 Glucose Readings",
        "avg_lbl":       "Average",
        "var_lbl":       "Variability",
        "total_lbl":     "Logs",
        "high_alert_d":  "⚠️ {n} very high reading(s). If persistent, see your doctor.",
        "low_alert_d":   "⚠️ {n} low reading(s). Discuss with your clinician.",
        "no_glucose":    "No readings yet — use Log Sugar to start.",
        "trend_head":    "Glucose Trend",
        "trend_note":    "For personal awareness only.",
        "view_all":      "View all readings",
        "col_time":      "Time", "col_type": "Type",
        "col_val":       "mg/dL", "col_note": "Meal",
        "col_date":      "Date", "col_fol":  "Followed?",

        # Misc
        "blocked_msg":   "🔴 This feature is unavailable. Please see a clinician first.",
        # Insulin / hypoglycaemia / weakness questions
        "q_insulin":         "Are you on insulin injections?",
        "q_insulin_help":    "This includes any insulin pen or syringe prescribed by your doctor.",
        "q_hypo":            "Do you get low blood sugar episodes?",
        "q_hypo_help":       "Signs: sudden shakiness, sweating, dizziness, feeling faint between meals.",
        "q_weakness":        "Do you feel weakness or dizziness between meals?",
        "q_weakness_help":   "For example — feeling very hungry or dizzy 2-3 hours after eating.",

        # Meal structure card shown at top of plan
        "your_meal_plan":    "Your Personalised Meal Plan",
        "meal_structure":    "Meal Structure",
        "why_this_plan":     "Why this plan?",
        "portion_note":      "Portion Note",
        "slot_breakfast":    "🌅 Breakfast",
        "slot_snack_am":     "🍎 Mid-Morning Snack",
        "slot_lunch":        "☀️ Lunch",
        "slot_snack_pm":     "🍊 Afternoon Snack",
        "slot_dinner":       "🌙 Dinner",
        "slot_snack_bed":    "🌛 Bedtime Snack",
        "total_carbs":       "Total carbs today",
        "insulin_reminder":  "💉 Insulin reminder: Never skip a meal or snack if you are on insulin.",
        "hypo_reminder":     "⚠️ Always carry a fast sugar source (e.g. glucose tablets, juice, candy).",

        "db_error":      "Could not connect. Please refresh the page and try again.",
    },

    # ─────────────────────── URDU ─────────────────────────────────────────────
    "ur": {
        # App shell
        "app_title":    "اپنی صحت",
        "app_subtitle": "آپ کا ذاتی صحت کا ساتھی",
        "lang_btn":     "English",
        "version":      "v1.2.0 · HEC GenAI Hackathon",

        # Entry screen
        "entry_heading":    "👋 السلام علیکم! اپنا نام اور نمبر بتائیں",
        "entry_subtitle":   "ہم آپ کا فون نمبر صرف آپ کا منصوبہ یاد رکھنے کے لیے استعمال کرتے ہیں۔",
        "entry_name":       "آپ کا نام",
        "entry_name_hint":  "مثلاً: احمد خان",
        "entry_phone":      "فون نمبر",
        "entry_phone_hint": "ملکی کوڈ شامل کریں جیسے +92، +44، +1",
        "entry_phone_ph":   "+92xxxxxxxxxx",
        "entry_btn":        "آگے بڑھیں →",
        "entry_privacy":    "🔒 آپ کا فون نمبر کبھی محفوظ نہیں کیا جاتا۔",
        "name_error":       "براہ کرم اپنا نام لکھیں۔",
        "phone_error":      "براہ کرم ملکی کوڈ کے ساتھ درست فون نمبر لکھیں۔",
        "finding_plan":     "آپ کا منصوبہ تلاش ہو رہا ہے...",
        "welcome_back":     "خوش آمدید واپس",
        "new_user_found":   "خوش آمدید! آئیں آپ کی پروفائل بنائیں۔",

        # Wizard
        "wizard_step1_heading":  "مرحلہ 1 — اپنے بارے میں بتائیں",
        "wizard_step1_caption":  "صرف ایک منٹ لگے گا۔ اس سے آپ کا صحیح کھانے کا منصوبہ بنے گا۔",
        "wizard_step2_heading":  "مرحلہ 2 — کوئی بیماری؟",
        "wizard_step2_caption":  "یہ ہمیں یقین دلاتا ہے کہ ایپ آپ کے لیے محفوظ ہے۔",
        "wizard_next":           "اگلا →",
        "wizard_back":           "← واپس",
        "wizard_finish":         "✅ میرا منصوبہ بنائیں",
        "wizard_saving":         "آپ کا منصوبہ تیار ہو رہا ہے...",
        "wizard_done_msg":       "بہت اچھا! آپ کا ذاتی کھانے کا منصوبہ تیار ہے۔",
        "wizard_name":           "آپ کا نام",
        "wizard_age":            "آپ کی عمر",
        "wizard_diabetes":       "ذیابیطس کی قسم",
        "wizard_diabetes_opts":  ["قسم 2", "قسم 1", "یقین نہیں"],
        "wizard_hypert":         "مجھے ہائی بلڈ پریشر ہے",
        "wizard_chol":           "مجھے زیادہ کولیسٹرول ہے",
        "wizard_other":          "دیگر بڑی بیماریاں (گردے، حمل وغیرہ)",
        "wizard_desi":           "مجھے دیسی کھانا پسند ہے 🍛",
        "wizard_veg":            "میں سبزی خور ہوں 🥦",
        "wizard_age_note":       "عمر اور دیگر تفصیلات بعد میں بھی شامل کی جا سکتی ہیں۔",

        # Profile card
        "profile_card_label":  "آپ کی پروفائل",
        "edit_profile_btn":    "✏️ تبدیل کریں",
        "save_profile_btn":    "💾 محفوظ کریں",
        "saving_profile":      "محفوظ ہو رہا ہے...",
        "profile_saved":       "✅ محفوظ! آپ کا منصوبہ اپ ڈیٹ ہو گیا۔",
        "profile_card_name":   "نام",
        "profile_card_age":    "عمر",
        "profile_card_type":   "قسم",
        "profile_card_conds":  "بیماریاں",
        "no_conditions":       "کوئی نہیں",
        "health_status":       "صحت کی حالت",
        "status_green":        "🟢 مستحکم",
        "status_amber":        "🟡 احتیاط — ڈاکٹر سے ملیں",
        "status_red":          "🔴 ڈاکٹر سے ضرور ملیں",
        "status_none":         "پروفائل مکمل کریں",

        # Profile edit form
        "pf_name":          "پورا نام",
        "pf_age":           "عمر",
        "pf_gender":        "جنس (اختیاری)",
        "pf_gender_opts":   ["بتانا نہیں چاہتے", "مرد", "عورت", "دیگر"],
        "pf_diabetes":      "ذیابیطس کی قسم",
        "pf_diabetes_opts": ["قسم 2", "قسم 1", "یقین نہیں"],
        "pf_height":        "قد (سینٹی میٹر)",
        "pf_weight":        "وزن (کلوگرام)",
        "pf_bmi":           "تخمینی BMI",
        "pf_bmi_note":      "(صرف معلومات)",
        "pf_family":        "خاندانی بیماریاں (اختیاری)",
        "pf_family_opts":   ["ذیابیطس", "ہائی بلڈ پریشر", "زیادہ کولیسٹرول", "دل کی بیماری"],
        "pf_hypert":        "مجھے ہائی بلڈ پریشر ہے",
        "pf_chol":          "مجھے زیادہ کولیسٹرول ہے",
        "pf_other":         "دیگر بڑی بیماریاں (گردے، حمل وغیرہ)",
        "pf_advanced":      "🔬 حالیہ ٹیسٹ کے نتائج شامل کریں (اختیاری)",
        "pf_advanced_note": "جو معلوم ہو وہ بھریں۔ نہ معلوم ہو تو 0 چھوڑ دیں۔",
        "pf_bp_sys":        "سیسٹولک بی پی (mmHg)",
        "pf_bp_dia":        "ڈائسٹولک بی پی (mmHg)",
        "pf_a1c":           "HbA1c (%)",
        "pf_chol_val":      "کل کولیسٹرول (mg/dL)",
        "pf_fasting_head":  "حالیہ فاسٹنگ گلوکوز ریڈنگز",
        "pf_fasting_note":  "فاسٹنگ = ناپنے سے 8+ گھنٹے پہلے کچھ نہ کھائیں",
        "pf_day3":          "3 دن پہلے (mg/dL)",
        "pf_day2":          "2 دن پہلے (mg/dL)",
        "pf_day1":          "کل (mg/dL)",
        "pf_health_result": "صحت کا جائزہ",
        "green_result":     "🟢 سب ٹھیک ہے — آپ کی ریڈنگز مستحکم ہیں۔",
        "amber_result":     "🟡 احتیاط سے آگے بڑھیں — ڈاکٹر سے بھی مشورہ کریں۔",
        "red_result":       "🔴 کھانے میں تبدیلی سے پہلے ڈاکٹر سے ملیں۔",
        "family_noted":     "📋 خاندانی بیماریاں نوٹ کی گئیں:",
        "family_suffix":    "آپ کا منصوبہ ذاتی بنانے کے لیے استعمال ہوتا ہے۔",

        # Sidebar
        "hi_user":          "السلام علیکم",
        "logout_btn":       "🚪 دوسرا شخص",
        "logout_confirm":   "کسی اور کی پروفائل پر جانا چاہتے ہیں؟",
        "yes":              "ہاں",
        "no":               "نہیں",
        "disclaimer_title": "⚠️ طبی وضاحت",
        "disclaimer_text":  (
            "**یہ ایپ صرف معلوماتی مدد کے لیے ہے — طبی مشورے کی جگہ نہیں لیتی۔**\n\n"
            "- یہ ایپ تشخیص نہیں کرتی اور دوائی تجویز نہیں کرتی\n"
            "- شوگر بار بار **180 mg/dL** سے اوپر؟ ڈاکٹر سے ملیں\n"
            "- **کم شوگر:** کپکپی، پسینہ، چکر → فوری مدد لیں\n"
            "- **زیادہ شوگر:** بار بار پیشاب، پیاس، دھندلی نظر → ڈاکٹر سے ملیں\n"
            "- ہنگامی صورت میں ایمرجنسی سروسز کو کال کریں"
        ),

        # Tip banner
        "tip_title": "💡 آج کی صحت کی تجویز",
        "tip_new":   "🔄 نئی تجویز",

        # Tabs
        "tab_plan":      "🥗 میرا منصوبہ",
        "tab_chat":      "💬 سوال پوچھیں",
        "tab_glucose":   "📊 شوگر لاگ",
        "tab_dashboard": "📈 پیشرفت",

        # Plan tab
        "plan_heading":    "آپ کا 7 دن کا کھانے کا منصوبہ",
        "plan_blocked":    "🔴 آپ کی ریڈنگز طبی توجہ مانگتی ہیں۔ پہلے ڈاکٹر سے ملیں۔",
        "plan_no_profile": "💡 اپنی پروفائل مکمل کریں تاکہ آپ کی صحت کے مطابق منصوبہ ملے۔",
        "desi_toggle":     "🍛 دیسی کھانا پسند ہے",
        "veg_toggle":      "🥦 صرف سبزی خور",
        "regen_btn":       "🔄 نیا منصوبہ",
        "building_plan":   "آپ کا 7 دن کا منصوبہ بن رہا ہے...",
        "loading_plan":    "منصوبہ لوڈ ہو رہا ہے...",
        "swaps_btn":       "💡 صحت مند متبادل",
        "getting_swaps":   "تجاویز تیار ہو رہی ہیں...",
        "swaps_heading":   "متبادل تجاویز:",
        "day_label":       "دن",
        "carbs_label":     "کاربس",

        # Chat tab
        "chat_heading":  "اپنے صحت کے مددگار سے پوچھیں",
        "chat_caption":  "خوراک یا بلڈ شوگر کے بارے میں کچھ بھی پوچھیں — اردو یا انگریزی میں۔",
        "chat_greeting_en": (
            "السلام علیکم! 👋 میں **صحت ساتھی** ہوں، آپ کا دوستانہ صحت کا مددگار۔\n\n"
            "میں آپ کی مدد کر سکتا ہوں:\n"
            "• ذیابیطس کے لیے خوراک کی تجاویز\n"
            "• اپنی بلڈ شوگر سمجھنے میں\n"
            "• دیسی کھانوں کے صحت مند متبادل\n"
            "• صحت کے کسی بھی سوال کا جواب\n\n"
            "آج میں آپ کی کیا مدد کر سکتا ہوں؟"
        ),
        "chat_placeholder": "یہاں اپنا سوال لکھیں... (اردو یا English)",
        "chat_thinking":    "سوچ رہا ہوں...",
        "chat_clear":       "🗑️ گفتگو صاف کریں",
        "chat_note":        "صرف خوراک کی رہنمائی — طبی مشورہ نہیں۔",

        # Glucose tab
        "glucose_heading":  "بلڈ شوگر ریڈنگ درج کریں",
        "reading_types":    ["فاسٹنگ", "کھانے سے پہلے", "کھانے کے بعد (1-2 گھنٹے)", "سونے سے پہلے"],
        "reading_lbl":      "ریڈنگ کی قسم",
        "date_lbl":         "تاریخ",
        "time_lbl":         "وقت",
        "value_lbl":        "گلوکوز (mg/dL)",
        "note_lbl":         "کھانے کا نوٹ (اختیاری)",
        "note_ph":          "مثلاً: بریانی، نہاری، روٹی...",
        "ref_ranges":       "حوالہ: 🟡 کم < {h}  |  🟢 فاسٹنگ ہدف: 80-130  |  🔴 بہت زیادہ ≥ {vh}",
        "very_high_alert":  "⚠️ بہت زیادہ ریڈنگ۔ طبیعت خراب ہو تو فوری ڈاکٹر سے ملیں۔",
        "low_alert":        "⚠️ کم ریڈنگ۔ فوری میٹھا کھائیں اور ڈاکٹر سے ملیں۔",
        "save_reading_btn": "💾 ریڈنگ محفوظ کریں",
        "saving_reading":   "محفوظ ہو رہا ہے...",
        "reading_saved":    "✅ ریڈنگ محفوظ!",

        # Check-in
        "checkin_heading":  "📋 آج کا چیک-ان",
        "checkin_date":     "تاریخ",
        "followed_q":       "کیا آپ نے آج کھانے کا منصوبہ فالو کیا؟",
        "yes_opt":          "ہاں ✅",
        "no_opt":           "نہیں ❌",
        "save_ci_btn":      "محفوظ کریں",
        "ci_saved":         "✅ بہت اچھا! مسلسل کوشش ہی کامیابی ہے۔",
        "ate_label":        "آپ نے کیا کھایا؟",
        "ate_ph":           "مثلاً: بریانی، نہاری، اضافی روٹی، مٹھائی...",
        "save_suggest_btn": "محفوظ کریں + تجاویز",
        "saving_suggest":   "محفوظ ہو رہا ہے اور تجاویز تیار ہو رہی ہیں...",
        "suggest_saved":    "✅ اگلی بار بہتر انتخاب کے لیے:",
        "suggest_note":     "صرف خوراک کی آگاہی کے لیے — طبی مشورہ نہیں۔",
        "describe_ate":     "براہ کرم بتائیں کہ آپ نے کیا کھایا۔",

        # Dashboard
        "dash_heading":  "میری پیشرفت",
        "dash_caption":  "بہتر رہنمائی کے لیے یہ اپنے ڈاکٹر کو دکھائیں۔",
        "adh_section":   "📅 منصوبے پر عمل",
        "adh_metric":    "عمل کی شرح",
        "adh_delta":     "{n} دنوں میں سے",
        "no_checkins":   "ابھی تک کوئی چیک-ان نہیں — میرا منصوبہ ٹیب سے شروع کریں۔",
        "gluc_section":  "🩸 گلوکوز ریڈنگز",
        "avg_lbl":       "اوسط",
        "var_lbl":       "اتار چڑھاؤ",
        "total_lbl":     "کل",
        "high_alert_d":  "⚠️ {n} بہت زیادہ ریڈنگز۔ مسلسل ہو تو ڈاکٹر سے ملیں۔",
        "low_alert_d":   "⚠️ {n} کم ریڈنگز۔ ڈاکٹر سے مشورہ کریں۔",
        "no_glucose":    "ابھی تک کوئی ریڈنگ نہیں — شوگر لاگ ٹیب سے شروع کریں۔",
        "trend_head":    "گلوکوز رجحان",
        "trend_note":    "صرف ذاتی آگاہی کے لیے۔",
        "view_all":      "تمام ریڈنگز دیکھیں",
        "col_time":      "وقت", "col_type": "قسم",
        "col_val":       "mg/dL", "col_note": "کھانا",
        "col_date":      "تاریخ", "col_fol":  "فالو کیا؟",

        # Misc
        "blocked_msg":   "🔴 یہ فیچر دستیاب نہیں۔ پہلے ڈاکٹر سے ملیں۔",
        # Insulin / hypoglycaemia / weakness questions
        "q_insulin":         "کیا آپ انسولین کے انجیکشن لیتے ہیں؟",
        "q_insulin_help":    "اس میں ڈاکٹر کی طرف سے تجویز کردہ انسولین پین یا سرنج شامل ہے۔",
        "q_hypo":            "کیا آپ کو کم شوگر کی علامات آتی ہیں؟",
        "q_hypo_help":       "علامات: اچانک کپکپی، پسینہ، چکر، کھانوں کے درمیان کمزوری محسوس ہونا۔",
        "q_weakness":        "کیا آپ کھانوں کے درمیان کمزوری یا چکر محسوس کرتے ہیں؟",
        "q_weakness_help":   "مثلاً کھانے کے 2-3 گھنٹے بعد بہت بھوک یا چکر آنا۔",

        # Meal structure card
        "your_meal_plan":    "آپ کا ذاتی کھانے کا منصوبہ",
        "meal_structure":    "کھانے کا ڈھانچہ",
        "why_this_plan":     "یہ منصوبہ کیوں؟",
        "portion_note":      "مقدار کا نوٹ",
        "slot_breakfast":    "🌅 ناشتہ",
        "slot_snack_am":     "🍎 دوپہر سے پہلے کا ناشتہ",
        "slot_lunch":        "☀️ دوپہر کا کھانا",
        "slot_snack_pm":     "🍊 شام کا ناشتہ",
        "slot_dinner":       "🌙 رات کا کھانا",
        "slot_snack_bed":    "🌛 سونے سے پہلے کا ناشتہ",
        "total_carbs":       "آج کے کل کاربس",
        "insulin_reminder":  "💉 انسولین یاددہانی: انسولین لینے والے کبھی کھانا یا ناشتہ نہ چھوڑیں۔",
        "hypo_reminder":     "⚠️ ہمیشہ ساتھ تیز شوگر رکھیں (جیسے گلوکوز کی گولیاں، جوس، مٹھائی)۔",

        "db_error":      "کنکشن نہیں ہو سکا۔ صفحہ تازہ کریں اور دوبارہ کوشش کریں۔",
    },
}

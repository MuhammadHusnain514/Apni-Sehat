# meal_bank.py  –  Apni Sehat v1.2
# Curated desi meal dataset covering all 6 possible slots.
# Slots: breakfast | snack_am | lunch | snack_pm | dinner | snack_bed
# Tags: desi | veg | high_fiber | low_sodium | low_satfat | light (low carb/cal for SMALL profile)

MEALS = [
    # ── BREAKFAST ─────────────────────────────────────────────────────────────
    {
        "name": "Besan chilla + unsweetened yogurt",
        "slot": "breakfast",
        "tags": ["desi", "veg", "high_fiber", "low_satfat", "low_sodium"],
        "carb_servings": 2,
        "notes": "Add chopped onion and green chilli. Keep oil minimal."
    },
    {
        "name": "Dalia (cracked wheat) with low-fat milk and almonds",
        "slot": "breakfast",
        "tags": ["desi", "veg", "high_fiber", "low_sodium"],
        "carb_servings": 2,
        "notes": "No sugar. A few almonds add healthy fat and slow sugar absorption."
    },
    {
        "name": "2 boiled eggs + 1 slice whole wheat bread + tomato",
        "slot": "breakfast",
        "tags": ["veg", "high_fiber", "low_satfat", "light"],
        "carb_servings": 1,
        "notes": "Boil or poach eggs. Tomato and cucumber on the side."
    },
    {
        "name": "Oats porridge with chia seeds and walnuts",
        "slot": "breakfast",
        "tags": ["veg", "high_fiber", "low_sodium", "low_satfat", "light"],
        "carb_servings": 2,
        "notes": "No sugar. Pinch of cinnamon helps blood sugar. Use water or low-fat milk."
    },
    {
        "name": "1 small whole wheat paratha (minimal oil) + plain yogurt",
        "slot": "breakfast",
        "tags": ["desi", "veg", "low_satfat"],
        "carb_servings": 2,
        "notes": "Very little oil. Yogurt adds protein. No butter or ghee on top."
    },
    {
        "name": "Moong daal chilla + mint chutney",
        "slot": "breakfast",
        "tags": ["desi", "veg", "high_fiber", "low_satfat", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "High protein and fibre. Very gentle on blood sugar."
    },

    # ── MID-MORNING SNACK (snack_am) ──────────────────────────────────────────
    # Small, protein/fibre focused — prevents mid-morning sugar dip
    {
        "name": "1 boiled egg + cucumber slices",
        "slot": "snack_am",
        "tags": ["veg", "low_sodium", "light"],
        "carb_servings": 0,
        "notes": "Zero-carb snack — protein keeps you full without spiking sugar."
    },
    {
        "name": "Small handful of roasted chana (unsalted)",
        "slot": "snack_am",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "High protein and fibre. Roasted, not fried."
    },
    {
        "name": "Unsweetened yogurt (1 small katori) with flaxseeds",
        "slot": "snack_am",
        "tags": ["desi", "veg", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Probiotic + healthy fat. Flaxseeds add fibre and omega-3."
    },
    {
        "name": "5 almonds + 1 small guava",
        "slot": "snack_am",
        "tags": ["veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Guava is the best fruit for diabetics. Almonds slow sugar absorption."
    },
    {
        "name": "Lassi (salted, low-fat, no sugar)",
        "slot": "snack_am",
        "tags": ["desi", "veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Salted lassi only — no sugar. Cooling and filling."
    },

    # ── LUNCH ─────────────────────────────────────────────────────────────────
    {
        "name": "Daal maash + 2 atta roti + cucumber salad",
        "slot": "lunch",
        "tags": ["desi", "veg", "high_fiber", "low_satfat", "low_sodium"],
        "carb_servings": 3,
        "notes": "Minimal oil in tadka. Lemon juice adds flavour without calories."
    },
    {
        "name": "Chana curry + 1 atta roti + raita",
        "slot": "lunch",
        "tags": ["desi", "veg", "high_fiber"],
        "carb_servings": 3,
        "notes": "Chickpeas are excellent for blood sugar. Avoid too much oil."
    },
    {
        "name": "Grilled chicken + mixed sabzi + 1 atta roti",
        "slot": "lunch",
        "tags": ["desi", "low_satfat", "low_sodium"],
        "carb_servings": 2,
        "notes": "Season with herbs and lemon. No frying."
    },
    {
        "name": "Mixed vegetable curry + 1 atta roti + plain yogurt",
        "slot": "lunch",
        "tags": ["desi", "veg", "low_sodium", "low_satfat", "high_fiber", "light"],
        "carb_servings": 2,
        "notes": "Load up on vegetables. Under 1 tsp oil."
    },
    {
        "name": "Moong daal soup + 1 atta roti + salad",
        "slot": "lunch",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "low_satfat", "light"],
        "carb_servings": 2,
        "notes": "Moong daal is gentle on digestion and blood sugar."
    },
    {
        "name": "Palak (spinach) with paneer or chicken + 1 roti",
        "slot": "lunch",
        "tags": ["desi", "low_satfat", "high_fiber"],
        "carb_servings": 2,
        "notes": "Spinach adds iron and fibre. Light on cream or butter."
    },

    # ── AFTERNOON SNACK (snack_pm) ─────────────────────────────────────────────
    {
        "name": "1 medium guava",
        "slot": "snack_pm",
        "tags": ["veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Best fruit for diabetics — high fibre, low glycemic."
    },
    {
        "name": "Small handful of roasted chana",
        "slot": "snack_pm",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "High protein and fibre. Roasted, not fried."
    },
    {
        "name": "Unsweetened yogurt with cucumber and mint",
        "slot": "snack_pm",
        "tags": ["desi", "veg", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Cooling, filling and blood-sugar friendly."
    },
    {
        "name": "1 small apple + 5 almonds",
        "slot": "snack_pm",
        "tags": ["veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Apple fibre slows sugar absorption. Almonds add healthy fat."
    },
    {
        "name": "Roasted pumpkin seeds (1 small handful)",
        "slot": "snack_pm",
        "tags": ["veg", "low_sodium", "light"],
        "carb_servings": 0,
        "notes": "High in magnesium which helps insulin sensitivity."
    },

    # ── DINNER ────────────────────────────────────────────────────────────────
    {
        "name": "Baked or grilled fish + raita + green salad",
        "slot": "dinner",
        "tags": ["desi", "low_satfat", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "No frying. Lemon and herbs for flavour."
    },
    {
        "name": "Daal tadka + 1 atta roti + cucumber slices",
        "slot": "dinner",
        "tags": ["desi", "veg", "high_fiber", "low_sodium"],
        "carb_servings": 2,
        "notes": "Minimal ghee in tadka. Garlic and cumin help blood sugar."
    },
    {
        "name": "Chicken karahi (less oil) + 1 atta roti + salad",
        "slot": "dinner",
        "tags": ["desi", "low_satfat"],
        "carb_servings": 2,
        "notes": "Ask for less oil. Atta roti instead of naan."
    },
    {
        "name": "Palak chicken + 1 roti + raita",
        "slot": "dinner",
        "tags": ["desi", "low_satfat", "high_fiber"],
        "carb_servings": 2,
        "notes": "Light on cream or butter. Spinach adds fibre."
    },
    {
        "name": "Vegetable pulao (small portion) + plain yogurt + salad",
        "slot": "dinner",
        "tags": ["desi", "veg", "low_satfat"],
        "carb_servings": 3,
        "notes": "One small katori of rice. Load the salad side."
    },
    {
        "name": "Masoor daal + 1 roti + tomato-onion salad",
        "slot": "dinner",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 2,
        "notes": "Red lentils are rich in protein and fibre. Light and easy to digest."
    },

    # ── BEDTIME SNACK (snack_bed) ──────────────────────────────────────────────
    # Small, slow-release — prevents overnight hypo for insulin users
    {
        "name": "1 small glass warm low-fat milk (unsweetened)",
        "slot": "snack_bed",
        "tags": ["veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Slow-release protein. Helps prevent overnight blood sugar drops."
    },
    {
        "name": "2 whole wheat crackers + 1 tsp peanut butter",
        "slot": "snack_bed",
        "tags": ["veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Carb + protein combination keeps blood sugar stable overnight."
    },
    {
        "name": "Small bowl of unsweetened yogurt + 5 almonds",
        "slot": "snack_bed",
        "tags": ["desi", "veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Protein slows overnight glucose drop. Good for insulin users."
    },
    {
        "name": "Half a small apple + a few walnuts",
        "slot": "snack_bed",
        "tags": ["veg", "high_fiber", "low_sodium"],
        "carb_servings": 1,
        "notes": "Light and satisfying. Walnuts add omega-3 and slow sugar release."
    },
]

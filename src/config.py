# src/config.py
CHANNEL_LIMITS = {
    "快递": {"max_weight": 24, "max_circumference": 290, "vol_weight_divisor": 5000},
    "海运": {"max_weight": 22, "max_circumference": 260, "vol_weight_divisor": 6000},
    "空运": {"max_weight": 22, "max_circumference": 260, "vol_weight_divisor": 6000},
}

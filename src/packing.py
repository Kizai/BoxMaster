# src/packing.py
import pandas as pd
from src.config import CHANNEL_LIMITS

def optimize_packing(channel, skus, box_length, box_width, box_height, box_weight, price_per_kg):
    if not skus:
        return "请至少输入一个SKU", None

    if channel not in CHANNEL_LIMITS:
        return "无效的渠道选择", None

    results = []
    max_volume = box_length * box_width * box_height
    max_weight = CHANNEL_LIMITS[channel]["max_weight"] - box_weight
    max_circumference = CHANNEL_LIMITS[channel]["max_circumference"]
    vol_weight_divisor = CHANNEL_LIMITS[channel]["vol_weight_divisor"]
    total_quantity = 0
    total_weight = 0

    sku_count = len(skus)
    quantity_limit = 30 if sku_count >= 3 else float('inf')

    for sku in skus:
        sku_id, length, width, height, weight = sku

        try:
            length = abs(float(length))
            width = abs(float(width))
            height = abs(float(height))
            weight = abs(float(weight))

            if length <= 0 or width <= 0 or height <= 0 or weight <= 0:
                return f"输入值错误，请确保 SKU: {sku_id} 的长、宽、高、重量为正数", None

        except (ValueError, TypeError):
            return f"输入值错误，请检查 SKU: {sku_id} 的长、宽、高、重量是否为有效数字", None

        dimensions = sorted([length, width, height])
        circumference = 2 * (dimensions[0] + dimensions[1]) + dimensions[2]

        if circumference > max_circumference:
            results.append([sku_id, 0, weight, f"物品周长超过 {channel} 规格限制 ({max_circumference} cm)"])
            continue

        if length > box_length or width > box_width or height > box_height:
            results.append([sku_id, 0, weight, "物品尺寸超过箱子规格"])
            continue

        volume = length * width * height

        if volume > max_volume or weight > max_weight:
            results.append([sku_id, 0, weight, "物品重量或体积超过箱子规格"])
            continue

        max_by_volume = max_volume // volume
        max_by_weight = max_weight // weight
        max_sku_count = int(min(max_by_volume, max_by_weight))

        if sku_count >= 3:
            max_sku_count = min(max(max_sku_count, 5), quantity_limit)
        else:
            max_sku_count = max(max_sku_count, 5)

        if total_weight + (max_sku_count * weight) + box_weight > CHANNEL_LIMITS[channel]["max_weight"]:
            max_sku_count = int((CHANNEL_LIMITS[channel]["max_weight"] - total_weight - box_weight) // weight)
            max_sku_count = max(max(max_sku_count, 5), 5)
            if max_sku_count < 5:
                results.append([sku_id, 0, weight, "无法装载至少 5 个数量而不超重"])
                continue

        results.append([sku_id, max_sku_count, weight, ""])
        total_quantity += max_sku_count
        total_weight += max_sku_count * weight

    # 调整数量以确保总重量不超过渠道限制
    for i in range(len(results)):
        while total_weight + box_weight > CHANNEL_LIMITS[channel]["max_weight"] and results[i][1] > 5:
            results[i][1] -= 1
            total_weight -= results[i][2]
            total_quantity -= 1
            if results[i][1] < 0:
                results[i][1] = 0

    # 计算体积重
    volumetric_weight = (box_length * box_width * box_height) / vol_weight_divisor
    chargeable_weight = max(total_weight + box_weight, volumetric_weight)

    # 根据计费重量计算费用
    total_cost = chargeable_weight * price_per_kg
    cost_per_item = total_cost / total_quantity if total_quantity > 0 else 0

    # 检查是否存在超重费用
    overweight_fee_notice = ""
    if total_weight + box_weight > CHANNEL_LIMITS[channel]["max_weight"]:
        overweight_fee_notice = f"\n- **注意**: 超过 {CHANNEL_LIMITS[channel]['max_weight']} kg 的重量限制，将会收取额外的超重费用。"

    # 检查箱子周长是否超过限制并添加警告
    dimensions = sorted([box_length, box_width, box_height])
    box_circumference = 2 * (dimensions[0] + dimensions[1]) + dimensions[2]
    oversized_warning = (
        f"\n- **注意**: 箱规周长为 {box_circumference:.2f} cm，超过 {max_circumference} cm 的限制。"
        " 可能会有超周长费用。" if box_circumference > max_circumference else ""
    )

    # 创建 DataFrame 并输出结果
    df = pd.DataFrame(results, columns=["SKU-ID", "最大数量", "重量(kg)", "备注"])
    summary = (
        f"\n\n- **预估总数量**: {total_quantity}\n"
        f"- **预估总重量**: {total_weight + box_weight:.2f} kg\n"
        f"- **体积重**: {volumetric_weight:.2f} kg\n"
        f"- **计费重量**: {chargeable_weight:.2f} kg\n"
        f"- **单箱预估费用**: ¥{total_cost:.2f}\n"
        f"- **每件预估费用**: ¥{cost_per_item:.2f}"
        + oversized_warning
        + overweight_fee_notice
    )
    output = df.to_markdown(index=False) + summary
    return output, df

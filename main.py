import gradio as gr
import pandas as pd
from io import BytesIO
import tempfile
import os

try:
    from tabulate import tabulate
except ImportError:
    raise ImportError("Missing optional dependency 'tabulate'. Use pip or conda to install tabulate.")

try:
    import xlsxwriter
except ImportError:
    raise ImportError("Missing optional dependency 'xlsxwriter'. Use pip或conda to install xlsxwriter.")

try:
    import openpyxl
except ImportError:
    raise ImportError("Missing optional dependency 'openpyxl'. Use pip或conda to install openpyxl.")

# 禁用 Gradio 分析请求
# gr.analytics.disable_analytics()

# Channel weight limits and circumference constraints
CHANNEL_LIMITS = {
    "快递": {"max_weight": 24, "max_circumference": 290, "vol_weight_divisor": 5000},
    "海运": {"max_weight": 22, "max_circumference": 260, "vol_weight_divisor": 6000},
    "空运": {"max_weight": 22, "max_circumference": 260, "vol_weight_divisor": 6000}
}

def optimize_packing(channel, skus, box_length, box_width, box_height, box_weight, price_per_kg):
    # Check if there are SKU entries
    if not skus:
        return "请至少输入一个SKU", None
    
    # Check if channel is valid
    if channel not in CHANNEL_LIMITS:
        return "无效的渠道选择", None
    
    results = []
    max_volume = box_length * box_width * box_height
    max_weight = CHANNEL_LIMITS[channel]["max_weight"] - box_weight
    max_circumference = CHANNEL_LIMITS[channel]["max_circumference"]
    vol_weight_divisor = CHANNEL_LIMITS[channel]["vol_weight_divisor"]
    total_quantity = 0
    total_weight = 0

    for sku in skus:
        sku_id, length, width, height, weight = sku
        
        # Validate if inputs are within box dimensions and are positive numbers
        try:
            length = abs(float(length))
            width = abs(float(width))
            height = abs(float(height))
            weight = abs(float(weight))

            if length <= 0 or width <= 0 or height <= 0 or weight <= 0:
                return f"输入值错误，请确保 SKU: {sku_id} 的长、宽、高、重量为正数", None

        except (ValueError, TypeError):
            return f"输入值错误，请检查 SKU: {sku_id} 的长、宽、高、重量是否为有效数字", None

        # Calculate circumference as per the specific method
        dimensions = sorted([length, width, height])
        circumference = 2 * (dimensions[0] + dimensions[1]) + dimensions[2]

        # Check if circumference exceeds the channel limits
        if circumference > max_circumference:
            results.append([sku_id, weight, 0, f"物品周长超过 {channel} 规格限制 ({max_circumference} cm)"])
            continue

        # Check if the item fits the box dimensions
        if length > box_length or width > box_width or height > box_height:
            results.append([sku_id, weight, 0, "物品尺寸超过箱子规格"])
            continue
        
        # Calculate the volume of the current SKU
        volume = length * width * height

        # Ensure at least one SKU can fit in the box
        if volume > max_volume or weight > max_weight:
            results.append([sku_id, weight, 0, "物品重量或体积超过箱子规格"])
            continue

        # Calculate the maximum number of this SKU that can fit in the box
        max_by_volume = max_volume // volume
        max_by_weight = max_weight // weight
        max_sku_count = int(min(max_by_volume, max_by_weight))

        # Set limits: at least 5 and at most 30 per SKU
        max_sku_count = min(max(max_sku_count, 5), 30)

        # Ensure total weight does not exceed the channel limit
        # Ensure total weight does not exceed the channel limit
        if total_weight + (max_sku_count * weight) + box_weight > CHANNEL_LIMITS[channel]["max_weight"]:
            max_sku_count = int((CHANNEL_LIMITS[channel]["max_weight"] - total_weight - box_weight) // weight)
            max_sku_count = min(max(max_sku_count, 5), 30)  # Re-check limits after weight adjustment
            # 如果调整后数量依然不满足最低数量限制，返回错误信息
            if max_sku_count < 5:
                results.append([sku_id, 0, weight, "无法装载至少 5 个数量而不超重"])
                continue


        # 将数量和重量的位置对换
        results.append([sku_id, max_sku_count, weight, ""])
        total_quantity += max_sku_count
        total_weight += max_sku_count * weight

    # Adjust the quantities to ensure total weight does not exceed the channel limit
    for i in range(len(results)):
        while total_weight + box_weight > CHANNEL_LIMITS[channel]["max_weight"] and results[i][1] > 5:
            results[i][1] -= 1  # 减少 SKU 的数量
            total_weight -= results[i][2]  # 更新总重量
            total_quantity -= 1  # 更新总数量

    # Calculate volumetric weight
    volumetric_weight = (box_length * box_width * box_height) / vol_weight_divisor
    chargeable_weight = max(total_weight + box_weight, volumetric_weight)

    # Calculate costs based on chargeable weight
    total_cost = chargeable_weight * price_per_kg
    cost_per_item = total_cost / total_quantity if total_quantity > 0 else 0

    # Check if the box circumference exceeds the limit and add a warning if so
    dimensions = sorted([box_length, box_width, box_height])
    box_circumference = 2 * (dimensions[0] + dimensions[1]) + dimensions[2]
    oversized_warning = (
        f"\n\n**注意**: 箱规周长为 {box_circumference:.2f} cm，超过 {max_circumference} cm 的限制。"
        " 可能会有超周长费用。" if box_circumference > max_circumference else ""
    )

    # Adjusted DataFrame column order: "最大数量" is now before "重量(kg)"
    df = pd.DataFrame(results, columns=["SKU-ID", "最大数量", "重量(kg)", "备注"])
    summary = (
        f"\n\n**预估总数量**: {total_quantity}\n"
        f"**预估总重量**: {total_weight + box_weight:.2f} kg\n"
        f"**体积重**: {volumetric_weight:.2f} kg\n"
        f"**计费重量**: {chargeable_weight:.2f} kg\n"
        f"**单箱预估费用**: ¥{total_cost:.2f}\n"
        f"**每件预估费用**: ¥{cost_per_item:.2f}"
        + oversized_warning
    )
    output = df.to_markdown(index=False) + summary
    return output, df

def save_file(df):
    output = BytesIO()
    df.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)
    
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    with open(temp_file.name, 'wb') as f:
        f.write(output.read())
    
    return temp_file.name

def download_template():
    return "temp/temp.xlsx"

def interface(channel, sku_input, file_input, box_length, box_width, box_height, box_weight, price_per_kg):
    # If a file is uploaded, read it into a DataFrame
    if file_input is not None:
        sku_input = pd.read_excel(file_input)
    
    # Convert the DataFrame-like input to a list of lists
    skus = sku_input.values.tolist() if isinstance(sku_input, pd.DataFrame) else sku_input
    
    validated_skus = []
    for row in skus:
        if len(row) == 5 and all(row):  # Ensure the row has all required fields filled
            try:
                sku_id = str(row[0]).strip()  # Convert SKU ID to string
                length = abs(float(row[1]))
                width = abs(float(row[2]))
                height = abs(float(row[3]))
                weight = abs(float(row[4]))

                # Explicitly validate numerical fields
                if not all(isinstance(x, (int, float)) and x > 0 for x in [length, width, height, weight]):
                    return f"输入值错误，请检查 SKU: {sku_id} 的长、宽、高、重量是否为正数", None

                validated_skus.append([sku_id, length, width, height, weight])
            except (ValueError, TypeError):
                return "输入值错误，请检查所有输入", None
    
    markdown, df = optimize_packing(channel, validated_skus, box_length, box_width, box_height, box_weight, price_per_kg)
    if df is None:
        return markdown, None
    return markdown, save_file(df)

with gr.Blocks() as demo:
    gr.Markdown("## BoxMaster - 货物最佳配货工具\n根据输入的产品规格和渠道选择，自动生成最佳的货物配货方案。\n\n**注意：** 本工具仅供参考，不保证最佳配货结果。\n Designed by [**Kizai**](https://github.com/Kizai)")
    
    with gr.Row():
        channel_input = gr.Radio(choices=["快递", "海运", "空运"], label="选择渠道")
        price_per_kg_input = gr.Number(label="单价 (¥/kg)", value=16)

    with gr.Row():
        box_length_input = gr.Number(label="箱子长度 (cm)", value=60)
        box_width_input = gr.Number(label="箱子宽度 (cm)", value=50)
        box_height_input = gr.Number(label="箱子高度 (cm)", value=40)
        box_weight_input = gr.Number(label="箱子重量 (kg)", value=1.35)

    sku_inputs = gr.Dataframe(
        headers=["SKU ID", "长 (cm)", "宽 (cm)", "高 (cm)", "重量 (kg)"],
        datatype=["str", "number", "number", "number", "number"],
        row_count=1,
        col_count=5,
        label="SKU 输入",
        interactive=True
    )
    file_input = gr.File(label="上传 Excel 文件", type="filepath")
    
    output_markdown = gr.Markdown(label="配货方案")
    output_file = gr.File(label="下载表格")
    
    gr.Button("生成配货方案").click(
        interface, 
        inputs=[channel_input, sku_inputs, file_input, box_length_input, box_width_input, box_height_input, box_weight_input, price_per_kg_input], 
        outputs=[output_markdown, output_file]
    )
    
    gr.Button("下载模板").click(
        download_template, 
        outputs=gr.File(label="模板文件")
    )

demo.launch(share=False, server_name="0.0.0.0")

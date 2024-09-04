# src/app.py
from src.packing import optimize_packing
from src.utils import save_file
import gradio as gr
import pandas as pd

def interface(channel, sku_input, file_input, box_length, box_width, box_height, box_weight, price_per_kg):
    # 如果上传了文件，则读取文件内容
    if file_input is not None:
        try:
            sku_input = pd.read_excel(file_input)
        except Exception as e:
            return f"文件读取错误: {e}", None

    # 转换 DataFrame 输入为列表
    skus = sku_input.values.tolist() if isinstance(sku_input, pd.DataFrame) else sku_input
    validated_skus = []

    for row in skus:
        if len(row) == 5 and all(row):
            try:
                sku_id = str(row[0]).strip()
                length = abs(float(row[1]))
                width = abs(float(row[2]))
                height = abs(float(row[3]))
                weight = abs(float(row[4]))

                if not all(isinstance(x, (int, float)) and x > 0 for x in [length, width, height, weight]):
                    return f"输入值错误，请检查 SKU: {sku_id} 的长、宽、高、重量是否为正数", None

                validated_skus.append([sku_id, length, width, height, weight])
            except (ValueError, TypeError):
                return "输入值错误，请检查所有输入", None

    markdown, df = optimize_packing(channel, validated_skus, box_length, box_width, box_height, box_weight, price_per_kg)
    if df is None:
        return markdown, None
    return markdown, save_file(df)

def main():
    with gr.Blocks() as demo:
        gr.Markdown("## BoxMaster - 货物最佳配货工具\n根据输入的产品规格和渠道选择，自动生成最佳的货物配货方案。\n\n**注意：** 本工具仅供参考，不保证最佳配货结果。\n Designed by [**Kizai**](https://github.com/Kizai/BoxMaster)")
        
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

        # 限制上传的文件格式为 .xlsx
        file_input = gr.File(label="上传 Excel 文件", type="filepath", file_types=[".xlsx"])

        output_markdown = gr.Markdown(label="配货方案")
        output_file = gr.File(label="下载表格")

        gr.Button("生成配货方案").click(
            interface,
            inputs=[channel_input, sku_inputs, file_input, box_length_input, box_width_input, box_height_input, box_weight_input, price_per_kg_input],
            outputs=[output_markdown, output_file]
        )
        
        gr.Button("下载模板").click(
            lambda: "temp/temp.xlsx",
            outputs=gr.File(label="模板文件")
        )

    demo.launch(share=False, server_name="0.0.0.0")

if __name__ == "__main__":
    main()

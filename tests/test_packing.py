import unittest
from src.packing  import optimize_packing  

# terminal直接运行
# python -m unittest test/test_packing.py


class TestOptimizePacking(unittest.TestCase):
    def test_single_sku_normal(self):
        # 单一 SKU 正常情况
        channel = "快递"
        skus = [['SKU1', 20, 15, 10, 2]]
        box_length = 60
        box_width = 50
        box_height = 40
        box_weight = 1.35
        price_per_kg = 16
        
        output, df = optimize_packing(channel, skus, box_length, box_width, box_height, box_weight, price_per_kg)
        print(output)
        self.assertIn("预估总数量", output)

    def test_multiple_skus_close_to_size_limit(self):
        # 多个 SKU，接近尺寸限制
        channel = "海运"
        skus = [['SKU1', 40, 30, 25, 5], ['SKU2', 30, 20, 15, 3], ['SKU3', 10, 10, 10, 1]]
        box_length = 60
        box_width = 50
        box_height = 40
        box_weight = 1.35
        price_per_kg = 10
        
        output, df = optimize_packing(channel, skus, box_length, box_width, box_height, box_weight, price_per_kg)
        print(output)
        self.assertIn("预估总重量", output)

    def test_sku_exceeds_box_size(self):
        # SKU 超过箱子尺寸
        channel = "空运"
        skus = [['SKU1', 70, 60, 50, 10]]  # 尺寸超出箱子规格
        box_length = 60
        box_width = 50
        box_height = 40
        box_weight = 1.35
        price_per_kg = 12
        
        output, df = optimize_packing(channel, skus, box_length, box_width, box_height, box_weight, price_per_kg)
        print(output)
        self.assertIn("物品尺寸超过箱子规格", output)

    def test_single_sku_close_to_circumference_limit(self):
        # 单 SKU，接近周长限制
        channel = "快递"
        skus = [['SKU1', 100, 50, 20, 3]]  # 接近周长限制
        box_length = 120
        box_width = 40
        box_height = 30
        box_weight = 2
        price_per_kg = 14
        
        output, df = optimize_packing(channel, skus, box_length, box_width, box_height, box_weight, price_per_kg)
        print(output)
        self.assertIn("超周长费用", output)

    def test_multiple_skus_near_weight_limit(self):
        # 多个 SKU，总重量接近限制
        channel = "海运"
        skus = [['SKU1', 20, 15, 10, 6], ['SKU2', 30, 20, 15, 7]]  # 重量较大
        box_length = 60
        box_width = 50
        box_height = 40
        box_weight = 1.35
        price_per_kg = 8
        
        output, df = optimize_packing(channel, skus, box_length, box_width, box_height, box_weight, price_per_kg)
        print(output)
        self.assertIn("预估总数量", output)

    def test_single_sku_overweight(self):
        # 单 SKU，超重情况
        channel = "空运"
        skus = [['SKU1', 10, 10, 10, 25]]  # 单个 SKU 超重
        box_length = 60
        box_width = 50
        box_height = 40
        box_weight = 1.35
        price_per_kg = 15
        
        output, df = optimize_packing(channel, skus, box_length, box_width, box_height, box_weight, price_per_kg)
        print(output)
        self.assertIn("超重", output)

if __name__ == "__main__":
    unittest.main()

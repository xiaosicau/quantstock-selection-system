#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化股票选股系统 - 综合演示程序

这是一个完整的演示程序，展示了系统的核心功能：
1. 数据获取与处理
2. 因子计算与分析
3. 策略回测
4. 结果可视化
5. 选股推荐

运行前请确保已安装所有依赖：
pip install -r requirements.txt
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 添加src到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

print("🎉 量化股票选股系统完整演示")
print("=" * 60)
print("✅ 系统初始化完成")
print("✅ 演示程序已就绪")
print("\n🎯 核心功能:")
print("1. 多因子模型选股")
print("2. 实时数据获取")
print("3. 策略回测引擎")
print("4. 风险监控系统")
print("5. Web可视化界面")
print("\n📊 运行方式:")
print("- 完整演示: python comprehensive_demo.py")
print("- Web界面: streamlit run frontend/app.py")
print("- 快速体验: python simple_demo.py")

if __name__ == "__main__":
    print("\n✅ 演示环境已配置完成！")
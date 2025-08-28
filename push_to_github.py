#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub项目上传脚本

用于将本地量化股票选股系统项目上传到GitHub
支持完整项目结构上传
"""

import os
import sys
import subprocess
from pathlib import Path

def upload_to_github():
    """上传项目到GitHub"""
    print("🚀 开始上传项目到GitHub...")
    
    # 检查git状态
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ 当前目录不是git仓库")
            return False
    except FileNotFoundError:
        print("❌ 未找到git命令")
        return False
    
    # 添加所有文件
    print("📁 添加所有文件...")
    subprocess.run(['git', 'add', '.'])
    
    # 提交更改
    print("💾 提交更改...")
    commit_message = "feat: 完整项目初始化上传"
    subprocess.run(['git', 'commit', '-m', commit_message])
    
    # 推送到GitHub
    print("☁️ 推送到GitHub...")
    result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 上传成功！")
        print("📍 项目地址: https://github.com/xiaosicau/quantstock-selection-system")
        return True
    else:
        print(f"❌ 上传失败: {result.stderr}")
        return False

if __name__ == "__main__":
    upload_to_github()
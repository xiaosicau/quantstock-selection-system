#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化股票选股系统 - 应用构建脚本

用于构建和打包量化交易系统的可执行应用
支持Windows、macOS、Linux多平台
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class AppBuilder:
    """应用构建器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        
    def clean_build(self):
        """清理构建目录"""
        print("🧹 清理构建目录...")
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"已删除: {dir_path}")
    
    def install_requirements(self):
        """安装构建依赖"""
        print("📦 安装构建依赖...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_build.txt"], 
                         check=True, capture_output=True)
            print("✅ 构建依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖安装失败: {e}")
            return False
        return True
    
    def build_streamlit_app(self):
        """构建Streamlit应用"""
        print("🏗️ 构建Streamlit应用...")
        
        # 创建启动脚本
        app_script = self.project_root / "run_app.py"
        with open(app_script, 'w') as f:
            f.write("""
import streamlit as st
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并运行主应用
from frontend.app import main
if __name__ == "__main__":
    main()
""")
        
        print("✅ Streamlit应用构建完成")
        return True
    
    def build_executable(self):
        """构建可执行文件"""
        print("🔨 构建可执行文件...")
        
        system = platform.system()
        
        if system == "Windows":
            return self._build_windows()
        elif system == "Darwin":
            return self._build_macos()
        elif system == "Linux":
            return self._build_linux()
        else:
            print(f"❌ 不支持的操作系统: {system}")
            return False
    
    def _build_windows(self):
        """构建Windows可执行文件"""
        print("🪟 构建Windows应用...")
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name", "QuantStock",
            "--add-data", "frontend;frontend",
            "--add-data", "config;config",
            "--add-data", "src;src",
            "run_app.py"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("✅ Windows应用构建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Windows构建失败: {e}")
            return False
    
    def _build_macos(self):
        """构建macOS应用"""
        print("🍎 构建macOS应用...")
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name", "QuantStock",
            "--add-data", "frontend:frontend",
            "--add-data", "config:config",
            "--add-data", "src:src",
            "run_app.py"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("✅ macOS应用构建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ macOS构建失败: {e}")
            return False
    
    def _build_linux(self):
        """构建Linux应用"""
        print("🐧 构建Linux应用...")
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--name", "QuantStock",
            "--add-data", "frontend:frontend",
            "--add-data", "config:config",
            "--add-data", "src:src",
            "run_app.py"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("✅ Linux应用构建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Linux构建失败: {e}")
            return False
    
    def create_installer(self):
        """创建安装程序"""
        print("📦 创建安装程序...")
        
        system = platform.system()
        
        if system == "Windows":
            return self._create_windows_installer()
        elif system == "Darwin":
            return self._create_macos_installer()
        elif system == "Linux":
            return self._create_linux_installer()
        else:
            print(f"❌ 不支持的操作系统: {system}")
            return False
    
    def _create_windows_installer(self):
        """创建Windows安装程序"""
        print("🪟 创建Windows安装程序...")
        
        # 使用Inno Setup创建安装程序
        inno_script = """
[Setup]
AppName=QuantStock Selection System
AppVersion=1.0.0
DefaultDirName={pf}\QuantStock
DefaultGroupName=QuantStock
OutputDir=dist
OutputBaseFilename=QuantStock-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist/QuantStock.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "frontend/*"; DestDir: "{app}/frontend"; Flags: ignoreversion recursesubdirs
Source: "config/*"; DestDir: "{app}/config"; Flags: ignoreversion recursesubdirs
Source: "src/*"; DestDir: "{app}/src"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\QuantStock"; Filename: "{app}/QuantStock.exe"
Name: "{commondesktop}\QuantStock"; Filename: "{app}/QuantStock.exe"
"""
        
        with open('installer/windows_installer.iss', 'w') as f:
            f.write(inno_script)
        
        print("✅ Windows安装程序脚本已生成")
        print("请使用Inno Setup编译 installer/windows_installer.iss")
        return True
    
    def _create_macos_installer(self):
        """创建macOS安装程序"""
        print("🍎 创建macOS安装程序...")
        
        # 创建应用包
        app_dir = self.dist_dir / "QuantStock.app"
        if app_dir.exists():
            shutil.rmtree(app_dir)
        
        # 创建应用目录结构
        contents_dir = app_dir / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        macos_dir.mkdir(parents=True)
        resources_dir.mkdir(parents=True)
        
        # 复制可执行文件
        if (self.dist_dir / "QuantStock").exists():
            shutil.copy(self.dist_dir / "QuantStock", macos_dir / "QuantStock")
            os.chmod(macos_dir / "QuantStock", 0o755)
        
        # 创建Info.plist
        info_plist = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>QuantStock</string>
    <key>CFBundleIdentifier</key>
    <string>com.quantstock.app</string>
    <key>CFBundleName</key>
    <string>QuantStock</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.12</string>
</dict>
</plist>
"""
        
        with open(contents_dir / "Info.plist", 'w') as f:
            f.write(info_plist)
        
        print("✅ macOS应用包已创建")
        return True
    
    def _create_linux_installer(self):
        """创建Linux安装程序"""
        print("🐧 创建Linux安装程序...")
        
        # 创建安装脚本
        install_script = """#!/bin/bash
# QuantStock Linux安装脚本

echo "安装 QuantStock Selection System..."

# 创建安装目录
INSTALL_DIR="/opt/quantstock"
sudo mkdir -p $INSTALL_DIR

# 复制文件
sudo cp dist/QuantStock $INSTALL_DIR/
sudo cp -r frontend $INSTALL_DIR/
sudo cp -r config $INSTALL_DIR/
sudo cp -r src $INSTALL_DIR/

# 创建符号链接
sudo ln -sf $INSTALL_DIR/QuantStock /usr/local/bin/quantstock

echo "安装完成！"
echo "运行: quantstock"
"""
        
        with open('installer/create_linux_installer.sh', 'w') as f:
            f.write(install_script)
        
        os.chmod('installer/create_linux_installer.sh', 0o755)
        print("✅ Linux安装脚本已生成")
        return True
    
    def run_full_build(self):
        """运行完整构建流程"""
        print("🚀 开始完整构建流程...")
        
        # 清理旧构建
        self.clean_build()
        
        # 安装依赖
        if not self.install_requirements():
            return False
        
        # 构建应用
        if not self.build_streamlit_app():
            return False
        
        # 构建可执行文件
        if not self.build_executable():
            return False
        
        # 创建安装程序
        if not self.create_installer():
            return False
        
        print("\n🎉 构建完成！")
        print("📁 输出目录: ./dist/")
        print("📦 安装程序: ./installer/")
        
        return True

if __name__ == "__main__":
    """主程序入口"""
    builder = AppBuilder()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            builder.run_full_build()
        elif sys.argv[1] == "clean":
            builder.clean_build()
        else:
            print("用法: python build_app.py [build|clean]")
    else:
        builder.run_full_build()
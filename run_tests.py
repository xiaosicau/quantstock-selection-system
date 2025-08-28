#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行器 - 一键运行所有测试

使用方法:
python run_tests.py          # 运行所有测试
python run_tests.py --unit   # 只运行单元测试
python run_tests.py --cov    # 运行测试并生成覆盖率报告
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

def run_command(cmd, description=""):
    """运行命令并处理错误"""
    print(f"🚀 {description}")
    print(f"   命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 失败")
        print(f"   错误: {e.stderr}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🧪 开始运行测试套件...")
    print("=" * 60)
    
    # 设置环境变量
    os.environ['PYTHONPATH'] = str(Path(__file__).parent)
    
    # 运行pytest
    cmd = [sys.executable, '-m', 'pytest', 'tests/', '-v']
    return run_command(cmd, "运行所有测试")

def run_unit_tests():
    """运行单元测试"""
    print("🔬 运行单元测试...")
    cmd = [sys.executable, '-m', 'pytest', 'tests/', '-v', '-k', 'not integration']
    return run_command(cmd, "运行单元测试")

def run_integration_tests():
    """运行集成测试"""
    print("🔗 运行集成测试...")
    cmd = [sys.executable, '-m', 'pytest', 'tests/', '-v', '-k', 'integration']
    return run_command(cmd, "运行集成测试")

def run_coverage_report():
    """运行测试覆盖率报告"""
    print("📊 生成测试覆盖率报告...")
    
    # 运行带覆盖率的测试
    cmd = [
        sys.executable, '-m', 'pytest', 'tests/', 
        '--cov=src', '--cov-report=html', '--cov-report=term'
    ]
    
    success = run_command(cmd, "运行测试覆盖率")
    
    if success:
        print("\n📁 覆盖率报告已生成:")
        print("   HTML报告: htmlcov/index.html")
        print("   终端报告: 见上方输出")
    
    return success

def run_linting():
    """运行代码质量检查"""
    print("🔍 运行代码质量检查...")
    
    # 检查代码格式
    success = True
    
    # 运行black检查
    cmd = ['black', '--check', 'src/', 'tests/', 'frontend/']
    success &= run_command(cmd, "检查代码格式")
    
    # 运行flake8检查
    cmd = ['flake8', 'src/', 'tests/', 'frontend/']
    success &= run_command(cmd, "检查代码风格")
    
    # 运行mypy类型检查
    cmd = ['mypy', 'src/']
    success &= run_command(cmd, "检查类型注解")
    
    return success

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='运行测试套件')
    parser.add_argument('--unit', action='store_true', help='只运行单元测试')
    parser.add_argument('--integration', action='store_true', help='只运行集成测试')
    parser.add_argument('--cov', action='store_true', help='生成覆盖率报告')
    parser.add_argument('--lint', action='store_true', help='运行代码质量检查')
    parser.add_argument('--all', action='store_true', help='运行所有检查')
    
    args = parser.parse_args()
    
    if not any([args.unit, args.integration, args.cov, args.lint, args.all]):
        # 默认运行所有测试
        success = run_all_tests()
    else:
        success = True
        
        if args.all:
            success &= run_all_tests()
            success &= run_coverage_report()
            success &= run_linting()
        else:
            if args.unit:
                success &= run_unit_tests()
            if args.integration:
                success &= run_integration_tests()
            if args.cov:
                success &= run_coverage_report()
            if args.lint:
                success &= run_linting()
    
    if success:
        print("\n🎉 所有测试完成！")
    else:
        print("\n❌ 部分测试失败，请查看错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
量化选股系统项目验证脚本
QuantStock Project Validation Script

该脚本用于验证项目完整性和功能正确性
"""

import os
import sys
import json
import importlib
import subprocess
from pathlib import Path
from datetime import datetime
import yaml

class ProjectValidator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.validation_report = {
            "timestamp": datetime.now().isoformat(),
            "project_name": "量化选股系统",
            "version": "1.0.0",
            "checks": {},
            "results": {},
            "recommendations": []
        }
        self.errors = []
        self.warnings = []
        
    def log_info(self, message):
        """记录信息"""
        print(f"ℹ {message}")
    
    def log_success(self, message):
        """记录成功"""
        print(f"✅ {message}")
    
    def log_warning(self, message):
        """记录警告"""
        print(f"⚠ {message}")
        self.warnings.append(message)
    
    def log_error(self, message):
        """记录错误"""
        print(f"❌ {message}")
        self.errors.append(message)
    
    def check_file_structure(self):
        """检查文件结构完整性"""
        self.log_info("检查文件结构...")
        
        required_files = [
            "README.md",
            "requirements.txt",
            "config/config.yaml",
            "simple_demo.py",
            "comprehensive_demo.py",
            "frontend/app.py",
            "src/__init__.py",
            "src/data/__init__.py",
            "src/data/data_manager.py",
            "src/backtest/__init__.py",
            "src/backtest/backtest_engine.py",
            "src/factor/__init__.py",
            "src/factor/factor_engine.py",
            "src/api/__init__.py",
            "src/api/rest_api.py",
            "src/utils/__init__.py",
            "src/utils/logger.py",
            "src/utils/config_manager.py",
            "tests/__init__.py",
            "tests/test_data_manager.py",
            "tests/test_backtest_engine.py",
            "tests/test_factor_engine.py",
            "installer/windows_installer.iss",
            "installer/create_macos_installer.sh",
            "installer/create_linux_installer.sh",
            "deploy.py",
            "validate_project.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log_error(f"缺失文件: {', '.join(missing_files)}")
            self.validation_report["checks"]["file_structure"] = False
            self.validation_report["recommendations"].extend([
                f"创建缺失文件: {file}" for file in missing_files
            ])
            return False
        else:
            self.log_success("文件结构完整")
            self.validation_report["checks"]["file_structure"] = True
            return True
    
    def check_python_modules(self):
        """检查Python模块导入"""
        self.log_info("检查Python模块...")
        
        modules_to_check = [
            "src.data.data_manager",
            "src.backtest.backtest_engine",
            "src.factor.factor_engine",
            "src.api.rest_api",
            "src.utils.logger",
            "src.utils.config_manager"
        ]
        
        failed_imports = []
        for module_name in modules_to_check:
            try:
                importlib.import_module(module_name)
                self.log_success(f"模块 {module_name} 导入成功")
            except ImportError as e:
                failed_imports.append(f"{module_name}: {str(e)}")
        
        if failed_imports:
            self.log_error(f"模块导入失败: {', '.join(failed_imports)}")
            self.validation_report["checks"]["python_modules"] = False
            self.validation_report["recommendations"].extend([
                f"修复模块导入: {error}" for error in failed_imports
            ])
            return False
        else:
            self.log_success("所有模块导入成功")
            self.validation_report["checks"]["python_modules"] = True
            return True
    
    def check_dependencies(self):
        """检查依赖包"""
        self.log_info("检查依赖包...")
        
        required_packages = [
            "pandas",
            "numpy",
            "streamlit",
            "fastapi",
            "uvicorn",
            "pydantic",
            "akshare",
            "matplotlib",
            "seaborn",
            "pyyaml",
            "pytest"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                importlib.import_module(package)
                self.log_success(f"包 {package} 已安装")
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.log_warning(f"缺失依赖包: {', '.join(missing_packages)}")
            self.validation_report["checks"]["dependencies"] = "warning"
            self.validation_report["recommendations"].append(
                f"安装缺失依赖: pip install {' '.join(missing_packages)}"
            )
            return "warning"
        else:
            self.log_success("所有依赖包已安装")
            self.validation_report["checks"]["dependencies"] = True
            return True
    
    def check_configuration(self):
        """检查配置文件"""
        self.log_info("检查配置文件...")
        
        config_file = self.project_root / "config" / "config.yaml"
        
        if not config_file.exists():
            self.log_error("配置文件不存在")
            self.validation_report["checks"]["configuration"] = False
            return False
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            required_sections = ["data_sources", "factors", "backtest", "risk_management"]
            missing_sections = [section for section in required_sections if section not in config]
            
            if missing_sections:
                self.log_warning(f"配置缺失章节: {', '.join(missing_sections)}")
                self.validation_report["checks"]["configuration"] = "warning"
                self.validation_report["recommendations"].extend([
                    f"添加配置章节: {section}" for section in missing_sections
                ])
                return "warning"
            else:
                self.log_success("配置文件完整")
                self.validation_report["checks"]["configuration"] = True
                return True
                
        except Exception as e:
            self.log_error(f"配置文件解析错误: {e}")
            self.validation_report["checks"]["configuration"] = False
            return False
    
    def check_demo_scripts(self):
        """检查演示脚本"""
        self.log_info("检查演示脚本...")
        
        demo_scripts = [
            "simple_demo.py",
            "comprehensive_demo.py"
        ]
        
        issues = []
        for script in demo_scripts:
            script_path = self.project_root / script
            if not script_path.exists():
                issues.append(f"演示脚本 {script} 不存在")
                continue
            
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查基本结构
                if "import" not in content:
                    issues.append(f"演示脚本 {script} 缺少导入语句")
                
                if "__main__" not in content and "def main" not in content:
                    issues.append(f"演示脚本 {script} 缺少主函数")
                    
            except Exception as e:
                issues.append(f"演示脚本 {script} 读取错误: {e}")
        
        if issues:
            self.log_warning(f"演示脚本问题: {', '.join(issues)}")
            self.validation_report["checks"]["demo_scripts"] = "warning"
            self.validation_report["recommendations"].extend(issues)
            return "warning"
        else:
            self.log_success("演示脚本检查通过")
            self.validation_report["checks"]["demo_scripts"] = True
            return True
    
    def check_api_service(self):
        """检查API服务"""
        self.log_info("检查API服务...")
        
        api_file = self.project_root / "src" / "api" / "rest_api.py"
        
        if not api_file.exists():
            self.log_error("API服务文件不存在")
            self.validation_report["checks"]["api_service"] = False
            return False
        
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查API服务基本结构
            checks = [
                ("fastapi", "FastAPI" in content),
                ("uvicorn", "uvicorn" in content.lower()),
                ("endpoints", "@app.get" in content or "@app.post" in content),
                ("cors", "cors" in content.lower() or "CORSMiddleware" in content)
            ]
            
            missing = [check[0] for check in checks if not check[1]]
            
            if missing:
                self.log_warning(f"API服务可能缺少: {', '.join(missing)}")
                self.validation_report["checks"]["api_service"] = "warning"
                self.validation_report["recommendations"].extend([
                    f"完善API服务: {item}" for item in missing
                ])
                return "warning"
            else:
                self.log_success("API服务结构完整")
                self.validation_report["checks"]["api_service"] = True
                return True
                
        except Exception as e:
            self.log_error(f"API服务检查错误: {e}")
            self.validation_report["checks"]["api_service"] = False
            return False
    
    def check_installer_scripts(self):
        """检查安装脚本"""
        self.log_info("检查安装脚本...")
        
        installer_dir = self.project_root / "installer"
        
        if not installer_dir.exists():
            self.log_error("安装脚本目录不存在")
            self.validation_report["checks"]["installer_scripts"] = False
            return False
        
        required_scripts = [
            "windows_installer.iss",
            "create_macos_installer.sh",
            "create_linux_installer.sh"
        ]
        
        missing_scripts = []
        for script in required_scripts:
            script_path = installer_dir / script
            if not script_path.exists():
                missing_scripts.append(script)
                continue
            
            # 检查脚本可执行性
            if script.endswith('.sh'):
                try:
                    os.chmod(script_path, 0o755)
                except Exception:
                    pass
        
        if missing_scripts:
            self.log_error(f"缺失安装脚本: {', '.join(missing_scripts)}")
            self.validation_report["checks"]["installer_scripts"] = False
            return False
        else:
            self.log_success("所有安装脚本存在")
            self.validation_report["checks"]["installer_scripts"] = True
            return True
    
    def check_documentation(self):
        """检查文档完整性"""
        self.log_info("检查文档完整性...")
        
        required_docs = [
            "README.md",
            "QUICK_START.md",
            "INSTALLER_GUIDE.md",
            "LICENSE"
        ]
        
        missing_docs = []
        for doc in required_docs:
            doc_path = self.project_root / doc
            if not doc_path.exists():
                missing_docs.append(doc)
        
        if missing_docs:
            self.log_warning(f"缺失文档: {', '.join(missing_docs)}")
            self.validation_report["checks"]["documentation"] = "warning"
            self.validation_report["recommendations"].extend([
                f"创建缺失文档: {doc}" for doc in missing_docs
            ])
            return "warning"
        else:
            self.log_success("文档完整")
            self.validation_report["checks"]["documentation"] = True
            return True
    
    def run_all_checks(self):
        """运行所有检查"""
        print("=" * 60)
        print("量化选股系统项目验证")
        print("=" * 60)
        print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        checks = [
            ("文件结构", self.check_file_structure),
            ("Python模块", self.check_python_modules),
            ("依赖包", self.check_dependencies),
            ("配置文件", self.check_configuration),
            ("演示脚本", self.check_demo_scripts),
            ("API服务", self.check_api_service),
            ("安装脚本", self.check_installer_scripts),
            ("文档完整性", self.check_documentation)
        ]
        
        results = {}
        
        for check_name, check_func in checks:
            try:
                result = check_func()
                results[check_name] = result
                
                if result is True:
                    self.validation_report["results"][check_name] = "PASS"
                elif result == "warning":
                    self.validation_report["results"][check_name] = "WARNING"
                else:
                    self.validation_report["results"][check_name] = "FAIL"
                    
            except Exception as e:
                self.log_error(f"检查 {check_name} 时发生异常: {e}")
                results[check_name] = False
                self.validation_report["results"][check_name] = "ERROR"
        
        # 生成验证报告
        self.generate_report(results)
        
        return results
    
    def generate_report(self, results):
        """生成验证报告"""
        report_file = self.project_root / "VALIDATION_REPORT.json"
        
        # 计算统计信息
        total_checks = len(results)
        passed_checks = sum(1 for r in results.values() if r is True)
        warning_checks = sum(1 for r in results.values() if r == "warning")
        failed_checks = total_checks - passed_checks - warning_checks
        
        self.validation_report["summary"] = {
            "total_checks": total_checks,
            "passed": passed_checks,
            "warnings": warning_checks,
            "failed": failed_checks,
            "success_rate": passed_checks / total_checks * 100
        }
        
        # 生成文本报告
        text_report = f"""# 项目验证报告

## 验证概览
- **总检查项**: {total_checks}
- **通过**: {passed_checks}
- **警告**: {warning_checks}
- **失败**: {failed_checks}
- **成功率**: {passed_checks/total_checks*100:.1f}%

## 详细结果
{chr(10).join(f"- {name}: {result}" for name, result in results.items())}

## 建议
{chr(10).join(f"- {rec}" for rec in self.validation_report["recommendations"])}

## 错误信息
{chr(10).join(f"- {error}" for error in self.errors) if self.errors else "无错误"}

## 警告信息
{chr(10).join(f"- {warning}" for warning in self.warnings) if self.warnings else "无警告"}
"""
        
        # 保存报告
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.validation_report, f, indent=2, ensure_ascii=False)
        
        with open("VALIDATION_REPORT.md", 'w', encoding='utf-8') as f:
            f.write(text_report)
        
        return report_file
    
    def print_summary(self, results):
        """打印验证总结"""
        print("\n" + "=" * 60)
        print("验证总结")
        print("=" * 60)
        
        for check_name, result in results.items():
            status = {
                True: "✅ 通过",
                "warning": "⚠ 警告",
                False: "❌ 失败",
                "ERROR": "❌ 错误"
            }.get(result, "❓ 未知")
            print(f"{check_name}: {status}")
        
        passed = sum(1 for r in results.values() if r is True)
        total = len(results)
        
        print(f"\n总计: {passed}/{total} 检查通过 ({passed/total*100:.1f}%)")
        
        if self.errors:
            print(f"\n错误 ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\n警告 ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        print("\n验证报告已保存到:")
        print("  - VALIDATION_REPORT.json (详细JSON格式)")
        print("  - VALIDATION_REPORT.md (可读Markdown格式)")

def main():
    """主函数"""
    validator = ProjectValidator()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            # 快速验证
            validator.check_file_structure()
            validator.check_python_modules()
            validator.check_dependencies()
            print("快速验证完成")
            return
        elif sys.argv[1] == "--help":
            print("用法: python validate_project.py [选项]")
            print("选项:")
            print("  --quick    快速验证（只检查基本结构）")
            print("  --help     显示帮助信息")
            print("  无参数     完整验证")
            return
    
    # 运行完整验证
    results = validator.run_all_checks()
    validator.print_summary(results)

if __name__ == "__main__":
    main()
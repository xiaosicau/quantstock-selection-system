#!/bin/bash
# 量化选股系统 macOS 安装程序创建脚本
# QuantStock macOS Installer Creation Script

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================"
echo "量化选股系统 macOS 安装程序创建工具"
echo "QuantStock macOS Installer Creator"
echo -e "======================================${NC}"

# 配置变量
APP_NAME="量化选股系统"
APP_NAME_EN="QuantStock"
VERSION="1.0.0"
IDENTIFIER="com.quantstock.app"
AUTHOR="量化分析团队"

# 路径配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_ROOT/dist"
APP_PATH="$DIST_DIR/$APP_NAME.app"
DMG_NAME="$APP_NAME_EN-$VERSION-macOS"
DMG_PATH="$DIST_DIR/$DMG_NAME.dmg"
TEMP_DMG_DIR="/tmp/quantstock_dmg"

echo -e "${YELLOW}项目路径: $PROJECT_ROOT${NC}"
echo -e "${YELLOW}应用路径: $APP_PATH${NC}"

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}检查系统依赖...${NC}"
    
    # 检查是否有create-dmg工具
    if ! command -v create-dmg &> /dev/null; then
        echo -e "${YELLOW}安装 create-dmg 工具...${NC}"
        if command -v brew &> /dev/null; then
            brew install create-dmg
        else
            echo -e "${RED}错误: 需要安装 Homebrew 和 create-dmg${NC}"
            echo "请执行: brew install create-dmg"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✓ 依赖检查完成${NC}"
}

# 检查应用程序包
check_app_bundle() {
    echo -e "${BLUE}检查应用程序包...${NC}"
    
    if [ ! -d "$APP_PATH" ]; then
        echo -e "${RED}错误: 找不到应用程序包 $APP_PATH${NC}"
        echo "请先运行构建脚本生成应用程序包"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 应用程序包检查完成${NC}"
}

# 应用程序签名 (可选)
sign_app() {
    echo -e "${BLUE}应用程序签名...${NC}"
    
    # 检查是否有开发者证书
    DEVELOPER_ID=$(security find-identity -v -p codesigning | grep "Developer ID Application" | head -1 | cut -d '"' -f 2)
    
    if [ -n "$DEVELOPER_ID" ]; then
        echo -e "${YELLOW}找到开发者证书: $DEVELOPER_ID${NC}"
        echo -e "${YELLOW}正在签名应用程序...${NC}"
        
        # 签名应用程序
        codesign --force --deep --sign "$DEVELOPER_ID" "$APP_PATH"
        
        # 验证签名
        if codesign --verify --deep --strict "$APP_PATH"; then
            echo -e "${GREEN}✓ 应用程序签名成功${NC}"
        else
            echo -e "${YELLOW}⚠ 应用程序签名验证失败${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ 未找到开发者证书，跳过签名${NC}"
        echo -e "${YELLOW}  应用程序仍可正常使用，但可能显示安全警告${NC}"
    fi
}

# 创建DMG背景和图标
setup_dmg_assets() {
    echo -e "${BLUE}准备DMG资源...${NC}"
    
    # 创建临时目录
    rm -rf "$TEMP_DMG_DIR"
    mkdir -p "$TEMP_DMG_DIR"
    
    # 复制应用程序
    cp -R "$APP_PATH" "$TEMP_DMG_DIR/"
    
    # 创建应用程序文件夹快捷方式
    ln -s /Applications "$TEMP_DMG_DIR/Applications"
    
    # 创建README文件
    cat > "$TEMP_DMG_DIR/使用说明.txt" << EOF
量化选股系统 v$VERSION

安装说明:
1. 将"$APP_NAME"拖拽到"Applications"文件夹
2. 从启动台或应用程序文件夹启动应用程序
3. 首次启动可能需要在"系统偏好设置 > 安全性与隐私"中允许运行

使用指南:
- 快速开始: 查看项目中的 QUICK_START.md
- 详细文档: 查看项目中的 INSTALLER_GUIDE.md
- 技术支持: $AUTHOR

注意事项:
- 需要网络连接以获取股票数据
- 建议使用macOS 10.13或更高版本
- 首次运行可能需要安装依赖库

开发团队: $AUTHOR
版本: $VERSION
日期: $(date '+%Y-%m-%d')
EOF
    
    echo -e "${GREEN}✓ DMG资源准备完成${NC}"
}

# 创建DMG文件
create_dmg_file() {
    echo -e "${BLUE}创建DMG安装包...${NC}"
    
    # 删除已存在的DMG文件
    [ -f "$DMG_PATH" ] && rm "$DMG_PATH"
    
    # 使用create-dmg创建DMG
    create-dmg \
        --volname "$APP_NAME v$VERSION" \
        --volicon "$PROJECT_ROOT/assets/icon.icns" \
        --background "$PROJECT_ROOT/assets/dmg_background.png" \
        --window-pos 200 120 \
        --window-size 800 600 \
        --icon-size 100 \
        --icon "$APP_NAME.app" 200 190 \
        --hide-extension "$APP_NAME.app" \
        --app-drop-link 600 185 \
        --text-size 16 \
        "$DMG_PATH" \
        "$TEMP_DMG_DIR/" \
        || {
            echo -e "${YELLOW}⚠ create-dmg失败，使用hdiutil创建简单DMG${NC}"
            
            # fallback: 使用hdiutil创建简单DMG
            hdiutil create -volname "$APP_NAME" -srcfolder "$TEMP_DMG_DIR" -ov -format UDZO "$DMG_PATH"
        }
    
    if [ -f "$DMG_PATH" ]; then
        echo -e "${GREEN}✓ DMG文件创建成功: $DMG_PATH${NC}"
        
        # 显示文件大小
        DMG_SIZE=$(du -h "$DMG_PATH" | cut -f1)
        echo -e "${GREEN}  文件大小: $DMG_SIZE${NC}"
    else
        echo -e "${RED}✗ DMG文件创建失败${NC}"
        exit 1
    fi
}

# 清理临时文件
cleanup() {
    echo -e "${BLUE}清理临时文件...${NC}"
    rm -rf "$TEMP_DMG_DIR"
    echo -e "${GREEN}✓ 清理完成${NC}"
}

# 创建安装脚本
create_install_script() {
    echo -e "${BLUE}创建安装脚本...${NC}"
    
    INSTALL_SCRIPT="$DIST_DIR/install_macos.sh"
    
    cat > "$INSTALL_SCRIPT" << 'EOF'
#!/bin/bash
# 量化选股系统 macOS 安装脚本

APP_NAME="量化选股系统"
DMG_NAME="QuantStock-1.0.0-macOS.dmg"

echo "======================================"
echo "量化选股系统 macOS 安装程序"
echo "======================================"

# 检查DMG文件
if [ ! -f "$DMG_NAME" ]; then
    echo "错误: 找不到安装文件 $DMG_NAME"
    exit 1
fi

echo "正在挂载安装映像..."
hdiutil attach "$DMG_NAME"

echo "请在打开的窗口中:"
echo "1. 将 '$APP_NAME' 拖拽到 'Applications' 文件夹"
echo "2. 等待复制完成"
echo "3. 关闭窗口"

read -p "复制完成后按回车键继续..." 

echo "正在卸载映像..."
hdiutil detach "/Volumes/$APP_NAME v1.0.0" 2>/dev/null || true

echo "安装完成！"
echo "您可以从启动台或应用程序文件夹启动 '$APP_NAME'"
EOF
    
    chmod +x "$INSTALL_SCRIPT"
    echo -e "${GREEN}✓ 安装脚本创建完成: $INSTALL_SCRIPT${NC}"
}

# 验证DMG
verify_dmg() {
    echo -e "${BLUE}验证DMG文件...${NC}"
    
    if hdiutil verify "$DMG_PATH"; then
        echo -e "${GREEN}✓ DMG文件验证通过${NC}"
    else
        echo -e "${YELLOW}⚠ DMG文件验证失败，但通常仍可正常使用${NC}"
    fi
}

# 显示完成信息
show_completion_info() {
    echo -e "${GREEN}======================================"
    echo "✓ macOS 安装程序创建完成!"
    echo -e "======================================${NC}"
    echo -e "${BLUE}生成的文件:${NC}"
    echo "  📦 DMG安装包: $DMG_PATH"
    echo "  📄 安装脚本: $DIST_DIR/install_macos.sh"
    echo ""
    echo -e "${BLUE}使用方法:${NC}"
    echo "1. 分发DMG文件给用户"
    echo "2. 用户双击DMG文件"
    echo "3. 拖拽应用到Applications文件夹"
    echo ""
    echo -e "${BLUE}技术信息:${NC}"
    echo "  应用标识: $IDENTIFIER"
    echo "  版本: $VERSION"
    echo "  开发者: $AUTHOR"
    echo ""
    echo -e "${YELLOW}注意事项:${NC}"
    echo "- 首次运行可能需要在安全设置中允许"
    echo "- 建议使用macOS 10.13或更高版本"
    echo "- 需要网络连接以获取数据"
}

# 主函数
main() {
    check_dependencies
    check_app_bundle
    sign_app
    setup_dmg_assets
    create_dmg_file
    create_install_script
    verify_dmg
    cleanup
    show_completion_info
}

# 错误处理
trap 'echo -e "${RED}✗ 脚本执行失败${NC}"; cleanup; exit 1' ERR

# 运行主函数
main "$@"
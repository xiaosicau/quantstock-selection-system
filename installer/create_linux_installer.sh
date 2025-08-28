#!/bin/bash
# 量化选股系统 Linux 安装程序创建脚本
# QuantStock Linux Installer Creation Script

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 应用信息
APP_NAME="量化选股系统"
APP_NAME_EN="quantstock"
VERSION="1.0.0"
AUTHOR="量化分析团队"
DESCRIPTION="基于多因子模型的量化股票选股系统"

# 路径配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build_linux"
PACKAGE_DIR="$BUILD_DIR/package"

echo -e "${CYAN}=============================================="
echo "       量化选股系统 Linux 安装程序创建工具"
echo "       QuantStock Linux Installer Creator"
echo -e "==============================================${NC}"
echo ""

# 检测Linux发行版
detect_linux_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION_ID=$VERSION_ID
    else
        DISTRO="unknown"
    fi
    
    echo -e "${BLUE}检测到的Linux发行版: ${YELLOW}$DISTRO $VERSION_ID${NC}"
}

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}检查构建依赖...${NC}"
    
    local missing_deps=()
    
    # 检查必需工具
    for cmd in tar gzip chmod; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=($cmd)
        fi
    done
    
    # 检查可选工具
    if command -v dpkg-deb &> /dev/null; then
        echo -e "${GREEN}✓ 支持创建DEB包${NC}"
        CAN_BUILD_DEB=true
    else
        echo -e "${YELLOW}○ 未找到dpkg-deb，无法创建DEB包${NC}"
        CAN_BUILD_DEB=false
    fi
    
    if command -v rpmbuild &> /dev/null; then
        echo -e "${GREEN}✓ 支持创建RPM包${NC}"
        CAN_BUILD_RPM=true
    else
        echo -e "${YELLOW}○ 未找到rpmbuild，无法创建RPM包${NC}"
        CAN_BUILD_RPM=false
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${RED}缺少依赖: ${missing_deps[*]}${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 依赖检查完成${NC}"
}

# 准备构建目录
prepare_build_dir() {
    echo -e "${BLUE}准备构建目录...${NC}"
    
    rm -rf "$BUILD_DIR"
    mkdir -p "$PACKAGE_DIR"
    
    echo -e "${GREEN}✓ 构建目录准备完成${NC}"
}

# 复制程序文件
copy_program_files() {
    echo -e "${BLUE}复制程序文件...${NC}"
    
    # 创建目录结构
    mkdir -p "$PACKAGE_DIR/opt/$APP_NAME_EN"
    mkdir -p "$PACKAGE_DIR/usr/bin"
    mkdir -p "$PACKAGE_DIR/usr/share/applications"
    mkdir -p "$PACKAGE_DIR/usr/share/pixmaps"
    mkdir -p "$PACKAGE_DIR/usr/share/doc/$APP_NAME_EN"
    
    # 复制主程序
    if [ -d "$DIST_DIR/$APP_NAME" ]; then
        cp -r "$DIST_DIR/$APP_NAME"/* "$PACKAGE_DIR/opt/$APP_NAME_EN/"
    else
        echo -e "${RED}错误: 找不到构建的程序文件 $DIST_DIR/$APP_NAME${NC}"
        exit 1
    fi
    
    # 复制文档
    for doc in README.md QUICK_START.md INSTALLER_GUIDE.md LICENSE; do
        if [ -f "$PROJECT_ROOT/$doc" ]; then
            cp "$PROJECT_ROOT/$doc" "$PACKAGE_DIR/usr/share/doc/$APP_NAME_EN/"
        fi
    done
    
    # 复制示例文件
    mkdir -p "$PACKAGE_DIR/usr/share/doc/$APP_NAME_EN/examples"
    for example in quantstock_demo.py simple_demo.py; do
        if [ -f "$PROJECT_ROOT/$example" ]; then
            cp "$PROJECT_ROOT/$example" "$PACKAGE_DIR/usr/share/doc/$APP_NAME_EN/examples/"
        fi
    done
    
    echo -e "${GREEN}✓ 程序文件复制完成${NC}"
}

# 创建启动脚本
create_launcher_script() {
    echo -e "${BLUE}创建启动脚本...${NC}"
    
    cat > "$PACKAGE_DIR/usr/bin/$APP_NAME_EN" << EOF
#!/bin/bash
# 量化选股系统启动脚本

APP_DIR="/opt/$APP_NAME_EN"
PYTHON_BIN="\$APP_DIR/$APP_NAME"

# 检查程序是否存在
if [ ! -f "\$PYTHON_BIN" ]; then
    echo "错误: 找不到程序文件 \$PYTHON_BIN"
    echo "请重新安装 $APP_NAME"
    exit 1
fi

# 切换到应用程序目录
cd "\$APP_DIR"

# 根据参数启动不同模式
case "\$1" in
    "gui"|"")
        # GUI模式 (默认)
        export DISPLAY=\${DISPLAY:-:0}
        "\$PYTHON_BIN" gui
        ;;
    "web")
        # Web模式
        "\$PYTHON_BIN" web
        ;;
    "console")
        # 控制台模式
        "\$PYTHON_BIN" console
        ;;
    "api")
        # API模式
        "\$PYTHON_BIN" api
        ;;
    "--help"|"-h")
        echo "用法: $APP_NAME_EN [模式]"
        echo ""
        echo "可用模式:"
        echo "  gui      图形界面模式 (默认)"
        echo "  web      Web界面模式"
        echo "  console  控制台模式"
        echo "  api      API服务模式"
        echo "  --help   显示此帮助信息"
        ;;
    *)
        echo "未知参数: \$1"
        echo "使用 --help 查看帮助信息"
        exit 1
        ;;
esac
EOF
    
    chmod +x "$PACKAGE_DIR/usr/bin/$APP_NAME_EN"
    
    echo -e "${GREEN}✓ 启动脚本创建完成${NC}"
}

# 创建桌面文件
create_desktop_file() {
    echo -e "${BLUE}创建桌面文件...${NC}"
    
    cat > "$PACKAGE_DIR/usr/share/applications/$APP_NAME_EN.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_NAME
Name[en]=QuantStock
Comment=$DESCRIPTION
Comment[en]=Quantitative stock selection system based on multi-factor model
Exec=$APP_NAME_EN %f
Icon=$APP_NAME_EN
Terminal=false
Categories=Office;Finance;
MimeType=application/x-quantstock;
StartupNotify=true
StartupWMClass=$APP_NAME_EN
Keywords=stock;finance;quantitative;investment;analysis;
EOF
    
    echo -e "${GREEN}✓ 桌面文件创建完成${NC}"
}

# 创建图标文件
create_icon() {
    echo -e "${BLUE}创建应用图标...${NC}"
    
    # 如果有图标文件，复制它
    if [ -f "$PROJECT_ROOT/assets/icon.png" ]; then
        cp "$PROJECT_ROOT/assets/icon.png" "$PACKAGE_DIR/usr/share/pixmaps/$APP_NAME_EN.png"
    else
        # 创建简单的文本图标
        echo "🏭📊" > "$PACKAGE_DIR/usr/share/pixmaps/$APP_NAME_EN.png"
    fi
    
    echo -e "${GREEN}✓ 图标文件创建完成${NC}"
}

# 创建安装/卸载脚本
create_install_scripts() {
    echo -e "${BLUE}创建安装/卸载脚本...${NC}"
    
    # 安装后脚本
    mkdir -p "$PACKAGE_DIR/DEBIAN"
    cat > "$PACKAGE_DIR/DEBIAN/postinst" << EOF
#!/bin/bash
# 安装后脚本

set -e

# 更新桌面数据库
if command -v update-desktop-database > /dev/null 2>&1; then
    update-desktop-database -q /usr/share/applications
fi

# 更新图标缓存
if command -v gtk-update-icon-cache > /dev/null 2>&1; then
    gtk-update-icon-cache -q -t -f /usr/share/pixmaps
fi

echo "安装完成!"
echo "您可以从应用程序菜单启动 '$APP_NAME'"
echo "或在终端运行: $APP_NAME_EN"
EOF

    # 卸载前脚本
    cat > "$PACKAGE_DIR/DEBIAN/prerm" << EOF
#!/bin/bash
# 卸载前脚本

set -e

# 停止可能运行的服务
pkill -f "$APP_NAME_EN" || true

echo "正在卸载 $APP_NAME..."
EOF

    # 卸载后脚本
    cat > "$PACKAGE_DIR/DEBIAN/postrm" << EOF
#!/bin/bash
# 卸载后脚本

set -e

# 更新桌面数据库
if command -v update-desktop-database > /dev/null 2>&1; then
    update-desktop-database -q /usr/share/applications
fi

# 清理用户配置（可选）
if [ "\$1" = "purge" ]; then
    rm -rf /home/*/.config/$APP_NAME_EN
    rm -rf /home/*/.local/share/$APP_NAME_EN
fi

echo "$APP_NAME 已卸载"
EOF

    chmod +x "$PACKAGE_DIR/DEBIAN/postinst"
    chmod +x "$PACKAGE_DIR/DEBIAN/prerm"
    chmod +x "$PACKAGE_DIR/DEBIAN/postrm"
    
    echo -e "${GREEN}✓ 安装/卸载脚本创建完成${NC}"
}

# 创建DEB包
create_deb_package() {
    if [ "$CAN_BUILD_DEB" = false ]; then
        echo -e "${YELLOW}跳过DEB包创建${NC}"
        return
    fi
    
    echo -e "${BLUE}创建DEB包...${NC}"
    
    # 创建control文件
    cat > "$PACKAGE_DIR/DEBIAN/control" << EOF
Package: $APP_NAME_EN
Version: $VERSION
Section: misc
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.8), python3-tk, python3-pip
Maintainer: $AUTHOR <support@quantstock.com>
Description: $DESCRIPTION
 $APP_NAME 是一个基于多因子模型的量化股票选股系统。
 .
 主要功能包括:
  * 多因子股票评估模型
  * 智能投资建议生成
  * 可视化分析工具
  * Web和桌面界面
Homepage: https://github.com/quantstock
EOF
    
    # 计算文件大小
    INSTALLED_SIZE=$(du -s "$PACKAGE_DIR" | cut -f1)
    echo "Installed-Size: $INSTALLED_SIZE" >> "$PACKAGE_DIR/DEBIAN/control"
    
    # 构建DEB包
    DEB_FILE="$DIST_DIR/${APP_NAME_EN}_${VERSION}_amd64.deb"
    dpkg-deb --build "$PACKAGE_DIR" "$DEB_FILE"
    
    if [ -f "$DEB_FILE" ]; then
        echo -e "${GREEN}✓ DEB包创建成功: $DEB_FILE${NC}"
        
        # 显示包信息
        DEB_SIZE=$(du -h "$DEB_FILE" | cut -f1)
        echo -e "${GREEN}  文件大小: $DEB_SIZE${NC}"
    else
        echo -e "${RED}✗ DEB包创建失败${NC}"
    fi
}

# 创建通用tar.gz包
create_tarball() {
    echo -e "${BLUE}创建通用tar.gz包...${NC}"
    
    TARBALL_NAME="${APP_NAME_EN}-${VERSION}-linux-x86_64.tar.gz"
    TARBALL_PATH="$DIST_DIR/$TARBALL_NAME"
    
    # 创建安装脚本
    cat > "$PACKAGE_DIR/install.sh" << EOF
#!/bin/bash
# $APP_NAME 安装脚本

set -e

APP_NAME="$APP_NAME"
APP_NAME_EN="$APP_NAME_EN"
INSTALL_DIR="/opt/\$APP_NAME_EN"
BIN_DIR="/usr/local/bin"

echo "=============================================="
echo "正在安装 \$APP_NAME v$VERSION"
echo "=============================================="

# 检查权限
if [ "\$EUID" -ne 0 ]; then
    echo "错误: 需要root权限安装"
    echo "请使用: sudo ./install.sh"
    exit 1
fi

# 创建安装目录
echo "创建安装目录..."
mkdir -p "\$INSTALL_DIR"

# 复制文件
echo "复制程序文件..."
cp -r opt/\$APP_NAME_EN/* "\$INSTALL_DIR/"

# 创建符号链接
echo "创建命令链接..."
ln -sf "\$INSTALL_DIR/$APP_NAME" "\$BIN_DIR/\$APP_NAME_EN"

# 安装桌面文件
if [ -d "/usr/share/applications" ]; then
    echo "安装桌面快捷方式..."
    cp usr/share/applications/\$APP_NAME_EN.desktop /usr/share/applications/
fi

# 安装图标
if [ -d "/usr/share/pixmaps" ]; then
    echo "安装应用图标..."
    cp usr/share/pixmaps/\$APP_NAME_EN.png /usr/share/pixmaps/
fi

# 安装文档
if [ -d "/usr/share/doc" ]; then
    echo "安装文档..."
    mkdir -p /usr/share/doc/\$APP_NAME_EN
    cp -r usr/share/doc/\$APP_NAME_EN/* /usr/share/doc/\$APP_NAME_EN/
fi

# 设置权限
chmod +x "\$INSTALL_DIR/$APP_NAME"
chmod +x "\$BIN_DIR/\$APP_NAME_EN"

echo ""
echo "=============================================="
echo "✓ 安装完成!"
echo "=============================================="
echo "启动方式:"
echo "1. 命令行: \$APP_NAME_EN"
echo "2. 应用程序菜单中查找 '\$APP_NAME'"
echo ""
echo "使用帮助: \$APP_NAME_EN --help"
EOF

    chmod +x "$PACKAGE_DIR/install.sh"
    
    # 创建卸载脚本
    cat > "$PACKAGE_DIR/uninstall.sh" << EOF
#!/bin/bash
# $APP_NAME 卸载脚本

set -e

APP_NAME="$APP_NAME"
APP_NAME_EN="$APP_NAME_EN"
INSTALL_DIR="/opt/\$APP_NAME_EN"
BIN_DIR="/usr/local/bin"

echo "=============================================="
echo "正在卸载 \$APP_NAME"
echo "=============================================="

# 检查权限
if [ "\$EUID" -ne 0 ]; then
    echo "错误: 需要root权限卸载"
    echo "请使用: sudo ./uninstall.sh"
    exit 1
fi

# 停止运行的进程
pkill -f "\$APP_NAME_EN" || true

# 删除文件
echo "删除程序文件..."
rm -rf "\$INSTALL_DIR"
rm -f "\$BIN_DIR/\$APP_NAME_EN"
rm -f "/usr/share/applications/\$APP_NAME_EN.desktop"
rm -f "/usr/share/pixmaps/\$APP_NAME_EN.png"
rm -rf "/usr/share/doc/\$APP_NAME_EN"

echo ""
echo "✓ 卸载完成!"
EOF

    chmod +x "$PACKAGE_DIR/uninstall.sh"
    
    # 创建README
    cat > "$PACKAGE_DIR/README.txt" << EOF
$APP_NAME v$VERSION
========================

这是 $APP_NAME 的Linux安装包。

安装方法:
1. 解压此文件: tar -xzf $TARBALL_NAME
2. 进入目录: cd ${APP_NAME_EN}-${VERSION}
3. 运行安装: sudo ./install.sh

卸载方法:
sudo ./uninstall.sh

或者手动运行:
./opt/$APP_NAME_EN/$APP_NAME

系统要求:
- Linux x86_64
- Python 3.8+
- 网络连接

开发团队: $AUTHOR
技术支持: https://github.com/quantstock
EOF
    
    # 创建tar.gz包
    cd "$BUILD_DIR"
    tar -czf "$TARBALL_PATH" -C package .
    
    if [ -f "$TARBALL_PATH" ]; then
        echo -e "${GREEN}✓ tar.gz包创建成功: $TARBALL_PATH${NC}"
        
        # 显示包信息
        TAR_SIZE=$(du -h "$TARBALL_PATH" | cut -f1)
        echo -e "${GREEN}  文件大小: $TAR_SIZE${NC}"
    else
        echo -e "${RED}✗ tar.gz包创建失败${NC}"
    fi
}

# 创建AppImage (如果可能)
create_appimage() {
    if ! command -v appimagetool &> /dev/null; then
        echo -e "${YELLOW}跳过AppImage创建 (需要appimagetool)${NC}"
        return
    fi
    
    echo -e "${BLUE}创建AppImage...${NC}"
    
    APPIMAGE_DIR="$BUILD_DIR/appimage"
    mkdir -p "$APPIMAGE_DIR"
    
    # 复制文件到AppImage结构
    cp -r "$PACKAGE_DIR/opt/$APP_NAME_EN"/* "$APPIMAGE_DIR/"
    cp "$PACKAGE_DIR/usr/share/applications/$APP_NAME_EN.desktop" "$APPIMAGE_DIR/"
    cp "$PACKAGE_DIR/usr/share/pixmaps/$APP_NAME_EN.png" "$APPIMAGE_DIR/"
    
    # 创建AppRun脚本
    cat > "$APPIMAGE_DIR/AppRun" << EOF
#!/bin/bash
SELF=\$(readlink -f "\$0")
HERE=\${SELF%/*}
export PATH="\${HERE}:\${PATH}"
cd "\$HERE"
exec "\$HERE/$APP_NAME" "\$@"
EOF
    chmod +x "$APPIMAGE_DIR/AppRun"
    
    # 构建AppImage
    APPIMAGE_FILE="$DIST_DIR/${APP_NAME_EN}-${VERSION}-x86_64.AppImage"
    appimagetool "$APPIMAGE_DIR" "$APPIMAGE_FILE"
    
    if [ -f "$APPIMAGE_FILE" ]; then
        echo -e "${GREEN}✓ AppImage创建成功: $APPIMAGE_FILE${NC}"
    else
        echo -e "${RED}✗ AppImage创建失败${NC}"
    fi
}

# 清理构建文件
cleanup() {
    echo -e "${BLUE}清理构建文件...${NC}"
    rm -rf "$BUILD_DIR"
    echo -e "${GREEN}✓ 清理完成${NC}"
}

# 显示完成信息
show_completion_info() {
    echo ""
    echo -e "${GREEN}=============================================="
    echo "✓ Linux 安装程序创建完成!"
    echo -e "==============================================${NC}"
    echo -e "${BLUE}生成的文件:${NC}"
    
    for file in "$DIST_DIR"/*linux*; do
        if [ -f "$file" ]; then
            SIZE=$(du -h "$file" | cut -f1)
            echo "  📦 $(basename "$file") ($SIZE)"
        fi
    done
    
    echo ""
    echo -e "${BLUE}安装方法:${NC}"
    echo "DEB包 (Ubuntu/Debian): sudo dpkg -i ${APP_NAME_EN}_${VERSION}_amd64.deb"
    echo "tar.gz包 (通用): tar -xzf ${APP_NAME_EN}-${VERSION}-linux-x86_64.tar.gz && sudo ./install.sh"
    echo ""
    echo -e "${BLUE}系统要求:${NC}"
    echo "- Linux x86_64"
    echo "- Python 3.8+"
    echo "- 图形界面 (GUI模式)"
    echo "- 网络连接"
    echo ""
    echo -e "${YELLOW}注意事项:${NC}"
    echo "- 首次运行可能需要安装Python依赖"
    echo "- 建议使用包管理器安装"
    echo "- GUI模式需要X11或Wayland"
}

# 主函数
main() {
    detect_linux_distro
    check_dependencies
    prepare_build_dir
    copy_program_files
    create_launcher_script
    create_desktop_file
    create_icon
    create_install_scripts
    create_deb_package
    create_tarball
    create_appimage
    cleanup
    show_completion_info
}

# 错误处理
trap 'echo -e "${RED}✗ 脚本执行失败${NC}"; cleanup; exit 1' ERR

# 运行主函数
main "$@"
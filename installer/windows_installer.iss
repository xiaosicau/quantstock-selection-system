; 量化选股系统 Windows 安装程序脚本
; QuantStock Windows Installer Script
; 使用 Inno Setup 编译

[Setup]
; 应用程序基本信息
AppName=量化选股系统
AppVersion=1.0.0
AppPublisher=量化分析团队
AppPublisherURL=https://github.com/quantstock
AppSupportURL=https://github.com/quantstock/issues
AppUpdatesURL=https://github.com/quantstock/releases
DefaultDirName={autopf}\QuantStock
DefaultGroupName=量化选股系统
AllowNoIcons=yes
LicenseFile=..\LICENSE
InfoBeforeFile=..\README.md
OutputDir=..\dist\installer
OutputBaseFilename=QuantStock-1.0.0-Windows-Setup
SetupIconFile=..\assets\icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

; 系统要求
MinVersion=6.1sp1
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; 多语言支持
[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

; 安装选项
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "associatefiles"; Description: "关联.qstock文件"; GroupDescription: "文件关联:"; Flags: unchecked

; 安装文件
[Files]
; 主程序
Source: "..\dist\量化选股系统\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 配置文件
Source: "..\config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
; 文档文件
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\QUICK_START.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\INSTALLER_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion
; 示例文件
Source: "..\quantstock_demo.py"; DestDir: "{app}\examples"; Flags: ignoreversion
Source: "..\simple_demo.py"; DestDir: "{app}\examples"; Flags: ignoreversion

; 注册表设置
[Registry]
Root: HKCR; Subkey: ".qstock"; ValueType: string; ValueName: ""; ValueData: "QuantStockFile"; Flags: uninsdeletevalue; Tasks: associatefiles
Root: HKCR; Subkey: "QuantStockFile"; ValueType: string; ValueName: ""; ValueData: "QuantStock 策略文件"; Flags: uninsdeletekey; Tasks: associatefiles
Root: HKCR; Subkey: "QuantStockFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\量化选股系统.exe,0"; Tasks: associatefiles
Root: HKCR; Subkey: "QuantStockFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\量化选股系统.exe"" ""%1"""; Tasks: associatefiles

; 快捷方式
[Icons]
; 开始菜单
Name: "{group}\量化选股系统"; Filename: "{app}\量化选股系统.exe"
Name: "{group}\量化选股系统 (控制台模式)"; Filename: "{app}\量化选股系统.exe"; Parameters: "console"
Name: "{group}\量化选股系统 (Web模式)"; Filename: "{app}\量化选股系统.exe"; Parameters: "web"
Name: "{group}\演示程序"; Filename: "{app}\examples\quantstock_demo.py"
Name: "{group}\用户指南"; Filename: "{app}\QUICK_START.md"
Name: "{group}\技术文档"; Filename: "{app}\INSTALLER_GUIDE.md"
Name: "{group}\{cm:UninstallProgram,量化选股系统}"; Filename: "{uninstallexe}"

; 桌面快捷方式
Name: "{autodesktop}\量化选股系统"; Filename: "{app}\量化选股系统.exe"; Tasks: desktopicon

; 快速启动栏
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\量化选股系统"; Filename: "{app}\量化选股系统.exe"; Tasks: quicklaunchicon

; 安装后运行
[Run]
Filename: "{app}\量化选股系统.exe"; Description: "{cm:LaunchProgram,量化选股系统}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\QUICK_START.md"; Description: "查看快速开始指南"; Flags: postinstall skipifsilent shellexec unchecked

; 卸载前运行
[UninstallRun]
Filename: "{app}\量化选股系统.exe"; Parameters: "--cleanup"; Flags: runhidden

; 安装过程消息
[Messages]
WelcomeLabel2=这将在您的计算机上安装 [name/ver]。%n%n量化选股系统是基于多因子模型的智能股票筛选工具，帮助您进行科学的投资决策。%n%n建议您在继续安装前关闭所有其他应用程序。

; 自定义页面
[Code]
var
  DataSourcePage: TInputOptionWizardPage;
  ConfigPage: TInputQueryWizardPage;

procedure InitializeWizard;
begin
  // 数据源选择页面
  DataSourcePage := CreateInputOptionPage(wpSelectDir,
    '数据源配置', '选择要使用的数据源',
    '请选择您要使用的数据源（可多选）：',
    True, False);
  DataSourcePage.Add('AkShare (免费，推荐)');
  DataSourcePage.Add('Yahoo Finance (免费)');
  DataSourcePage.Add('Tushare Pro (需要Token)');
  DataSourcePage.Add('Wind (商业版，需要授权)');
  
  // 默认选择前两个
  DataSourcePage.Values[0] := True;
  DataSourcePage.Values[1] := True;
  
  // 配置页面
  ConfigPage := CreateInputQueryPage(DataSourcePage.ID,
    '基本配置', '配置系统参数',
    '请输入基本配置信息：');
  ConfigPage.Add('Tushare Pro Token (可选):', False);
  ConfigPage.Add('Wind路径 (可选):', False);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if CurPageID = DataSourcePage.ID then
  begin
    // 验证至少选择一个数据源
    if not (DataSourcePage.Values[0] or DataSourcePage.Values[1] or 
            DataSourcePage.Values[2] or DataSourcePage.Values[3]) then
    begin
      MsgBox('请至少选择一个数据源！', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigText: string;
  ConfigFile: string;
begin
  if CurStep = ssPostInstall then
  begin
    // 生成配置文件
    ConfigText := '{' + #13#10;
    ConfigText := ConfigText + '  "data_sources": {' + #13#10;
    ConfigText := ConfigText + '    "akshare": {"enabled": ' + 
      BoolToStr(DataSourcePage.Values[0], 'true', 'false') + '},' + #13#10;
    ConfigText := ConfigText + '    "yahoo": {"enabled": ' + 
      BoolToStr(DataSourcePage.Values[1], 'true', 'false') + '},' + #13#10;
    ConfigText := ConfigText + '    "tushare": {"enabled": ' + 
      BoolToStr(DataSourcePage.Values[2], 'true', 'false') + 
      ', "token": "' + ConfigPage.Values[0] + '"},' + #13#10;
    ConfigText := ConfigText + '    "wind": {"enabled": ' + 
      BoolToStr(DataSourcePage.Values[3], 'true', 'false') + 
      ', "path": "' + ConfigPage.Values[1] + '"}' + #13#10;
    ConfigText := ConfigText + '  }' + #13#10;
    ConfigText := ConfigText + '}';
    
    // 保存配置文件
    ConfigFile := ExpandConstant('{app}\config\user_config.json');
    SaveStringToFile(ConfigFile, ConfigText, False);
    
    // 创建数据目录
    CreateDir(ExpandConstant('{app}\data'));
    CreateDir(ExpandConstant('{app}\logs'));
    CreateDir(ExpandConstant('{commonappdata}\QuantStock'));
  end;
end;
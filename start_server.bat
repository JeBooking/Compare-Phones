@echo off
echo ========================================
echo      照片设备识别器 - 启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python
    echo 请先安装Python: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo Python已安装，版本信息:
python --version
echo.

REM 检查依赖是否安装
echo 检查项目依赖...
python -c "import flask, PIL, exifread" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装项目依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo 依赖检查完成!
echo.

REM 创建uploads文件夹
if not exist "uploads" mkdir uploads

echo 启动Web服务器...
echo 服务器启动后，请在浏览器中访问: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.

REM 启动Flask应用
python app.py

pause

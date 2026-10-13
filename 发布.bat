@echo off
rem 这个文件故意只写英文：中文提示交给 publish.py 打印，免得 cmd 里乱码
chcp 65001 >nul
cd /d "%~dp0"
python publish.py --ask
echo.
pause

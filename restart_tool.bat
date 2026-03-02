@echo off
setlocal
echo [1/2] 正在查找并关闭旧的 MIZ 工具进程 (端口 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a >nul 2>&1
)
echo [2/2] 正在重新启动服务...
python -m pip install fastapi uvicorn python-multipart --quiet
start http://127.0.0.1:8000
python app_server.py
pause

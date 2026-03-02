@echo off
echo 正在启动 DCS MIZ 本地化工具...
python -m pip install fastapi uvicorn python-multipart --quiet
start http://127.0.0.1:8000
python app_server.py
pause

@echo off
REM Starts the Streamlit app (start_llm_server.bat must already be running).
cd /d %~dp0
.venv\Scripts\python.exe -m streamlit run app.py

@echo off
REM Starts a local OpenAI-compatible server (llama.cpp) for the chat + embedding models.
REM Keep this window open while you use the app.
cd /d %~dp0
.venv\Scripts\python.exe llm_server.py

@echo off
REM ==========================================================================
REM  start_demo.bat - start the whole Travel Guide Assistant with one double-click
REM
REM    1. checks that the setup is complete
REM    2. starts the local model server in its own (minimised) window,
REM       or reuses it if it is already running
REM    3. waits until the model server answers
REM    4. starts the Streamlit app, which opens in your browser
REM
REM  To stop: close this window (the app) and the "model server" window.
REM ==========================================================================
cd /d %~dp0
title Travel Guide Assistant - app

REM ---- 1. setup checks (see README.md, "Setup")
if not exist .venv\Scripts\python.exe (
    echo [X] The Python environment .venv is missing. Follow "Setup" in README.md.
    pause
    exit /b 1
)
if not exist models\SmolLM2-135M-Instruct-Q8_0.gguf (
    echo [X] The model files are missing from the models folder.
    echo     The download command is at the top of config.py, and in "Setup" in README.md.
    pause
    exit /b 1
)
if not exist chroma_db\ echo [!] The RAG index is not built yet: the RAG tab will not work. See "Build the data" in README.md.
if not exist graphrag\output\vectors\ echo [!] The GraphRAG index is not built yet: the GraphRAG tab will not work. See "Build the data" in README.md.

REM ---- already running? then just open it again
curl -s -o nul http://localhost:8501/_stcore/health
if not errorlevel 1 (
    echo The app is already running - opening http://localhost:8501 in your browser.
    start "" http://localhost:8501
    timeout /t 3 /nobreak >nul
    exit /b 0
)

REM ---- 2. start the model server, unless it is already running
curl -s -o nul http://127.0.0.1:8000/v1/models
if errorlevel 1 (
    echo Starting the model server in a new minimised window...
    start "Travel Guide Assistant - model server" /min cmd /k .venv\Scripts\python.exe llm_server.py
) else (
    echo The model server is already running.
)

REM ---- 3. wait until it answers (up to 2 minutes)
echo Waiting for the model server to be ready...
for /l %%i in (1,1,60) do (
    curl -s -o nul http://127.0.0.1:8000/v1/models && goto ready
    timeout /t 2 /nobreak >nul
)
echo [X] The model server did not answer within 2 minutes. Look at its window for an error message.
pause
exit /b 1

:ready
REM ---- 4. start the app
echo Model server ready. Starting the app at http://localhost:8501 ...
.venv\Scripts\python.exe -m streamlit run app.py

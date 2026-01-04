@echo off
echo Starting CoolKonyha Assistant...
echo.
echo Checking for virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/Updating dependencies...
pip install --default-timeout=100 -r requirements.txt

echo.
echo Launching Streamlit App...
streamlit run app.py

pause

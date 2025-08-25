@echo off
:: Hackathon-ready launcher for Competitor Intelligence

:: Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Upgrade pip and install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: Install Playwright browser
python -m playwright install chromium

:: Run collector (pre-filled config included)
echo Running Competitor Intelligence Collector...
python main_v2.py

:: Launch Streamlit dashboard
echo Launching Streamlit Dashboard...
streamlit run dashboard_app.py

pause

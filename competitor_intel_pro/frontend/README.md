# Competitor Intelligence Platform (FAANG-Style Enhanced)

**What it does**
- Renders modern JS websites via **Playwright**
- Extracts text + captures screenshots
- Diffs content vs last snapshot (semantic-ish + visual)
- Classifies updates (Feature / Pricing / UI / Bugfix / Other)
- Summarizes with AI (OpenAI) or fallback heuristic
- Stores history in **SQLite**
- Generates **visual diffs** (before vs after)
- Provides a **Streamlit dashboard** for trends & browsing updates
- Optional Slack notifications; PDF digest export

## Quick Start (Local)

1) Create venv (optional) and install dependencies
```
pip install -r requirements.txt
python -m playwright install chromium
```

2) Set env vars (optional but recommended)
```
# Powershell
setx OPENAI_API_KEY "sk-..."
setx SLACK_WEBHOOK_URL "https://hooks.slack.com/services/XXX/YYY/ZZZ"
# macOS/Linux (session)
export OPENAI_API_KEY="sk-..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX/YYY/ZZZ"
```

3) Configure targets in `config.yaml`

4) Run the collector (renders pages, saves snapshots, logs to DB)
```
python main_v2.py
```

5) Launch Dashboard
```
streamlit run dashboard_app.py
```

## Docker (optional)
```
# Build
docker build -t competitor-intel .
# Run collector
docker run --rm -it -e OPENAI_API_KEY -e SLACK_WEBHOOK_URL -v ${PWD}:/app competitor-intel python main_v2.py
# Run dashboard (map port 8501)
docker run --rm -it -p 8501:8501 -v ${PWD}:/app competitor-intel streamlit run dashboard_app.py
```

## Files
- `main_v2.py` — Orchestrator (Playwright render → diff → summarize → classify → store → notify)
- `renderer.py` — Playwright-based renderer (HTML + screenshot)
- `parser.py` — Extracts readable text from rendered HTML
- `diff_tools.py` — Text diff + change line extraction
- `visual_diff.py` — Pixel difference of screenshots
- `classifier.py` — Simple rules-based tagger (Feature/Pricing/UI/Bugfix/Other)
- `summarizer.py` — AI summary with safe fallback
- `storage.py` — SQLite schema + helpers
- `notifier.py` — Report saving + Slack webhook
- `dashboard_app.py` — Streamlit dashboard
- `utils.py`, `config.yaml`, `requirements.txt`, `Dockerfile`

## Next Ideas
- App/Play Store APIs for release notes
- LinkedIn/X monitor for official accounts
- Email weekly PDF digest to stakeholders
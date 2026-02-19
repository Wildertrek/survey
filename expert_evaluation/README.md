# Personality Atlas — Expert Review

Interactive validation tool for the **Computational Atlas of Personality Models** (TIST-2025-12-1243).

Estimated time: **45-60 minutes**.

## Quick Start

### Option 1: One command (requires Python 3.9+)

**Mac/Linux:**
```bash
cd expert_evaluation
pip install streamlit && streamlit run evaluator.py
```

**Windows (PowerShell):**
```powershell
cd expert_evaluation
pip install streamlit; streamlit run evaluator.py
```

### Option 2: With virtual environment (recommended)

**Mac/Linux:**
```bash
cd expert_evaluation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run evaluator.py
```

**Windows (PowerShell):**
```powershell
cd expert_evaluation
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run evaluator.py
```

A browser window will open automatically at `http://localhost:8501`.

## What You'll Do

| Task | Items | Time |
|------|-------|------|
| Task 1: Item Classification | 50 items | ~25 min |
| Task 2: Construct Review | 67 factor entries | ~15 min |
| Task 3: Taxonomy Review | 7 categories | ~10 min |

Each model name links to its **Model Card** with full descriptions, dimensions, and references.

## Submitting Results

When finished, click **Submit** in the sidebar to:
1. Download a zip of your completed CSVs
2. Open a pre-addressed email to send the zip

## Requirements

- Python 3.9 or newer
- Works on macOS, Windows, and Linux
- No API keys or database needed

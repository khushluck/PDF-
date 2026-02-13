# PDF Role + Task Analyzer

A Flask app where you:
1. Upload a PDF.
2. Define your role.
3. Type the task you want done.

The app extracts text from the PDF, computes key points, and generates a role-task oriented response based on the uploaded document content.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:8000`.

## Run tests

```bash
pytest
```

from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Optional

from flask import Flask, render_template, request
from pypdf import PdfReader

from core import create_role_response, top_sentences, words

app = Flask(__name__)


@dataclass
class AnalysisResult:
    role: str
    task: str
    page_count: int
    character_count: int
    word_count: int
    key_points: list[str]
    response: str


def extract_pdf_text(file_bytes: bytes) -> tuple[str, int]:
    """Extract raw text from a PDF payload."""
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    text = "\n".join(pages).strip()
    return text, len(reader.pages)


def analyze(role: str, task: str, file_bytes: bytes) -> AnalysisResult:
    text, page_count = extract_pdf_text(file_bytes)
    key_points = top_sentences(text)

    return AnalysisResult(
        role=role,
        task=task,
        page_count=page_count,
        character_count=len(text),
        word_count=len(words(text)),
        key_points=key_points,
        response=create_role_response(role, task, text),
    )


@app.route("/", methods=["GET", "POST"])
def index():
    result: Optional[AnalysisResult] = None
    error: Optional[str] = None

    if request.method == "POST":
        role = request.form.get("role", "").strip()
        task = request.form.get("task", "").strip()
        uploaded = request.files.get("pdf")

        if not role or not task:
            error = "Please provide both role and task."
        elif not uploaded or not uploaded.filename.lower().endswith(".pdf"):
            error = "Please upload a valid PDF file."
        else:
            try:
                result = analyze(role, task, uploaded.read())
            except Exception as exc:  # noqa: BLE001
                error = f"Could not analyze PDF: {exc}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

from __future__ import annotations

import re


def top_sentences(text: str, limit: int = 5) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    cleaned = [s.strip() for s in sentences if len(s.strip()) > 30]
    return cleaned[:limit]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]{3,}", text.lower())


def top_terms(text: str, limit: int = 8) -> list[str]:
    stop_words = {
        "the",
        "and",
        "for",
        "that",
        "with",
        "this",
        "from",
        "are",
        "was",
        "were",
        "have",
        "has",
        "had",
        "you",
        "your",
        "into",
        "about",
        "their",
        "can",
        "will",
        "would",
        "should",
        "there",
        "they",
        "them",
    }

    counts: dict[str, int] = {}
    for word in words(text):
        if word in stop_words:
            continue
        counts[word] = counts.get(word, 0) + 1

    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [term for term, _ in ranked[:limit]]


def create_role_response(role: str, task: str, text: str) -> str:
    short_excerpt = text[:1500].strip()
    terms = ", ".join(top_terms(text)) or "No dominant terms detected"
    points = top_sentences(text, limit=3)

    if not short_excerpt:
        return (
            f"As a {role}, I could not find readable text in the PDF. "
            "Please upload a text-based PDF or OCR the file first."
        )

    bullets = "\n".join(f"- {p}" for p in points) if points else "- No clear sentences detected."

    return (
        f"Role: {role}\n"
        f"Task: {task}\n\n"
        "I analyzed the uploaded document and tailored this output to your role/task request.\n\n"
        f"Top document terms: {terms}\n\n"
        "Most relevant extracted statements:\n"
        f"{bullets}\n\n"
        "Role-directed action plan:\n"
        f"1) Interpret the top terms through the lens of '{role}'.\n"
        f"2) Execute the requested task: '{task}' using the statements above.\n"
        "3) Validate with the original PDF context before making decisions.\n\n"
        "Document excerpt used for reasoning:\n"
        f"{short_excerpt}"
    )

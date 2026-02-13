from core import create_role_response, top_sentences


def test_top_sentences_picks_long_entries():
    text = (
        "Short. "
        "This sentence is definitely long enough to be included in the output. "
        "Another meaningful sentence that should be selected as well."
    )
    result = top_sentences(text, limit=2)
    assert len(result) == 2


def test_create_role_response_includes_role_and_task():
    response = create_role_response(
        "Researcher",
        "Summarize key findings",
        "This document explains the architecture and includes performance benchmarks.",
    )
    assert "Role: Researcher" in response
    assert "Task: Summarize key findings" in response

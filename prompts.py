"""Reusable text and formatting helpers for the AI Study Assistant."""

APP_TITLE = "AI Study Assistant"

STUDY_INSTRUCTION = (
    "Read the question carefully. Write a short explanation or reflection "
    "in your own words."
)


def format_study_prompt(topic: str, question: str) -> str:
    """Return a clear prompt for one study session."""
    return (
        f"Topic: {topic}\n"
        f"Question: {question}\n\n"
        f"{STUDY_INSTRUCTION}"
    )

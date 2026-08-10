"""Functions for managing study-session history.

The functions in this file are intentionally incomplete. Complete the TODOs
during the appropriate assignment milestones.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def load_history(history_file: str) -> list[dict[str, Any]]:
    """Return all saved study sessions.

    Milestone 2:
    - Return an empty list if the history file does not exist.
    - Read valid JSON history from the file.

    Milestone 4:
    - Handle invalid JSON without crashing the application.
    """
    path = Path(history_file)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            history = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(history, list):
        return []

    return [session for session in history if isinstance(session, dict)]


def save_session(history_file: str, session: dict[str, Any]) -> None:
    """Append a study session to the history file."""
    path = Path(history_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    history = load_history(history_file)
    history.append(session)

    with path.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def display_history(history):
    if not history:
        print("No study sessions found.")
        return

    print("\nStudy History:\n")

    for i, session in enumerate(history, 1):
        print(f"{i}. {session.get('topic')} - {session.get('question')}")
        print(f"   Notes: {session.get('notes')}")
        print(f"   Time: {session.get('timestamp')}\n")


def search_history(
    history: list[dict[str, Any]],
    keyword: str,
) -> list[dict[str, Any]]:
    """Return sessions matching a keyword.

    Milestone 3:
    Search the topic, question and notes using a case-insensitive comparison.
    """
    search_term = keyword.casefold().strip()
    if not search_term:
        return []

    return [
        session
        for session in history
        if any(
            search_term in str(session.get(field, "")).casefold()
            for field in ("topic", "question", "notes")
        )
    ]


def export_session(
    session: dict[str, Any],
    export_directory: str,
) -> Path | None:
    """Export one selected study session as a Markdown file.

    Milestone 3:
    - Create the export directory if required.
    - Create a safe and meaningful filename.
    - Write the session details in Markdown format.
    - Return the path of the created file.
    """
    directory = Path(export_directory)
    directory.mkdir(parents=True, exist_ok=True)

    topic = str(session.get("topic", "study-session"))
    safe_topic = re.sub(r"[^A-Za-z0-9._-]+", "-", topic).strip("-._")
    if not safe_topic:
        safe_topic = "study-session"

    timestamp = str(session.get("timestamp", "session")).replace(":", "-")
    export_path = directory / f"{timestamp}-{safe_topic}.md"
    content = (
        f"# {topic}\n\n"
        f"- **Timestamp:** {session.get('timestamp', '')}\n"
        f"- **Question:** {session.get('question', '')}\n\n"
        f"## Notes\n\n{session.get('notes', '')}\n"
    )
    export_path.write_text(content, encoding="utf-8")
    return export_path

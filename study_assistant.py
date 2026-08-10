"""Main entry point for the AI Study Assistant.

Complete the TODOs gradually and create logical Git commits as the project
moves from Version 1 to Version 2.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import EXPORT_DIRECTORY, HISTORY_FILE as CONFIG_HISTORY_FILE, QUESTIONS_FILE as CONFIG_QUESTIONS_FILE
from history import (
    display_history,
    export_session,
    load_history,
    save_session,
    search_history,
)
from prompts import APP_TITLE, format_study_prompt

BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = str(BASE_DIR / CONFIG_QUESTIONS_FILE)
HISTORY_FILE = str(BASE_DIR / CONFIG_HISTORY_FILE)
EXPORT_DIR = str(BASE_DIR / EXPORT_DIRECTORY)


# ✅ Load questions
def load_questions(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        print("Error loading file")
        return []


# ✅ Select question
def select_question(questions):
    if not questions:
        print("No questions available")
        return None

    for i, q in enumerate(questions, 1):
        print(f"{i}. {q.get('question')}")

    try:
        choice = int(input("Enter choice: "))
        if 1 <= choice <= len(questions):
            return questions[choice - 1]
        else:
            print("Invalid choice")
            return None
    except:
        print("Enter a number")
        return None


# ✅ Complete session
def complete_study_session(selected_question: dict[str, Any]) -> dict[str, Any]:
    topic = str(selected_question.get("topic", "Unknown Topic"))
    question = str(selected_question.get("question", ""))

    print("\n" + format_study_prompt(topic, question))
    notes = input("\nYour explanation or reflection: ").strip()

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "topic": topic,
        "question": question,
        "notes": notes,
    }


# ✅ Start session
def start_study_session():
    questions = load_questions(QUESTIONS_FILE)

    if not questions:
        print("No questions loaded")
        return

    selected_question = select_question(questions)

    if selected_question is None:
        return

    session = complete_study_session(selected_question)
    save_session(HISTORY_FILE, session)

    print("\nStudy session saved.")


# ✅ Recent activity
def show_recent_activity(history):
    if not history:
        print("No recent activity")
        return

    print("\nRecent Activity:")
    for session in history[-3:]:
        print(f"{session['timestamp']} - {session['topic']}")


# ✅ Search
def run_search():
    history = load_history(HISTORY_FILE)
    keyword = input("Enter a keyword: ").strip()

    results = search_history(history, keyword)
    display_history(results)


# ✅ Export
def run_export():
    history = load_history(HISTORY_FILE)

    if not history:
        print("No study sessions are available to export.")
        return

    display_history(history)

    try:
        choice = int(input("Select session number: "))

        if 1 <= choice <= len(history):
            session = history[choice - 1]
            path = export_session(session, EXPORT_DIR)
            print("Exported to:", path)
        else:
            print("Invalid choice")

    except:
        print("Enter a valid number")


# ✅ Menu
def display_menu():
    print(f"\n{APP_TITLE}")
    print("1. Start a study session")
    print("2. View study history")
    print("3. Search study history")
    print("4. Export a study session")
    print("5. Exit")


# ✅ Main
def main():
    history = load_history(HISTORY_FILE)
    show_recent_activity(history)

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            start_study_session()
        elif choice == "2":
            display_history(load_history(HISTORY_FILE))
        elif choice == "3":
            run_search()
        elif choice == "4":
            run_export()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Please enter a valid option.")


if __name__ == "__main__":
    main()
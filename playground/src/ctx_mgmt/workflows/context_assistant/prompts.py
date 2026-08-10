ASSISTANT_SYSTEM_PROMPT = (
    "You are a context-aware project assistant. Use ONLY the provided context. "
    "If the answer is not in context, say so."
)


def build_router_prompt(message: str) -> str:
    return (
        "Classify whether this user message needs client/project documents to answer. "
        "Return needs_retrieval=true for any question asking about project-specific facts, "
        "such as what the client does, architecture, deployment, infrastructure, auth, analytics, "
        "implementation details, or other scoped knowledge. Return needs_retrieval=false only for "
        "greetings, thanks, simple acknowledgements, or replies answerable from recent conversation alone.\n\n"
        f"User message:\n{message}"
    )


def build_summary_prompt(existing_summary: str, older_history: str) -> str:
    return (
        "Summarize the following conversation history into a concise running summary. "
        "Preserve decisions, facts, and open questions.\n\n"
        f"EXISTING SUMMARY (may be empty):\n{existing_summary}\n\n"
        f"NEW HISTORY TO SUMMARIZE:\n{older_history}"
    )

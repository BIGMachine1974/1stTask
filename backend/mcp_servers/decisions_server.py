"""MCP tools for the Chief of Staff decision framework.

These tools let the agent:
- Log decisions and recommendations
- Record user feedback (approve/reject/correct)
- Look up decision criteria for a category
- Save and retrieve user preferences
"""

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import select

from backend.db.models import Decision, DecisionCriteria, UserPreference
from backend.db.session import async_session


async def log_decision(
    category: str,
    summary: str,
    reasoning: str,
    autonomy_level: str = "recommend",
    context: str | None = None,
    criteria_id: str | None = None,
    session_id: str | None = None,
) -> str:
    """Log a decision or recommendation made by the Chief of Staff.

    Use this EVERY TIME you make a recommendation or take an autonomous action.
    This creates the feedback loop that helps you learn the user's preferences.

    Args:
        category: Decision category (e.g. "scheduling", "vendor", "architecture", "hiring", "email").
        summary: One-line summary of what was decided or recommended.
        reasoning: Why this decision was made — reference the user's known criteria and preferences.
        autonomy_level: "auto" (already done), "recommend" (awaiting approval), "flag" (just flagging).
        context: Optional JSON string with supporting data.
        criteria_id: Optional UUID of the DecisionCriteria used.
        session_id: Optional UUID of the conversation session.

    Returns:
        The decision ID and status confirmation.
    """
    ctx = json.loads(context) if context else None
    cid = uuid.UUID(criteria_id) if criteria_id else None
    sid = uuid.UUID(session_id) if session_id else None

    decision = Decision(
        category=category,
        summary=summary,
        reasoning=reasoning,
        autonomy_level=autonomy_level,
        context=ctx,
        criteria_id=cid,
        session_id=sid,
        status="executed" if autonomy_level == "auto" else "pending",
    )

    async with async_session() as db:
        db.add(decision)
        await db.commit()
        await db.refresh(decision)

    status_msg = {
        "auto": "Action taken autonomously.",
        "recommend": "Recommendation logged — awaiting your approval.",
        "flag": "Flagged for your awareness.",
    }

    return f"Decision logged (ID: {decision.id}). {status_msg.get(autonomy_level, '')}"


async def record_feedback(
    decision_id: str,
    status: str,
    feedback: str | None = None,
    correction: str | None = None,
) -> str:
    """Record the user's feedback on a decision.

    Call this when the user approves, rejects, or corrects a recommendation.
    This is how the Chief of Staff learns and improves over time.

    Args:
        decision_id: UUID of the decision to update.
        status: "approved", "rejected", or "corrected".
        feedback: Optional user comment (e.g. "Good call" or "Not quite right").
        correction: What should have been decided instead (required if status is "corrected").

    Returns:
        Confirmation of the feedback recorded.
    """
    async with async_session() as db:
        decision = await db.get(Decision, uuid.UUID(decision_id))
        if not decision:
            return f"Decision {decision_id} not found."

        decision.status = status
        decision.user_feedback = feedback
        decision.correction = correction
        decision.resolved_at = datetime.now(timezone.utc)
        await db.commit()

    if status == "corrected" and correction:
        return f"Correction recorded. I'll remember: {correction}"
    elif status == "approved":
        return "Noted — this reinforces the decision pattern."
    else:
        return f"Feedback recorded (status: {status})."


async def get_criteria(category: str) -> str:
    """Look up the decision criteria for a category.

    Check this BEFORE making any recommendation — it contains the user's
    established rules and preferences for this type of decision.

    Args:
        category: The decision category (e.g. "vendor", "scheduling", "architecture").

    Returns:
        The criteria as formatted text, or a message if no criteria exist yet.
    """
    async with async_session() as db:
        result = await db.execute(
            select(DecisionCriteria).where(DecisionCriteria.category == category)
        )
        criteria = result.scalars().all()

    if not criteria:
        return f"No established criteria for '{category}' yet. Ask the user about their preferences for this type of decision and save them."

    formatted = []
    for c in criteria:
        formatted.append(
            f"--- {c.name} (autonomy: {c.autonomy_level}) ---\n"
            f"{json.dumps(c.criteria, indent=2)}"
        )
    return "\n\n".join(formatted)


async def save_preference(
    key: str,
    value: str,
    source: str = "explicit",
    confidence: float = 0.8,
) -> str:
    """Save or update a user preference.

    Use this when the user states a preference explicitly, or when you infer
    one from their behavior or corrections. Preferences are used across all
    agents to personalize behavior.

    Args:
        key: Preference category (e.g. "communication_style", "meeting_preferences", "risk_tolerance").
        value: The preference description.
        source: "explicit" (user stated it), "inferred" (observed from behavior), "corrected" (learned from correction).
        confidence: 0.0-1.0 confidence level. Explicit = 0.9+, inferred = 0.5-0.7, corrected = 0.8+.

    Returns:
        Confirmation.
    """
    async with async_session() as db:
        # Check if this preference already exists
        result = await db.execute(
            select(UserPreference).where(UserPreference.key == key)
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.value = value
            existing.source = source
            existing.confidence = confidence
            existing.updated_at = datetime.now(timezone.utc)
        else:
            db.add(UserPreference(
                key=key, value=value, source=source, confidence=confidence,
            ))
        await db.commit()

    return f"Preference saved: {key} = {value}"


async def get_preferences() -> str:
    """Get all known user preferences.

    Check this at the start of conversations and before making decisions
    to ensure alignment with the user's established patterns.

    Returns:
        All preferences as formatted text.
    """
    async with async_session() as db:
        result = await db.execute(
            select(UserPreference).order_by(UserPreference.key)
        )
        prefs = result.scalars().all()

    if not prefs:
        return "No preferences recorded yet. As you learn the user's style and preferences, save them here."

    lines = []
    for p in prefs:
        conf = f"{'high' if p.confidence >= 0.8 else 'medium' if p.confidence >= 0.5 else 'low'} confidence"
        lines.append(f"- {p.key}: {p.value} ({p.source}, {conf})")
    return "\n".join(lines)


async def get_recent_decisions(category: str | None = None, limit: int = 10) -> str:
    """Get recent decisions for context and pattern recognition.

    Use this to understand the user's decision history before making
    new recommendations in the same category.

    Args:
        category: Optional filter by category.
        limit: Maximum number of decisions to return (default 10).

    Returns:
        Recent decisions with their outcomes and any corrections.
    """
    async with async_session() as db:
        query = select(Decision).order_by(Decision.created_at.desc()).limit(limit)
        if category:
            query = query.where(Decision.category == category)
        result = await db.execute(query)
        decisions = result.scalars().all()

    if not decisions:
        return f"No previous decisions{f' in {category}' if category else ''}."

    lines = []
    for d in decisions:
        status_icon = {"approved": "Y", "rejected": "N", "corrected": "~", "pending": "?", "executed": "A"}.get(d.status, "?")
        line = f"[{status_icon}] {d.summary} (category: {d.category}, {d.created_at.strftime('%Y-%m-%d')})"
        if d.correction:
            line += f"\n    Correction: {d.correction}"
        if d.user_feedback:
            line += f"\n    Feedback: {d.user_feedback}"
        lines.append(line)
    return "\n".join(lines)

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    messages: Mapped[list["Message"]] = relationship(back_populates="session", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"))
    role: Mapped[str]  # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["Session"] = relationship(back_populates="messages")


# --- Chief of Staff: Decision Framework ---


class DecisionCriteria(Base):
    """Reusable decision criteria that capture how the user thinks about a category of decisions.

    Examples:
    - category="vendor_selection", criteria={"must_have": ["SOC2", "API access"], "prefer": ["< $500/mo"], ...}
    - category="hiring", criteria={"must_have": ["3+ yrs experience"], "red_flags": ["job hopping"], ...}
    """
    __tablename__ = "decision_criteria"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    category: Mapped[str]  # e.g. "vendor_selection", "architecture", "hiring", "scheduling"
    name: Mapped[str]  # human-readable name, e.g. "SaaS Vendor Evaluation"
    criteria: Mapped[dict] = mapped_column(JSON)  # structured criteria
    autonomy_level: Mapped[str] = mapped_column(default="recommend")  # "auto", "recommend", "flag"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    decisions: Mapped[list["Decision"]] = relationship(back_populates="criteria_ref")


class Decision(Base):
    """A specific decision the Chief of Staff made or recommended.

    Tracks the full lifecycle: recommendation -> user feedback -> outcome.
    This is the learning loop — corrections teach the system how the user thinks.
    """
    __tablename__ = "decisions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    criteria_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("decision_criteria.id"), nullable=True)
    session_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("sessions.id"), nullable=True)

    # What was decided
    category: Mapped[str]  # matches DecisionCriteria.category
    summary: Mapped[str] = mapped_column(Text)  # "Recommended Stripe over Square for payment processing"
    reasoning: Mapped[str] = mapped_column(Text)  # "Based on your criteria: API quality, pricing, SOC2..."
    context: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # supporting data

    # Autonomy and outcome
    autonomy_level: Mapped[str]  # "auto" (just did it), "recommend" (waiting for approval), "flag" (heads up)
    status: Mapped[str] = mapped_column(default="pending")  # "pending", "approved", "rejected", "corrected"

    # User feedback (the learning loop)
    user_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)  # "Good call" or "No, because..."
    correction: Mapped[str | None] = mapped_column(Text, nullable=True)  # What should have been decided instead

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    criteria_ref: Mapped["DecisionCriteria | None"] = relationship(back_populates="decisions")


class UserPreference(Base):
    """Explicit user preferences and patterns learned over time.

    These are distilled from conversation history, decision corrections, and direct statements.
    Examples:
    - key="communication_style", value="concise, no fluff, bullet points preferred"
    - key="risk_tolerance", value="conservative on spending, aggressive on tech adoption"
    - key="meeting_preferences", value="no meetings before 10am, prefer 30min max"
    """
    __tablename__ = "user_preferences"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    key: Mapped[str]  # preference category
    value: Mapped[str] = mapped_column(Text)  # the preference
    source: Mapped[str] = mapped_column(default="inferred")  # "explicit", "inferred", "corrected"
    confidence: Mapped[float] = mapped_column(default=0.5)  # 0.0-1.0, increases with confirmation
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

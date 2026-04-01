import json
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from backend.agents.manager import run_agent
from backend.db.models import Message, Session
from backend.db.session import async_session

ws_router = APIRouter()


async def _ensure_session(session_id: uuid.UUID) -> None:
    """Create the session row if it doesn't exist."""
    async with async_session() as db:
        existing = await db.get(Session, session_id)
        if not existing:
            db.add(Session(id=session_id))
            await db.commit()


async def _load_history(session_id: uuid.UUID) -> list[dict]:
    """Load conversation history for a session."""
    async with async_session() as db:
        result = await db.execute(
            select(Message).where(Message.session_id == session_id).order_by(Message.created_at)
        )
        messages = result.scalars().all()
        return [{"role": m.role, "content": m.content} for m in messages]


async def _save_message(session_id: uuid.UUID, role: str, content: str) -> None:
    """Save a message to the database."""
    async with async_session() as db:
        db.add(Message(session_id=session_id, role=role, content=content))
        if role == "user":
            session = await db.get(Session, session_id)
            if session and session.title is None:
                session.title = content[:100]
        await db.commit()


@ws_router.websocket("/ws/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: uuid.UUID):
    await websocket.accept()
    await _ensure_session(session_id)

    # Send existing history on connect
    history = await _load_history(session_id)
    if history:
        await websocket.send_text(json.dumps({"type": "history", "messages": history}))

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            user_message = msg.get("content", "")

            if not user_message.strip():
                continue

            await _save_message(session_id, "user", user_message)
            history = await _load_history(session_id)

            # Stream agent response with structured events
            full_response = []
            try:
                async for event in run_agent(user_message, history[:-1]):
                    if event.type == "text":
                        full_response.append(event.content)
                        await websocket.send_text(json.dumps({
                            "type": "token",
                            "content": event.content,
                        }))
                    elif event.type == "agent_start":
                        await websocket.send_text(json.dumps({
                            "type": "agent_start",
                            "agent": event.agent_name,
                        }))
                    elif event.type == "agent_stop":
                        await websocket.send_text(json.dumps({
                            "type": "agent_stop",
                            "agent": event.agent_name,
                        }))
                    elif event.type == "tool_use":
                        await websocket.send_text(json.dumps({
                            "type": "tool_use",
                            "tool": event.content,
                        }))
            except Exception as e:
                await websocket.send_text(json.dumps({"type": "error", "content": str(e)}))
                continue

            assistant_content = "".join(full_response)
            if assistant_content:
                await _save_message(session_id, "assistant", assistant_content)

            await websocket.send_text(json.dumps({"type": "done"}))

    except WebSocketDisconnect:
        pass

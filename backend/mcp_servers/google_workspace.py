"""MCP tools for Google Workspace integration (Gmail + Calendar).

Requires Google OAuth2 credentials. Setup:
1. Create a project in Google Cloud Console
2. Enable Gmail API and Google Calendar API
3. Create OAuth2 credentials (Desktop app)
4. Download credentials.json to the project root
5. On first run, you'll be prompted to authorize in a browser

The tokens are cached in token.json for subsequent use.
"""

import base64
import json
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
]

TOKEN_PATH = Path("token.json")
CREDENTIALS_PATH = Path("credentials.json")


def _get_google_service(service_name: str, version: str):
    """Authenticate and return a Google API service client."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError(
            "Install Google client libraries: "
            "pip install google-auth google-auth-oauthlib google-api-python-client"
        )

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                return None
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())

    return build(service_name, version, credentials=creds)


# --- Gmail Tools ---


def gmail_get_recent(max_results: int = 10, query: str = "is:inbox") -> str:
    """Get recent emails from Gmail.

    Use this to check the user's inbox, find specific emails, or understand
    what needs attention. The Chief of Staff should check this proactively.

    Args:
        max_results: Number of emails to return (default 10, max 50).
        query: Gmail search query (e.g. "is:unread", "from:john@example.com", "subject:invoice").

    Returns:
        Formatted list of recent emails with sender, subject, date, and snippet.
    """
    service = _get_google_service("gmail", "v1")
    if not service:
        return "Gmail not configured. Add credentials.json from Google Cloud Console."

    try:
        results = service.users().messages().list(
            userId="me", q=query, maxResults=min(max_results, 50)
        ).execute()

        messages = results.get("messages", [])
        if not messages:
            return f"No emails matching: {query}"

        formatted = []
        for msg_ref in messages:
            msg = service.users().messages().get(
                userId="me", id=msg_ref["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            ).execute()

            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            formatted.append(
                f"ID: {msg_ref['id']}\n"
                f"From: {headers.get('From', 'Unknown')}\n"
                f"Subject: {headers.get('Subject', '(no subject)')}\n"
                f"Date: {headers.get('Date', 'Unknown')}\n"
                f"Snippet: {msg.get('snippet', '')}\n"
            )
        return "\n---\n".join(formatted)
    except Exception as e:
        return f"Error reading Gmail: {e}"


def gmail_read_email(message_id: str) -> str:
    """Read the full content of a specific email.

    Args:
        message_id: The Gmail message ID (from gmail_get_recent results).

    Returns:
        The full email content including headers and body.
    """
    service = _get_google_service("gmail", "v1")
    if not service:
        return "Gmail not configured."

    try:
        msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}

        # Extract body
        body = _extract_body(msg.get("payload", {}))

        return (
            f"From: {headers.get('From', 'Unknown')}\n"
            f"To: {headers.get('To', 'Unknown')}\n"
            f"Subject: {headers.get('Subject', '(no subject)')}\n"
            f"Date: {headers.get('Date', 'Unknown')}\n\n"
            f"{body}"
        )
    except Exception as e:
        return f"Error reading email: {e}"


def _extract_body(payload: dict) -> str:
    """Extract plain text body from Gmail message payload."""
    if payload.get("mimeType") == "text/plain" and "data" in payload.get("body", {}):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")

    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
        # Recurse into nested parts
        if part.get("parts"):
            result = _extract_body(part)
            if result:
                return result

    return "(Could not extract email body)"


def gmail_draft_reply(
    message_id: str,
    body: str,
    send: bool = False,
) -> str:
    """Draft (or send) a reply to an email.

    By default this creates a DRAFT, not a sent email. The user can review
    and send from Gmail. Set send=True only for autonomy_level="auto" decisions.

    Args:
        message_id: The Gmail message ID to reply to.
        body: The reply body text.
        send: If True, send immediately. If False (default), save as draft.

    Returns:
        Confirmation with draft/sent status.
    """
    service = _get_google_service("gmail", "v1")
    if not service:
        return "Gmail not configured."

    try:
        # Get original message for threading
        original = service.users().messages().get(userId="me", id=message_id, format="metadata",
            metadataHeaders=["From", "Subject", "Message-ID"]).execute()
        headers = {h["name"]: h["value"] for h in original.get("payload", {}).get("headers", [])}

        subject = headers.get("Subject", "")
        if not subject.startswith("Re:"):
            subject = f"Re: {subject}"

        message = MIMEText(body)
        message["to"] = headers.get("From", "")
        message["subject"] = subject
        message["In-Reply-To"] = headers.get("Message-ID", "")
        message["References"] = headers.get("Message-ID", "")

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        if send:
            service.users().messages().send(
                userId="me", body={"raw": raw, "threadId": original.get("threadId")}
            ).execute()
            return f"Reply sent to {headers.get('From', 'Unknown')}."
        else:
            service.users().drafts().create(
                userId="me", body={"message": {"raw": raw, "threadId": original.get("threadId")}}
            ).execute()
            return f"Draft reply created for {headers.get('From', 'Unknown')}. Review in Gmail before sending."

    except Exception as e:
        return f"Error creating reply: {e}"


# --- Google Calendar Tools ---


def calendar_get_events(
    days_ahead: int = 7,
    max_results: int = 20,
) -> str:
    """Get upcoming calendar events.

    Use this to check the user's schedule, find availability, or prepare
    for upcoming meetings.

    Args:
        days_ahead: How many days ahead to look (default 7).
        max_results: Maximum events to return (default 20).

    Returns:
        Formatted list of upcoming events with time, title, and attendees.
    """
    service = _get_google_service("calendar", "v3")
    if not service:
        return "Google Calendar not configured. Add credentials.json from Google Cloud Console."

    try:
        now = datetime.utcnow()
        time_min = now.isoformat() + "Z"
        time_max = (now + timedelta(days=days_ahead)).isoformat() + "Z"

        events_result = service.events().list(
            calendarId="primary", timeMin=time_min, timeMax=time_max,
            maxResults=max_results, singleEvents=True, orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return f"No events in the next {days_ahead} days."

        formatted = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            attendees = [a.get("email", "") for a in event.get("attendees", [])]

            formatted.append(
                f"Event: {event.get('summary', '(no title)')}\n"
                f"When: {start} — {end}\n"
                f"Where: {event.get('location', 'No location')}\n"
                f"Attendees: {', '.join(attendees) if attendees else 'Just you'}\n"
                f"Status: {event.get('status', 'confirmed')}"
            )
        return "\n---\n".join(formatted)
    except Exception as e:
        return f"Error reading calendar: {e}"


def calendar_create_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str = "",
    attendees: str = "",
    location: str = "",
) -> str:
    """Create a new calendar event.

    For autonomy_level="auto" (scheduling), create directly.
    For autonomy_level="recommend", describe the event and wait for approval.

    Args:
        summary: Event title.
        start_time: Start time in ISO format (e.g. "2026-04-10T14:00:00-07:00").
        end_time: End time in ISO format.
        description: Optional event description.
        attendees: Comma-separated email addresses of attendees.
        location: Optional event location.

    Returns:
        Confirmation with event link.
    """
    service = _get_google_service("calendar", "v3")
    if not service:
        return "Google Calendar not configured."

    try:
        event: dict[str, Any] = {
            "summary": summary,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time},
        }

        if description:
            event["description"] = description
        if location:
            event["location"] = location
        if attendees:
            event["attendees"] = [{"email": e.strip()} for e in attendees.split(",")]

        created = service.calendarId("primary").events().insert(
            calendarId="primary", body=event, sendUpdates="all" if attendees else "none",
        ).execute()

        return f"Event created: {created.get('summary')} — {created.get('htmlLink')}"
    except Exception as e:
        return f"Error creating event: {e}"


def calendar_find_free_time(
    days_ahead: int = 5,
    duration_minutes: int = 30,
) -> str:
    """Find available time slots in the user's calendar.

    Use this when scheduling meetings or recommending times.

    Args:
        days_ahead: How many days ahead to search (default 5).
        duration_minutes: Required duration in minutes (default 30).

    Returns:
        List of available time slots.
    """
    service = _get_google_service("calendar", "v3")
    if not service:
        return "Google Calendar not configured."

    try:
        now = datetime.utcnow()
        time_min = now.isoformat() + "Z"
        time_max = (now + timedelta(days=days_ahead)).isoformat() + "Z"

        # Get busy times
        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": "primary"}],
        }
        freebusy = service.freebusy().query(body=body).execute()
        busy_times = freebusy.get("calendars", {}).get("primary", {}).get("busy", [])

        # Find gaps (simplified: working hours 9am-5pm)
        slots = []
        current = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if current < now:
            current += timedelta(days=1)

        for _ in range(days_ahead):
            day_start = current.replace(hour=9, minute=0)
            day_end = current.replace(hour=17, minute=0)
            slot_start = day_start

            for busy in busy_times:
                busy_start = datetime.fromisoformat(busy["start"].replace("Z", "+00:00")).replace(tzinfo=None)
                busy_end = datetime.fromisoformat(busy["end"].replace("Z", "+00:00")).replace(tzinfo=None)

                if busy_start > slot_start and (busy_start - slot_start).total_seconds() >= duration_minutes * 60:
                    slots.append(f"{slot_start.strftime('%a %b %d, %I:%M %p')} — {busy_start.strftime('%I:%M %p')}")
                slot_start = max(slot_start, busy_end)

            if slot_start < day_end and (day_end - slot_start).total_seconds() >= duration_minutes * 60:
                slots.append(f"{slot_start.strftime('%a %b %d, %I:%M %p')} — {day_end.strftime('%I:%M %p')}")

            current += timedelta(days=1)

        if not slots:
            return f"No {duration_minutes}-minute slots available in the next {days_ahead} days."

        return "Available slots:\n" + "\n".join(f"  - {s}" for s in slots[:10])
    except Exception as e:
        return f"Error checking availability: {e}"

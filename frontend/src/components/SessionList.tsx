import { useEffect, useState } from "react";
import type { Session } from "../types";

interface Props {
  currentSessionId: string;
  onSelectSession: (id: string) => void;
  onNewSession: () => void;
}

export default function SessionList({ currentSessionId, onSelectSession, onNewSession }: Props) {
  const [sessions, setSessions] = useState<Session[]>([]);

  useEffect(() => {
    fetch("/sessions")
      .then((r) => r.json())
      .then(setSessions)
      .catch(() => {});
  }, [currentSessionId]);

  return (
    <div className="flex h-full flex-col bg-gray-800">
      <div className="flex items-center justify-between border-b border-gray-700 px-4 py-3">
        <h2 className="text-sm font-semibold text-gray-300">Conversations</h2>
        <button
          onClick={onNewSession}
          className="rounded-lg bg-blue-600 px-3 py-1 text-xs font-medium text-white hover:bg-blue-500"
        >
          + New
        </button>
      </div>
      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 && (
          <p className="px-4 py-6 text-center text-sm text-gray-500">No conversations yet</p>
        )}
        {sessions.map((s) => (
          <button
            key={s.id}
            onClick={() => onSelectSession(s.id)}
            className={`w-full border-b border-gray-700/50 px-4 py-3 text-left transition-colors hover:bg-gray-700 ${
              s.id === currentSessionId ? "bg-gray-700" : ""
            }`}
          >
            <p className="truncate text-sm text-gray-200">
              {s.title || "New conversation"}
            </p>
            <p className="mt-0.5 text-xs text-gray-500">
              {new Date(s.createdAt).toLocaleDateString()}
            </p>
          </button>
        ))}
      </div>
    </div>
  );
}

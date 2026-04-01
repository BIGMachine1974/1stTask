import { useCallback, useState } from "react";
import ChatWindow from "./components/ChatWindow";
import SessionList from "./components/SessionList";
import KnowledgePanel from "./components/KnowledgePanel";

const SESSION_KEY = "agent-team-session-id";

function getSessionId(): string {
  let id = localStorage.getItem(SESSION_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, id);
  }
  return id;
}

export default function App() {
  const [sessionId, setSessionId] = useState(getSessionId);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleNewSession = useCallback(() => {
    const id = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, id);
    setSessionId(id);
    setSidebarOpen(false);
  }, []);

  const handleSelectSession = useCallback((id: string) => {
    localStorage.setItem(SESSION_KEY, id);
    setSessionId(id);
    setSidebarOpen(false);
  }, []);

  return (
    <div className="flex h-dvh bg-gray-900">
      {/* Sidebar — hidden on mobile unless toggled */}
      <div
        className={`fixed inset-y-0 left-0 z-30 w-72 transform transition-transform duration-200 md:relative md:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <SessionList
          currentSessionId={sessionId}
          onSelectSession={handleSelectSession}
          onNewSession={handleNewSession}
        />
        <KnowledgePanel />
      </div>

      {/* Overlay for mobile sidebar */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/50 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main chat area */}
      <div className="flex flex-1 flex-col">
        <ChatWindow
          key={sessionId}
          sessionId={sessionId}
          onToggleSidebar={() => setSidebarOpen((v) => !v)}
        />
      </div>
    </div>
  );
}

import { useEffect, useRef, useState } from "react";
import { useWebSocket } from "../hooks/useWebSocket";
import MessageBubble from "./MessageBubble";
import AgentStatusPanel from "./AgentStatus";

interface Props {
  sessionId: string;
  onToggleSidebar: () => void;
}

export default function ChatWindow({ sessionId, onToggleSidebar }: Props) {
  const { messages, sendMessage, isConnected, isStreaming, activeAgents, lastTool } =
    useWebSocket(sessionId);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    const text = input.trim();
    if (!text || isStreaming) return;
    sendMessage(text);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-full flex-col bg-gray-900">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-700 px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-700 hover:text-white md:hidden"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div>
            <h1 className="text-lg font-semibold text-white">Agent Team</h1>
            <p className="text-xs text-gray-400">Managing Agent + Research, Writing, DevOps</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`h-2.5 w-2.5 rounded-full ${
              isConnected ? "bg-green-500" : "bg-red-500"
            }`}
          />
          <span className="text-xs text-gray-400">
            {isConnected ? "Connected" : "Disconnected"}
          </span>
        </div>
      </div>

      {/* Agent status bar */}
      <AgentStatusPanel agents={activeAgents} lastTool={lastTool} isStreaming={isStreaming} />

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 sm:px-6">
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center">
            <div className="max-w-sm text-center text-gray-500">
              <p className="text-2xl">🤖</p>
              <p className="mt-2 text-lg font-medium">Welcome to Agent Team</p>
              <p className="mt-1 text-sm">
                Your Managing Agent is ready. It coordinates Research, Writing, and DevOps specialists to help you.
              </p>
            </div>
          </div>
        )}
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {isStreaming && messages[messages.length - 1]?.role !== "assistant" && (
          <div className="mb-4 flex justify-start">
            <div className="rounded-2xl bg-gray-700 px-4 py-3 text-gray-400">
              <span className="animate-pulse">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-700 px-4 py-3 sm:px-6 sm:py-4">
        <div className="flex gap-2 sm:gap-3">
          <textarea
            className="flex-1 resize-none rounded-xl border border-gray-600 bg-gray-800 px-3 py-2.5 text-sm text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none sm:px-4 sm:py-3 sm:text-base"
            rows={1}
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={!isConnected}
          />
          <button
            className="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-500 disabled:opacity-50 sm:px-6 sm:py-3 sm:text-base"
            onClick={handleSend}
            disabled={!isConnected || isStreaming || !input.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

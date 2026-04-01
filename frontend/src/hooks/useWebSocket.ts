import { useCallback, useEffect, useRef, useState } from "react";
import type { AgentStatus, Message, WebSocketMessage } from "../types";

function makeId(): string {
  return crypto.randomUUID();
}

export function useWebSocket(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [activeAgents, setActiveAgents] = useState<AgentStatus[]>([]);
  const [lastTool, setLastTool] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const streamBufferRef = useRef("");

  useEffect(() => {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/${sessionId}`);
    wsRef.current = ws;

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => {
      setIsConnected(false);
      setIsStreaming(false);
      setActiveAgents([]);
    };

    ws.onmessage = (event) => {
      const data: WebSocketMessage = JSON.parse(event.data);

      if (data.type === "history" && data.messages) {
        setMessages(
          data.messages.map((m) => ({
            id: makeId(),
            role: m.role,
            content: m.content,
            createdAt: new Date().toISOString(),
          }))
        );
        return;
      }

      if (data.type === "token" && data.content) {
        streamBufferRef.current += data.content;
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last && last.role === "assistant") {
            return [
              ...prev.slice(0, -1),
              { ...last, content: streamBufferRef.current },
            ];
          }
          return [
            ...prev,
            {
              id: makeId(),
              role: "assistant",
              content: streamBufferRef.current,
              createdAt: new Date().toISOString(),
            },
          ];
        });
      }

      if (data.type === "agent_start" && data.agent) {
        setActiveAgents((prev) => [
          ...prev.filter((a) => a.name !== data.agent),
          { name: data.agent!, active: true },
        ]);
      }

      if (data.type === "agent_stop" && data.agent) {
        setActiveAgents((prev) =>
          prev.map((a) =>
            a.name === data.agent ? { ...a, active: false } : a
          )
        );
      }

      if (data.type === "tool_use" && data.tool) {
        setLastTool(data.tool);
      }

      if (data.type === "done") {
        setIsStreaming(false);
        setActiveAgents([]);
        setLastTool(null);
        streamBufferRef.current = "";
      }

      if (data.type === "error") {
        setIsStreaming(false);
        setActiveAgents([]);
        setLastTool(null);
        streamBufferRef.current = "";
        setMessages((prev) => [
          ...prev,
          {
            id: makeId(),
            role: "assistant",
            content: `Error: ${data.content}`,
            createdAt: new Date().toISOString(),
          },
        ]);
      }
    };

    return () => {
      ws.close();
    };
  }, [sessionId]);

  const sendMessage = useCallback((content: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;

    const userMsg: Message = {
      id: makeId(),
      role: "user",
      content,
      createdAt: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsStreaming(true);
    streamBufferRef.current = "";

    wsRef.current.send(JSON.stringify({ content }));
  }, []);

  return { messages, sendMessage, isConnected, isStreaming, activeAgents, lastTool };
}

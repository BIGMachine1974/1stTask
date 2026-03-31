import { useCallback, useEffect, useRef, useState } from "react";
import type { Message, WebSocketMessage } from "../types";

function makeId(): string {
  return crypto.randomUUID();
}

export function useWebSocket(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
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
          if (last && last.role === "assistant" && isStreaming) {
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

      if (data.type === "done") {
        setIsStreaming(false);
        streamBufferRef.current = "";
      }

      if (data.type === "error") {
        setIsStreaming(false);
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

  const sendMessage = useCallback(
    (content: string) => {
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
    },
    []
  );

  return { messages, sendMessage, isConnected, isStreaming };
}

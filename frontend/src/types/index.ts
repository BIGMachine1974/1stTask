export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
}

export interface Session {
  id: string;
  title: string | null;
  createdAt: string;
}

export interface WebSocketMessage {
  type: "token" | "done" | "error" | "history" | "agent_start" | "agent_stop" | "tool_use";
  content?: string;
  messages?: { role: "user" | "assistant"; content: string }[];
  agent?: string;
  tool?: string;
}

export interface AgentStatus {
  name: string;
  active: boolean;
}

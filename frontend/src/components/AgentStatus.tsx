import type { AgentStatus } from "../types";

const AGENT_INFO: Record<string, { label: string; icon: string; color: string }> = {
  research: { label: "Research", icon: "🔍", color: "text-blue-400" },
  writing: { label: "Writing", icon: "✍️", color: "text-green-400" },
  devops: { label: "DevOps", icon: "⚙️", color: "text-orange-400" },
};

interface Props {
  agents: AgentStatus[];
  lastTool: string | null;
  isStreaming: boolean;
}

export default function AgentStatusPanel({ agents, lastTool, isStreaming }: Props) {
  if (!isStreaming) return null;

  const activeAgent = agents.find((a) => a.active);

  return (
    <div className="flex items-center gap-3 border-b border-gray-700 bg-gray-800/50 px-6 py-2 text-sm">
      <span className="text-gray-500">Active:</span>
      {activeAgent ? (
        <span className={AGENT_INFO[activeAgent.name]?.color ?? "text-gray-300"}>
          {AGENT_INFO[activeAgent.name]?.icon ?? "🤖"}{" "}
          {AGENT_INFO[activeAgent.name]?.label ?? activeAgent.name}
        </span>
      ) : (
        <span className="text-purple-400">🧠 Manager</span>
      )}
      {lastTool && (
        <>
          <span className="text-gray-600">|</span>
          <span className="text-gray-400">
            using <code className="rounded bg-gray-700 px-1.5 py-0.5 text-xs">{lastTool}</code>
          </span>
        </>
      )}
      <span className="ml-auto">
        <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-green-500" />
      </span>
    </div>
  );
}

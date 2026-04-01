import { useState } from "react";

export default function KnowledgePanel() {
  const [isOpen, setIsOpen] = useState(false);

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="border-t border-gray-700 px-4 py-3 text-left text-sm text-gray-400 hover:bg-gray-700 hover:text-gray-200"
      >
        📚 Knowledge Base
      </button>
    );
  }

  return (
    <div className="border-t border-gray-700 px-4 py-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-300">📚 Knowledge Base</h3>
        <button
          onClick={() => setIsOpen(false)}
          className="text-gray-500 hover:text-gray-300"
        >
          ✕
        </button>
      </div>
      <p className="mt-2 text-xs text-gray-500">
        Upload files or point to directories to add to your knowledge base.
        The agents will use this context automatically.
      </p>
      <div className="mt-3 rounded-lg border-2 border-dashed border-gray-600 p-4 text-center">
        <p className="text-sm text-gray-400">
          Use the CLI to ingest data:
        </p>
        <code className="mt-1 block rounded bg-gray-900 px-2 py-1 text-xs text-green-400">
          python scripts/ingest.py /path/to/data
        </code>
      </div>
      <div className="mt-3">
        <p className="text-xs text-gray-500">Supported formats:</p>
        <div className="mt-1 flex flex-wrap gap-1">
          {["JSON", "MD", "TXT", "PDF", "PY", "JS", "TS"].map((ext) => (
            <span
              key={ext}
              className="rounded bg-gray-700 px-1.5 py-0.5 text-xs text-gray-400"
            >
              .{ext.toLowerCase()}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

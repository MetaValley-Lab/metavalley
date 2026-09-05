"use client";

import { useState, type FormEvent } from "react";
import { Send } from "lucide-react";

interface MessageInputProps {
  onSend: (content: string) => void;
}

export default function MessageInput({ onSend }: MessageInputProps) {
  const [value, setValue] = useState("");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue("");
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 border-t border-gray-200 p-3">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Digite uma mensagem"
        className="flex-1 rounded-full border border-gray-300 px-4 py-2 text-sm focus:border-[#4735FD] focus:outline-none focus:ring-2 focus:ring-[#4735FD]/30"
      />
      <button
        type="submit"
        aria-label="Enviar mensagem"
        disabled={!value.trim()}
        className="flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-full bg-[#4735FD] text-white hover:bg-[#3c2ce0] disabled:cursor-not-allowed disabled:opacity-50"
      >
        <Send size={18} />
      </button>
    </form>
  );
}


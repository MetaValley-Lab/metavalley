"use client";

import type { ReactNode } from "react";
import { Dialog } from "primereact/dialog";
import { X } from "lucide-react";

interface ModalProps {
  visible: boolean;
  onHide: () => void;
  title: string;
  children: ReactNode;
}

export default function Modal({ visible, onHide, title, children }: ModalProps) {
  return (
    <Dialog
      visible={visible}
      onHide={onHide}
      showHeader={false}
      dismissableMask
      className="w-[95vw] max-w-lg rounded-lg bg-white p-6 shadow-xl"
    >
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-lg font-bold text-gray-900">{title}</h3>
        <button
          type="button"
          onClick={onHide}
          aria-label="Fechar"
          className="cursor-pointer text-gray-400 hover:text-gray-600"
        >
          <X size={20} />
        </button>
      </div>
      {children}
    </Dialog>
  );
}


"use client";

import Modal from "./Modal";
import Button from "./Button";

interface ConfirmModalProps {
  visible: boolean;
  title: string;
  message: string;
  isSubmitting?: boolean;
  onHide: () => void;
  onConfirm: () => void;
}

export default function ConfirmModal({
  visible,
  title,
  message,
  isSubmitting = false,
  onHide,
  onConfirm,
}: ConfirmModalProps) {
  return (
    <Modal visible={visible} onHide={onHide} title={title}>
      <p className="text-sm text-gray-600">{message}</p>
      <div className="mt-6 flex justify-end gap-3">
        <Button label="Cancelar" type="button" onClick={onHide} className="bg-gray-200 text-gray-700 hover:bg-gray-300" />
        <Button label={isSubmitting ? "Excluindo..." : "Excluir"} type="button" onClick={onConfirm} disabled={isSubmitting} className="bg-red-600 hover:bg-red-700" />
      </div>
    </Modal>
  );
}
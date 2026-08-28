import { InputText } from "primereact/inputtext";
import type { InputTextProps } from "primereact/inputtext";

interface TextFieldProps extends InputTextProps {
  id: string;
  label: string;
}

export default function TextField({ id, label, className, ...inputProps }: TextFieldProps) {
  return (
    <div className="flex w-full max-w-sm flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-semibold text-gray-900">
        {label}
      </label>
      <InputText
        id={id}
        className={`rounded-md border border-gray-300 p-2.5 text-sm focus:border-[#4735FD] focus:outline-none focus:ring-2 focus:ring-[#4735FD]/30 ${className ?? ""}`}
        {...inputProps}
      />
    </div>
  );
}
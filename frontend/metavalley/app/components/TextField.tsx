import { forwardRef } from "react";
import { InputText } from "primereact/inputtext";
import type { InputTextProps } from "primereact/inputtext";

interface TextFieldProps extends InputTextProps {
  id: string;
  label: string;
}

const TextField = forwardRef<HTMLInputElement, TextFieldProps>(function TextField(
  { id, label, className, ...inputProps },
  ref,
) {
  return (
    <div className="flex w-full flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-semibold text-gray-900">
        {label}
      </label>
      <InputText
        ref={ref}
        id={id}
        className={`w-full rounded-md border border-gray-300 p-2.5 text-sm focus:border-[#4735FD] focus:outline-none focus:ring-2 focus:ring-[#4735FD]/30 ${className ?? ""}`}
        {...inputProps}
      />
    </div>
  );
});

export default TextField;
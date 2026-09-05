import { Dropdown } from "primereact/dropdown";
import type { DropdownProps } from "primereact/dropdown";

interface SelectFieldProps extends DropdownProps {
  id: string;
  label: string;
}

export default function SelectField({ id, label, className, ...selectProps }: SelectFieldProps) {
  return (
    <div className="flex w-full flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-semibold text-gray-900">
        {label}
      </label>
      <Dropdown
        inputId={id}
        className={`w-full p-2.5 rounded-md border border-gray-300 p-1 text-sm focus:border-[#4735FD] ${className ?? ""}`}
        panelClassName="bg-white border border-gray-200 shadow-xl rounded-md z-50 p-2"
        {...selectProps}
      />
    </div>
  );
}


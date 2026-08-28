import { Button as PrimeButton } from "primereact/button";
import type { ButtonProps } from "primereact/button";

export default function Button({ className, ...buttonProps }: ButtonProps) {
  return (
    <PrimeButton
      type="submit"
      className={`w-full justify-center rounded-md bg-[#4735FD] p-2.5 text-sm font-semibold text-white transition-colors hover:bg-[#3c2ce0] focus:outline-none focus:ring-2 focus:ring-[#4735FD] focus:ring-offset-2 ${className ?? ""}`}
      {...buttonProps}
    />
  );
}
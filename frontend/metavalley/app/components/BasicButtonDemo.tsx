
import React from 'react'; 
import { Button } from 'primereact/button';

interface ButtonProps {
    label: string
}

export default function BasicDemo({label}: ButtonProps) {
    return (
        <div className="card flex w-full bg-[#4735FD] items-center justify-content-center rounded-sm p-2">
            <Button  label={label} className="font-bold text-white justify-content-center w-full"  />
        </div>
    )
}
        
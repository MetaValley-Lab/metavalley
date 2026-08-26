import React from 'react'; 
import { InputText } from "primereact/inputtext";

interface InputTextDemoProps {
    id: string;
    ariaDescribedBy: string;
}

export default function InputTextDemo({ id, ariaDescribedBy }: InputTextDemoProps) {
    return (
        <div className="card flex-column justify-content-center">
            <div className="flex flex-col gap-1 w-full max-w-sm">
                <label className="text-lg font-bold" htmlFor={id}>{id}</label>
                <InputText className="border border-solid border-gray-400 rounded-sm text-xs p-2 focus:outline-none focus:shadow-none" id={id} aria-describedby={ariaDescribedBy} />
            </div>
        </div>
    )
}
        
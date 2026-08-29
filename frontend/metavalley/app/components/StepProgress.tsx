interface StepProgressProps {
  steps: string[];
  currentStep: number;
}

export default function StepProgress({ steps, currentStep }: StepProgressProps) {
  return (
    <div>
      <div className="flex gap-2">
        {steps.map((step, i) => (
          <div
            key={step}
            className={`h-1.5 flex-1 rounded-full ${i <= currentStep ? "bg-[#4735FD]" : "bg-gray-200"}`}
          />
        ))}
      </div>
      <p className="mt-2 text-xs font-medium text-gray-500">
        Etapa {currentStep + 1} de {steps.length}: {steps[currentStep]}
      </p>
    </div>
  );
}


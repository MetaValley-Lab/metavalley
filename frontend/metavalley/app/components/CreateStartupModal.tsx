"use client";

import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  createStartupSchema,
  CreateStartupFormData,
  startupSteps,
  stageOptions,
  revenueModelOptions,
} from "@/features/startups/startup.schema";

import { createStartup } from "@/features/startups/startup.service";
import { brazilianStates } from "@/features/startups/lib/brazilian-states";
import Modal from "@/app/components/Modal";
import TextField from "@/app/components/TextField";
import SelectField from "./SelectField";
import Button from "./Button";
import StepProgress from "./StepProgress";

interface CreateStartupModalProps {
  visible: boolean;
  onHide: () => void;
  onCreated: () => void;
}

export default function CreateStartupModal({ visible, onHide, onCreated }: CreateStartupModalProps) {
  const [step, setStep] = useState(0);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const {
    register,
    control,
    handleSubmit,
    trigger,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateStartupFormData>({
    resolver: zodResolver(createStartupSchema),
    defaultValues: { stage: "idea" },
  });

  const isLastStep = step === startupSteps.length - 1;

  async function goNext(e: React.MouseEvent<HTMLButtonElement>) {

    e.preventDefault();
    
    const valid = await trigger(startupSteps[step].fields);
    if (valid) setStep((s) => s + 1);
  }

  function goBack() {
    setStep((s) => Math.max(0, s - 1));
  }

  function handleClose() {
    reset();
    setStep(0);
    setSubmitError(null);
    onHide();
  }

  async function onSubmit(data: CreateStartupFormData) {
    setSubmitError(null);
    try {
      await createStartup(data);
      reset();
      setStep(0);
      onCreated();
    } catch (err) {
      console.error("Erro ao criar startup:", err);
      setSubmitError("Não foi possível criar a startup agora. Tente novamente.");
    }
  }

  return (
    <Modal visible={visible} onHide={handleClose} title="Criar nova startup">
      <StepProgress steps={startupSteps.map((s) => s.title)} currentStep={step} />

      <form onSubmit={handleSubmit(onSubmit)} className="mt-6 flex flex-col gap-4">
        {step === 0 && (
          <>
            <div className="w-full">
              <TextField id="name" label="Nome da startup" {...register("name")} />
              {errors.name && <p className="mt-1 text-xs text-red-500">{errors.name.message}</p>}
            </div>
            <div>
              <TextField id="description" label="Descrição (opcional)" {...register("description")} />
            </div>
            <div>
              <Controller
                name="target_location"
                control={control}
                render={({ field }) => (
                  <SelectField
                    id="target_location"
                    label="Estado (opcional)"
                    value={field.value ?? null}
                    onChange={(e) => field.onChange(e.value)}
                    options={[...brazilianStates]}
                    showClear
                    placeholder="Selecione o estado"
                  />
                )}
              />
            </div>
          </>
        )}

        {step === 1 && (
          <>
            <div>
              <TextField id="problem" label="Problema (opcional)" {...register("problem")} />
            </div>
            <div>
              <TextField id="solution" label="Solução (opcional)" {...register("solution")} />
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <div>
              <TextField id="segment" label="Segmento (opcional)" {...register("segment")} />
            </div>
            <div>
              <Controller
                name="stage"
                control={control}
                render={({ field }) => (
                  <SelectField
                    id="stage"
                    label="Estágio"
                    value={field.value}
                    onChange={(e) => field.onChange(e.value)}
                    options={[...stageOptions]}
                  />
                )}
              />
            </div>
            <div>
              <Controller
                name="primary_revenue_model"
                control={control}
                render={({ field }) => (
                  <SelectField
                    id="primary_revenue_model"
                    label="Modelo de receita (opcional)"
                    value={field.value ?? null}
                    onChange={(e) => field.onChange(e.value)}
                    options={[...revenueModelOptions]}
                    showClear
                    placeholder="Selecione um modelo"
                  />
                )}
              />
            </div>
            <div>
              <TextField
                id="revenue_model_details"
                label="Detalhes do modelo de receita (opcional)"
                {...register("revenue_model_details")}
              />
            </div>
          </>
        )}

        {submitError && <p className="text-xs text-red-500">{submitError}</p>}

        <div className="mt-2 flex items-center justify-between">
          {step > 0 ? (
            <button
              type="button"
              onClick={goBack}
              className="cursor-pointer w-full text-sm font-semibold text-gray-500 hover:text-gray-700"
            >
              Voltar
            </button>
          ) : (
            <span />
          )}

          {isLastStep ? (
            <Button
              label={isSubmitting ? "Criando..." : "Criar startup"}
              type="submit"
              disabled={isSubmitting}
              className="w-auto px-6"
            />
          ) : (
            <Button label="Próximo" type="button" onClick={(e) => goNext(e)} className="w-auto px-6" />
          )}
        </div>
      </form>
    </Modal>
  );
}


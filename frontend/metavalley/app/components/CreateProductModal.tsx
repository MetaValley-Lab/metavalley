"use client";

import { useEffect, useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  createProductSchema,
  type CreateProductFormData,
  productSteps,
  productTypeOptions,
  productStageOptions,
} from "@/features/startups/products/product.schema";
import { createProduct, updateProduct, uploadProductImage } from "@/features/startups/products/product.service";
import type { Product } from "@/features/startups/products/product.types";
import Modal from "@/app/components/Modal";
import TextField from "@/app/components/TextField";
import SelectField from "@/app/components/SelectField";
import Button from "@/app/components/Button";
import StepProgress from "@/app/components/StepProgress";

interface CreateProductModalProps {
  startupId: string;
  visible: boolean;
  onHide: () => void;
  onCreated: () => void;
  product?: Product | null;
}

export default function CreateProductModal({
  startupId,
  visible,
  onHide,
  onCreated,
  product = null,
}: CreateProductModalProps) {
  const [step, setStep] = useState(0);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);

  const {
    register,
    control,
    handleSubmit,
    trigger,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateProductFormData>({
    resolver: zodResolver(createProductSchema),
    defaultValues: { stage: "idea" },
  });

  const isLastStep = step === productSteps.length - 1;

  useEffect(() => {
    if (visible && product) {
      reset({
        name: product.name,
        description: product.description ?? undefined,
        type: product.type,
        price: product.price === null ? undefined : String(product.price),
        stage: product.stage,
      });
    }
  }, [product, reset, visible]);

  async function goNext(e: React.MouseEvent<HTMLButtonElement>) {
    e.preventDefault();
    const valid = await trigger(productSteps[step].fields);
    if (valid) setStep((s) => s + 1);
  }

  function goBack(e: React.MouseEvent<HTMLButtonElement>) {
    e.preventDefault();
    setStep((s) => Math.max(0, s - 1));
  }

  function handleClose() {
    reset();
    setImageFile(null);
    setStep(0);
    setSubmitError(null);
    onHide();
  }

  async function onSubmit(data: CreateProductFormData) {
    setSubmitError(null);
    try {
      const payload = {
        name: data.name,
        description: data.description || undefined,
        type: data.type,
        price: data.price ? Number(data.price) : undefined,
        stage: data.stage,
      };
      if (product) {
        await updateProduct(product.id, payload);
        if (imageFile) await uploadProductImage(product.id, imageFile);
      } else {
        const createdProduct = await createProduct({ startup_id: startupId, ...payload });
        if (imageFile) await uploadProductImage(createdProduct.id, imageFile);
      }
      reset();
      setImageFile(null);
      setStep(0);
      onCreated();
    } catch (err) {
      console.error("Erro ao salvar produto:", err);
      setSubmitError("Não foi possível salvar o produto agora. Tente novamente.");
    }
  }

  return (
    <Modal visible={visible} onHide={handleClose} title={product ? "Editar produto" : "Criar novo produto"}>
      <StepProgress
        steps={productSteps.map((s) => s.title)}
        currentStep={step}
      />

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="mt-6 flex flex-col gap-4"
      >
        {step === 0 && (
          <>
            <div>
              <TextField
                id="name"
                label="Nome do produto"
                {...register("name")}
              />
              {errors.name && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.name.message}
                </p>
              )}
            </div>
            <div>
              <label htmlFor="product-image" className="mb-1 block text-sm font-medium text-gray-700">Imagem do produto (opcional)</label>
              <input id="product-image" type="file" accept="image/jpeg,image/png,image/webp" onChange={(event) => setImageFile(event.target.files?.[0] ?? null)} className="block w-full text-sm text-gray-600" />
              {imageFile && <p className="mt-1 text-xs text-gray-500">{imageFile.name}</p>}
            </div>
            <div>
              <TextField
                id="description"
                label="Descrição (opcional)"
                {...register("description")}
              />
            </div>
            <div>
              <Controller
                name="type"
                control={control}
                render={({ field }) => (
                  <SelectField
                    id="type"
                    label="Tipo de produto"
                    value={field.value ?? null}
                    onChange={(e) => field.onChange(e.value)}
                    options={[...productTypeOptions]}
                    placeholder="Selecione o tipo"
                  />
                )}
              />
              {errors.type && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.type.message}
                </p>
              )}
            </div>
          </>
        )}

        {step === 1 && (
          <>
            <div>
              <TextField
                id="price"
                label="Preço (opcional)"
                type="number"
                min={0}
                step="0.01"
                {...register("price")}
              />
              {errors.price && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.price.message}
                </p>
              )}
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
                    options={[...productStageOptions]}
                  />
                )}
              />
            </div>
          </>
        )}

        {submitError && <p className="text-xs text-red-500">{submitError}</p>}


        <div className="w-full mt-6 flex ">
          {step > 0 ? (
            <button
              type="button"
              onClick={goBack}
              className="w-full cursor-pointer text-sm font-semibold text-gray-500 hover:text-gray-700 transition-colors"
            >
              Voltar
            </button>
          ) : (
            <span />
          )}

          {isLastStep ? (
            <Button
              label={isSubmitting ? "Salvando..." : product ? "Salvar alterações" : "Criar produto"}
              type="submit"
              disabled={isSubmitting}
              className="w-full"
            />
          ) : (
            <Button
              label="Próximo"
              type="button"
              onClick={goNext}
              className="w-full"
            />
          )}
        </div>
      </form>
    </Modal>
  );
}


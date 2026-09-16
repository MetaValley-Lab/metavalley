"use client";

import Link from "next/link";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Button from "@/app/components/Button";
import TextField from "@/app/components/TextField";
import {
  forgotPasswordSchema,
  type ForgotPasswordFormData,
} from "@/features/auth/auth.schema";
import { requestPasswordReset } from "@/features/auth/auth.service";

export default function ForgotPasswordPage() {
  const [message, setMessage] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ForgotPasswordFormData>({ resolver: zodResolver(forgotPasswordSchema) });

  async function onSubmit(data: ForgotPasswordFormData) {
    setMessage(null);
    setSubmitError(null);
    try {
      const response = await requestPasswordReset(data.email);
      setMessage(response.message);
    } catch (error) {
      console.error("Erro ao solicitar restauração de senha:", error);
      setSubmitError("Não foi possível solicitar a restauração agora. Tente novamente.");
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <form className="w-full max-w-sm" onSubmit={handleSubmit(onSubmit)}>
        <h1 className="mb-2 text-3xl font-bold text-gray-900">Restaurar senha</h1>
        <p className="mb-6 text-sm text-gray-500">
          Informe seu e-mail e enviaremos as instruções para criar uma nova senha.
        </p>

        <div className="mb-6">
          <TextField
            id="email"
            label="E-mail"
            type="email"
            autoComplete="email"
            {...register("email")}
            required
          />
          {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email.message}</p>}
        </div>

        {message && <p className="mb-4 text-sm text-green-600">{message}</p>}
        {submitError && <p className="mb-4 text-sm text-red-500">{submitError}</p>}

        <Button
          label={isSubmitting ? "Enviando..." : "Enviar instruções"}
          type="submit"
          disabled={isSubmitting}
        />

        <p className="mt-4 text-center text-xs text-gray-500">
          <Link href="/auth/login" className="font-bold text-[#4735fd]">Voltar para o login</Link>
        </p>
      </form>
    </main>
  );
}
"use client";

import Link from "next/link";
import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Button from "@/app/components/Button";
import TextField from "@/app/components/TextField";
import {
  resetPasswordSchema,
  type ResetPasswordFormData,
} from "@/features/auth/auth.schema";
import { resetPassword } from "@/features/auth/auth.service";

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={<main className="flex min-h-screen items-center justify-center p-6" />}>
      <ResetPasswordForm />
    </Suspense>
  );
}

function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const code = searchParams.get("code");
  const [hashCredentials, setHashCredentials] = useState<{
    accessToken: string;
    refreshToken: string;
  } | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ResetPasswordFormData>({ resolver: zodResolver(resetPasswordSchema) });

  useEffect(() => {
    const params = new URLSearchParams(window.location.hash.replace(/^#/, ""));
    const accessToken = params.get("access_token");
    const refreshToken = params.get("refresh_token");

    if (accessToken && refreshToken) {
      // Supabase exposes recovery credentials in the URL fragment after mount.
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setHashCredentials({ accessToken, refreshToken });
    }
  }, []);

  const hasCredentials = Boolean(code || hashCredentials);

  async function onSubmit(data: ResetPasswordFormData) {
    setSubmitError(null);
    if (!hasCredentials) {
      setSubmitError("O link de restauração é inválido ou expirou.");
      return;
    }

    try {
      await resetPassword(
        hashCredentials
          ? { accessToken: hashCredentials.accessToken, refreshToken: hashCredentials.refreshToken }
          : { code: code ?? undefined },
        data.password,
      );
      setSuccess(true);
    } catch (error) {
      console.error("Erro ao restaurar senha:", error);
      setSubmitError("Não foi possível restaurar a senha. Solicite um novo link.");
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <form className="w-full max-w-sm" onSubmit={handleSubmit(onSubmit)}>
        <h1 className="mb-2 text-3xl font-bold text-gray-900">Criar nova senha</h1>
        <p className="mb-6 text-sm text-gray-500">Escolha uma senha com pelo menos 8 caracteres.</p>

        {!hasCredentials && <p className="mb-4 text-sm text-red-500">Link de restauração inválido ou expirado.</p>}
        {success ? (
          <>
            <p className="mb-4 text-sm text-green-600">Senha restaurada com sucesso.</p>
            <Link href="/auth/login" className="text-sm font-bold text-[#4735fd]">Ir para o login</Link>
          </>
        ) : (
          <>
            <div className="mb-4">
              <TextField id="password" label="Nova senha" type="password" autoComplete="new-password" {...register("password")} required />
              {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password.message}</p>}
            </div>
            <div className="mb-6">
              <TextField id="confirm_password" label="Confirmar nova senha" type="password" autoComplete="new-password" {...register("confirm_password")} required />
              {errors.confirm_password && <p className="mt-1 text-xs text-red-500">{errors.confirm_password.message}</p>}
            </div>
            {submitError && <p className="mb-4 text-sm text-red-500">{submitError}</p>}
            <Button label={isSubmitting ? "Salvando..." : "Restaurar senha"} type="submit" disabled={isSubmitting || !hasCredentials} />
          </>
        )}
      </form>
    </main>
  );
}
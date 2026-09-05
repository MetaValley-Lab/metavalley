"use client";

import Link from "next/link";
import TextField from "@/app/components/TextField";
import Button from "@/app/components/Button";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, LoginFormData } from "@/features/auth/auth.schema";
import { login } from "@/features/auth/auth.service";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const router = useRouter();

  async function onSubmit(data: LoginFormData) {
    try {
      const response = await login(data);

      if (!response) {
        throw new Error("Erro ao fazer login. Tente novamente mais tarde.");
      }

      router.push("/home");
    } catch (error) {
      console.error("Erro ao login: ", error);
    }
  }

  return (
    <div className="flex min-h-screen w-full gap-4 p-6">
      {/* Coluna esquerda: reservada para imagem, oculta em telas pequenas */}
      <div className="relative hidden overflow-hidden rounded-md lg:block lg:w-1/2">
        <Image
          src="/images/login-image.png"
          alt="Ilustração de login"
          fill
          sizes="(max-width: 1024px) 100vw, 50vw"
          priority
          className="object-cover"
        />
      </div>

      {/* TODO: trocar pelo componente <Image> do next/image quando a arte final estiver em /public */}

      {/* Coluna direita: formulário */}
      <div className="flex w-full flex-1 items-center justify-center">
        <form className="w-full max-w-sm" onSubmit={handleSubmit(onSubmit)}>
          <h2 className="mb-2 text-center text-4xl font-bold">
            Seja Bem-vindo
          </h2>
          <p className="mb-6 text-center text-xs text-gray-400">
            Acesse suas startups e a valide suas ideias
          </p>

          <div className="mb-6 flex flex-col gap-4">
            <div>
              <TextField
                id="email"
                label="E-mail"
                type="email"
                autoComplete="email"
                {...register("email")}
                required
              />

              {errors.email && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.email.message}
                </p>
              )}
            </div>
            <div>
              <TextField
                id="password"
                label="Senha"
                type="password"
                autoComplete="current-password"
                {...register("password")}
                required
              />

              {errors.password && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.password.message}
                </p>
              )}
            </div>
          </div>

          <Button
            label={isSubmitting ? "Entrando..." : "Fazer login"}
            type="submit"
            disabled={isSubmitting}
          />

          <p className="mt-4 text-center text-xs text-gray-500">
            Não possui uma conta?{" "}
            <Link href="/auth/register" className="font-bold text-[#4735fd]">
              Crie uma
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}

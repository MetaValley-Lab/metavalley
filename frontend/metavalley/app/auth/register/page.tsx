"use client";

import Link from "next/link";
import TextField from "@/app/components/TextField";
import Button from "@/app/components/Button";
import { useForm } from "react-hook-form";
import {
  RegisterFormData,
  userRegisterSchema,
} from "@/features/auth/auth.schema";
import { zodResolver } from "@hookform/resolvers/zod";
import { register as registerUser } from "@/features/auth/auth.service";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function RegisterPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData, typeof userRegisterSchema>({
    resolver: zodResolver(userRegisterSchema),
  });

  const router = useRouter();

  async function onSubmit(data: RegisterFormData) {
    try {
      if (data.password != data.confirm_password) {
        throw new Error("As senhas não coincidem");
      }

      const response = await registerUser(data);
      if (response) {
        router.push("/auth/login");
      }
    } catch (error) {
      console.error("Erro ao criar uma conta", error);
    }
  }

  return (
    <div className="flex min-h-screen w-full gap-4 p-6">
      {/* Coluna esquerda: reservada para imagem, oculta em telas pequenas */}
      <div className="relative hidden overflow-hidden rounded-md lg:block lg:w-1/2">
        <Image
          src="/images/register-ilustration.jpg"
          alt="Ilustração de registro"
          fill
          sizes="(max-width: 1024px) 100vw, 50vw"
          priority
          className="object-cover"
        />
      </div>
      {/* TODO: trocar pelo componente <Image> do next/image quando a arte final estiver em /public */}

      {/* Coluna direita: formulário */}
      <div className="flex w-full flex-1 items-center justify-center py-10">
        <form className="w-full max-w-sm" onSubmit={handleSubmit(onSubmit)}>
          <h2 className="mb-2 text-4xl font-bold">Crie a sua conta</h2>
          <p className="mb-6 text-xs text-gray-400">
            Comece a validar suas ideias antes mesmo de construí-las
          </p>

          <div className="mb-6 flex flex-col gap-4">
            <div>
              <TextField
                id="username"
                label="Nome de usuário"
                type="text"
                autoComplete="username"
                {...register("username")}
                required
              />
              {errors.username && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.username.message}
                </p>
              )}
            </div>
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
                autoComplete="password"
                {...register("password")}
                required
              />
              {errors.password && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.password.message}
                </p>
              )}
            </div>
            <div>
              <TextField
                id="confirm_password"
                label="Confirmar Senha"
                type="password"
                autoComplete="confirm_password"
                {...register("confirm_password")}
                required
              />
              {errors.confirm_password && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.confirm_password.message}
                </p>
              )}
            </div>
            <div>
              <TextField
                id="phoneNumber"
                label="Número de Telefone"
                type="tel"
                autoComplete="tel"
                {...register("phone_number")}
                required
              />
              {errors.phone_number && (
                <p className="mt-1 text-xs text-red-500">
                  {errors.phone_number.message}
                </p>
              )}
            </div>
          </div>

          <Button
            label={isSubmitting ? "Carregando..." : "Criar conta"}
            type="submit"
            disabled={isSubmitting}
          />

          <p className="mt-4 text-center text-xs text-gray-500">
            Possui uma conta?{" "}
            <Link href="/auth/login" className="font-bold text-[#4735fd]">
              Faça login
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}

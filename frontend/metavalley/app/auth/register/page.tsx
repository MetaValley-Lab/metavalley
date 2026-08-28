import type { Metadata } from "next";
import Link from "next/link";
import TextField from "@/app/components/TextField";
import Button from "@/app/components/Button";

export const metadata: Metadata = {
  title: "Criar conta",
};

export default function RegisterPage() {
  return (
    <div className="flex min-h-screen w-full gap-4 p-6">
      {/* Coluna esquerda: reservada para imagem, oculta em telas pequenas */}
      <div className="hidden rounded-md bg-[#D9D9D9] lg:block lg:w-1/2" />
      {/* TODO: trocar pelo componente <Image> do next/image quando a arte final estiver em /public */}

      {/* Coluna direita: formulário */}
      <div className="flex w-full flex-1 items-center justify-center py-10">
        <form className="w-full max-w-sm">
          <h2 className="mb-2 text-4xl font-bold">Crie a sua conta</h2>
          <p className="mb-6 text-xs text-gray-400">
            Comece a validar suas ideias antes mesmo de construí-las
          </p>

          <div className="mb-6 flex flex-col gap-4">
            <TextField
              id="username"
              label="Nome de usuário"
              type="text"
              autoComplete="username"
              required
            />
            <TextField
              id="email"
              label="E-mail"
              type="email"
              autoComplete="email"
              required
            />
            <TextField
              id="senha"
              label="Senha"
              type="password"
              autoComplete="new-password"
              required
            />
            <TextField
              id="confirmar-senha"
              label="Confirmar Senha"
              type="password"
              autoComplete="new-password"
              required
            />
            <TextField
              id="telefone"
              label="Número de Telefone"
              type="tel"
              autoComplete="tel"
              required
            />
          </div>

          <Button label="Criar conta" />

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


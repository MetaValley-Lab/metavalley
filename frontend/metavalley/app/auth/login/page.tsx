import type { Metadata } from "next";
import Link from "next/link";
import TextField from "@/app/components/TextField";
import Button from "@/app/components/Button";

export const metadata: Metadata = {
  title: "Login",
};

export default function LoginPage() {
  return (
    <div className="flex min-h-screen w-full gap-4 p-6">
      {/* Coluna esquerda: reservada para imagem, oculta em telas pequenas */}
      <div className="hidden rounded-md bg-[#D9D9D9] lg:block lg:w-1/2" />
      {/* TODO: trocar pelo componente <Image> do next/image quando a arte final estiver em /public */}

      {/* Coluna direita: formulário */}
      <div className="flex w-full flex-1 items-center justify-center">
        <form className="w-full max-w-sm">
          <h2 className="mb-2 text-center text-4xl font-bold">Seja Bem-vindo</h2>
          <p className="mb-6 text-center text-xs text-gray-400">
            Acesse suas startups e a valide suas ideias
          </p>

          <div className="mb-6 flex flex-col gap-4">
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
              autoComplete="current-password"
              required
            />
          </div>

          <Button label="Fazer login" />

          <p className="mt-4 text-center text-xs text-gray-500">
            Não possui uma conta?{" "}
            <Link href="/auth/cadastro" className="font-bold text-[#4735fd]">
              Crie uma
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}


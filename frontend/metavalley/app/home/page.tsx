import type { Metadata } from "next";
import Sidebar from "@/app/components/Sidebar";
import Carousel from "@/app/components/Carousel";
import StartupsGrid from "@/app/components/StartupsGrid";

export const metadata: Metadata = {
  title: "Home",
};

// TODO: trocar "Samir" pelo nome do usuário autenticado assim que houver
// um contexto/sessão de usuário disponível no client.
const userName = "Samir";

export default function HomePage() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />

      <main className="flex-1 p-8">
        <h1 className="mb-4 text-2xl font-bold text-gray-900">Seja Bem-vindo, {userName}</h1>

        <Carousel
          slides={[
            {
              id: "placeholder-1",
              content: (
                <div className="flex h-full w-full items-center justify-center text-sm text-gray-400">
                  Espaço para propaganda ou insight da startup
                </div>
              ),
            },
          ]}
        />
        {/* TODO: alimentar os slides com base no plano do usuário (propaganda MetaValley
            vs. insights da startup) assim que essa lógica existir no backend */}

        <div className="mt-8">
          <StartupsGrid />
        </div>
      </main>
    </div>
  );
}

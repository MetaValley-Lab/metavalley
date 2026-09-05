import type { Metadata } from "next";
import Sidebar from "@/app/components/Sidebar";
import StartupInsightsCarousel from "../components/StartupInsightsCarousel";
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

        <StartupInsightsCarousel />

        <div className="mt-8">
          <StartupsGrid />
        </div>
      </main>
    </div>
  );
}

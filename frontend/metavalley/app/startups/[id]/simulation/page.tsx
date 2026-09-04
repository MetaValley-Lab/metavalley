import SimulationPromo from "@/app/components/SimulationPromo";

export default async function StartupSimulationPage({ params }: PageProps<"/startups/[id]/simulation">) {
  const { id } = await params;

  return <SimulationPromo startupId={id} />;
}
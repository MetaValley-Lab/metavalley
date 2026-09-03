import PlanningList from "@/app/components/PlanningList";

export default async function StartupTasksPage({ params }: PageProps<"/startups/[id]/tasks">) {
  const { id } = await params;

  return <PlanningList startupId={id} />;
}


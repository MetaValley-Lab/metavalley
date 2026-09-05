import Sidebar from "@/app/components/Sidebar";
import StartupWorkspaceShell from "@/app/components/StartupWorkspaceShell";

export default async function StartupLayout({ children, params }: LayoutProps<"/startups/[id]">) {
  const { id } = await params;

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1 overflow-y-auto">
        <StartupWorkspaceShell startupId={id}>{children}</StartupWorkspaceShell>
      </div>
    </div>
  );
}


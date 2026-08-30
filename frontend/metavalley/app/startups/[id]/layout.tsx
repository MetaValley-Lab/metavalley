import StartupWorkspaceShell from "@/app/components/StartupWorkspaceShell";

interface LayoutProps {
  children: React.ReactNode;
  params: Promise<{ id: string }>; // No Next.js 15+, params é uma Promise
}

export default async function StartupLayout({ children, params }: LayoutProps) {
  const { id } = await params;

  return <StartupWorkspaceShell startupId={id}>{children}</StartupWorkspaceShell>;
}


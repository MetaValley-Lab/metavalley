import ChatLayout from "@/app/components/ChatLayout";

interface StartupChatPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function StartupChatPage({ params }: StartupChatPageProps) {
  const { id } = await params;
  return <ChatLayout startupId={id} />;
}


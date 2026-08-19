-- ========================================================
-- MIGRAÇÃO: Conversations e Messages
-- ========================================================

-- 1. Enums
CREATE TYPE conversation_type AS ENUM (
    'onboarding',
    'group',
    'ceo',
    'cto',
    'cfo',
    'cmo'
);

CREATE TYPE message_role AS ENUM ('user', 'agent');

-- 2. Tabela conversations
-- Cada startup tem uma conversa por tipo (group, onboarding, ceo, etc.)
CREATE TABLE IF NOT EXISTS public.conversations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    startup_id  UUID NOT NULL REFERENCES public.startups(id) ON DELETE CASCADE,
    type        conversation_type NOT NULL DEFAULT 'group',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT conversations_startup_type_unique UNIQUE (startup_id, type)
);

ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Usuários podem ver conversas de suas startups"
    ON public.conversations FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.startups
        WHERE startups.id = conversations.startup_id
        AND startups.user_id = auth.uid()
    ));

CREATE POLICY "Usuários podem criar conversas para suas startups"
    ON public.conversations FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.startups
        WHERE startups.id = conversations.startup_id
        AND startups.user_id = auth.uid()
    ));

-- 3. Tabela messages
CREATE TABLE IF NOT EXISTS public.messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    role            message_role NOT NULL,
    agent_name      actor_role,          -- NULL para mensagens do founder
    content         TEXT NOT NULL,
    actions         JSONB,               -- Auditoria das actions executadas
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id
    ON public.messages(conversation_id, created_at);

ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Usuários podem ver mensagens de suas startups"
    ON public.messages FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.conversations
        JOIN public.startups ON startups.id = conversations.startup_id
        WHERE conversations.id = messages.conversation_id
        AND startups.user_id = auth.uid()
    ));

CREATE POLICY "Usuários podem criar mensagens em suas conversas"
    ON public.messages FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.conversations
        JOIN public.startups ON startups.id = conversations.startup_id
        WHERE conversations.id = messages.conversation_id
        AND startups.user_id = auth.uid()
    ));
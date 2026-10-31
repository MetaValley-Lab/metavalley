-- ========================================================
-- MIGRAÇÃO: Correção de Segurança e Blindagem de RLS
-- ========================================================

-- Correção 1: Garantir segurança estrita na criação de mensagens
DROP POLICY IF EXISTS "Usuários podem criar mensagens em suas conversas" ON public.messages;

CREATE POLICY "Usuários podem criar mensagens em suas conversas"
    ON public.messages FOR INSERT
    WITH CHECK (
        -- Garante que a conversa pertence ao usuário autenticado
        EXISTS (
            SELECT 1 FROM public.conversations
            JOIN public.startups ON startups.id = conversations.startup_id
            WHERE conversations.id = messages.conversation_id
            AND startups.user_id = auth.uid()
        )
        AND
        -- Proteção de engenharia social: O usuário comum NUNCA pode fingir ser um agente de IA
        (role = 'user' AND agent_name IS NULL)
    );

-- Correção 2: Blindagem da tabela de demonstração de interesse (simulation_interests)
DROP POLICY IF EXISTS "Usuários podem demonstrar interesse" ON public.simulation_interests;

CREATE POLICY "Usuários podem demonstrar interesse"
    ON public.simulation_interests FOR INSERT
    WITH CHECK (
        auth.uid() = user_id
        AND 
        -- Garante que ele só pode interagir com startups legítimas cadastradas
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = simulation_interests.startup_id
        )
    );


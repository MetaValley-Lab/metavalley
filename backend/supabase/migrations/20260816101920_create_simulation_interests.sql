-- 1. Criação da tabela
CREATE TABLE IF NOT EXISTS public.simulation_interests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    startup_id UUID NOT NULL REFERENCES public.startups(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT simulation_interests_user_startup_unique
        UNIQUE (user_id, startup_id)
);


-- 2. Habilitar RLS
ALTER TABLE public.simulation_interests ENABLE ROW LEVEL SECURITY;


-- 3. Políticas de acesso
CREATE POLICY "Usuários podem visualizar seus próprios interesses"
    ON public.simulation_interests FOR SELECT
    USING (auth.uid() = user_id);


CREATE POLICY "Usuários podem demonstrar interesse"
    ON public.simulation_interests FOR INSERT
    WITH CHECK (
        auth.uid() = user_id
        AND EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = simulation_interests.startup_id
        )
    );


CREATE POLICY "Usuários podem remover seus próprios interesses"
    ON public.simulation_interests FOR DELETE
    USING (auth.uid() = user_id);



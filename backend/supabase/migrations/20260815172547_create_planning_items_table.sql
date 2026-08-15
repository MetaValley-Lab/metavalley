-- 1. Criação do tipo ENUM para os atores (Agentes IA + Fundador)
CREATE TYPE actor_role AS ENUM ('founder', 'ceo', 'cto', 'cfo', 'cmo');

-- 2. Criação da tabela
CREATE TABLE IF NOT EXISTS public.planning_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    startup_id UUID NOT NULL REFERENCES public.startups(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_by actor_role NOT NULL DEFAULT 'founder',
    last_updated_by actor_role NOT NULL DEFAULT 'founder',
    completed BOOLEAN DEFAULT false,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Trigger para updated_at
CREATE TRIGGER update_planning_items_updated_at
    BEFORE UPDATE ON public.planning_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 4. Habilitar RLS
ALTER TABLE public.planning_items ENABLE ROW LEVEL SECURITY;

-- 5. Políticas de Acesso RLS
CREATE POLICY "Usuários podem ver itens de suas startups" 
    ON public.planning_items FOR SELECT 
    USING (EXISTS (SELECT 1 FROM public.startups WHERE startups.id = planning_items.startup_id AND startups.user_id = auth.uid()));

CREATE POLICY "Usuários podem criar itens para suas startups" 
    ON public.planning_items FOR INSERT 
    WITH CHECK (EXISTS (SELECT 1 FROM public.startups WHERE startups.id = planning_items.startup_id AND startups.user_id = auth.uid()));

CREATE POLICY "Usuários podem atualizar itens de suas startups" 
    ON public.planning_items FOR UPDATE 
    USING (EXISTS (SELECT 1 FROM public.startups WHERE startups.id = planning_items.startup_id AND startups.user_id = auth.uid()));

CREATE POLICY "Usuários podem deletar itens de suas startups" 
    ON public.planning_items FOR DELETE 
    USING (EXISTS (SELECT 1 FROM public.startups WHERE startups.id = planning_items.startup_id AND startups.user_id = auth.uid()));

    
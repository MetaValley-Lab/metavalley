-- 1. Criação dos tipos ENUM para as zonas do Canvas e seus status
CREATE TYPE canvas_zone_key AS ENUM (
    'value_proposition',
    'customer_segments',
    'acquisition_channels',
    'revenue_model',
    'cost_structure',
    'key_resource',
    'success_metrics'
);


CREATE TYPE canvas_zone_status AS ENUM (
    'filled',
    'in_progress',
    'to_define'
);


-- 2. Criação da tabela canvas_zones
CREATE TABLE IF NOT EXISTS public.canvas_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    startup_id UUID NOT NULL REFERENCES public.startups(id) ON DELETE CASCADE,
    zone_key canvas_zone_key NOT NULL,
    content TEXT,
    status canvas_zone_status NOT NULL DEFAULT 'to_define',
    filled_by actor_role NOT NULL DEFAULT 'founder',
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    previous_content TEXT,

    CONSTRAINT canvas_zones_startup_zone_unique
        UNIQUE (startup_id, zone_key)
);


-- 3. Trigger para atualização automática do updated_at
CREATE TRIGGER update_canvas_zones_updated_at
    BEFORE UPDATE ON public.canvas_zones
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- 4. Habilitar RLS
ALTER TABLE public.canvas_zones ENABLE ROW LEVEL SECURITY;


-- 5. Políticas de acesso RLS

CREATE POLICY "Usuários podem ver zonas do Canvas de suas startups"
    ON public.canvas_zones FOR SELECT
    USING (
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = canvas_zones.startup_id
              AND startups.user_id = auth.uid()
        )
    );


CREATE POLICY "Usuários podem criar zonas do Canvas de suas startups"
    ON public.canvas_zones FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = canvas_zones.startup_id
              AND startups.user_id = auth.uid()
        )
    );


CREATE POLICY "Usuários podem atualizar zonas do Canvas de suas startups"
    ON public.canvas_zones FOR UPDATE
    USING (
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = canvas_zones.startup_id
              AND startups.user_id = auth.uid()
        )
    );


CREATE POLICY "Usuários podem deletar zonas do Canvas de suas startups"
    ON public.canvas_zones FOR DELETE
    USING (
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = canvas_zones.startup_id
              AND startups.user_id = auth.uid()
        )
    );
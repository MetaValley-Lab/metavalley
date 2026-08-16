-- 1. Criação dos tipos ENUM para produtos
CREATE TYPE product_type AS ENUM (
    'saas',
    'marketplace',
    'app',
    'hardware',
    'service',
    'other'
);


CREATE TYPE product_stage AS ENUM (
    'idea',
    'prototype',
    'mvp',
    'launched'
);


-- 2. Criação da tabela products
CREATE TABLE IF NOT EXISTS public.products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    startup_id UUID NOT NULL REFERENCES public.startups(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type product_type NOT NULL,
    price NUMERIC(12, 2),
    stage product_stage NOT NULL DEFAULT 'idea',
    last_updated_by actor_role NOT NULL DEFAULT 'founder',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);


-- 3. Trigger para atualização automática do updated_at
CREATE TRIGGER update_products_updated_at
    BEFORE UPDATE ON public.products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- 4. Habilitar RLS
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;


-- 5. Políticas de acesso RLS

CREATE POLICY "Usuários podem ver produtos de suas startups"
    ON public.products FOR SELECT
    USING (
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = products.startup_id
              AND startups.user_id = auth.uid()
        )
    );


CREATE POLICY "Usuários podem criar produtos para suas startups"
    ON public.products FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = products.startup_id
              AND startups.user_id = auth.uid()
        )
    );


CREATE POLICY "Usuários podem atualizar produtos de suas startups"
    ON public.products FOR UPDATE
    USING (
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = products.startup_id
              AND startups.user_id = auth.uid()
        )
    );


CREATE POLICY "Usuários podem deletar produtos de suas startups"
    ON public.products FOR DELETE
    USING (
        EXISTS (
            SELECT 1
            FROM public.startups
            WHERE startups.id = products.startup_id
              AND startups.user_id = auth.uid()
        )
    );
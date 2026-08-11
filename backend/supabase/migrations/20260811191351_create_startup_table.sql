-- 1. Criação dos tipos ENUM
CREATE TYPE startup_stage AS ENUM ('idea', 'mvp', 'launched');

CREATE TYPE revenue_model AS ENUM (
    'subscription', 
    'saas', 
    'marketplace', 
    'freemium',
    'pay_per_use', 
    'licensing', 
    'advertising',
    'e_commerce', 
    'service', 
    'hardware', 
    'other'
);

CREATE TYPE startup_status AS ENUM ('active', 'archived');

-- 2. Criação da tabela startups
CREATE TABLE IF NOT EXISTS public.startups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    problem TEXT,
    solution TEXT,
    segment VARCHAR(255),
    target_location VARCHAR(255),
    stage startup_stage DEFAULT 'idea',
    primary_revenue_model revenue_model,
    revenue_model_details TEXT,
    status startup_status DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Função e Trigger para atualização automática do updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_startups_updated_at
    BEFORE UPDATE ON public.startups
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 4. Habilitar RLS (Row Level Security)
ALTER TABLE public.startups ENABLE ROW LEVEL SECURITY;

-- 5. Políticas de Acesso RLS
CREATE POLICY "Usuários podem visualizar suas próprias startups" 
    ON public.startups FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Usuários podem criar suas próprias startups" 
    ON public.startups FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Usuários podem atualizar suas próprias startups" 
    ON public.startups FOR UPDATE 
    USING (auth.uid() = user_id);

CREATE POLICY "Usuários podem deletar suas próprias startups" 
    ON public.startups FOR DELETE 
    USING (auth.uid() = user_id);
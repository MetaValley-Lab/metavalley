-- ========================================================
-- MIGRAÇÃO 001: Estrutura Inicial de Perfis de Usuários
-- ========================================================

-- 1. Criar tipo Enumerado para os Planos
CREATE TYPE public.type_plan AS ENUM ('free', 'pro');

-- 2. Criar a tabela 'profiles' vinculada ao auth.users
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL PRIMARY KEY,
    username TEXT UNIQUE,
    phone_number TEXT,
    avatar_url TEXT,
    plan public.type_plan DEFAULT 'free'::public.type_plan NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Habilitar Row Level Security (RLS)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- 4. Criar Políticas de Acesso (Policies)
CREATE POLICY "Usuários podem ver o próprio perfil" 
ON public.profiles 
FOR SELECT 
USING (auth.uid() = id);

CREATE POLICY "Usuários podem atualizar o próprio perfil" 
ON public.profiles 
FOR UPDATE 
USING (auth.uid() = id);

-- 5. Função Trigger para automatizar criação do perfil
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, username, phone_number, avatar_url, plan)
    VALUES (
        new.id,
        new.raw_user_meta_data->>'username',
        new.raw_user_meta_data->>'phone_number',
        new.raw_user_meta_data->>'avatar_url',
        'free'::public.type_plan
    );
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 6. Trigger disparado quando um novo usuário se cadastra no Auth
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();


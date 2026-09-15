-- ========================================================
-- MIGRAÇÃO: image_url em profiles, startups e products + Storage buckets
-- ========================================================

-- 1. Adicionar image_url nas tabelas
ALTER TABLE public.profiles
    ADD COLUMN IF NOT EXISTS image_url TEXT;

ALTER TABLE public.startups
    ADD COLUMN IF NOT EXISTS image_url TEXT;

ALTER TABLE public.products
    ADD COLUMN IF NOT EXISTS image_url TEXT;


-- 2. Criar buckets públicos no Supabase Storage
-- (public = true → URLs não precisam de token para leitura)
INSERT INTO storage.buckets (id, name, public)
VALUES
    ('avatars',        'avatars',        true),
    ('startup-images', 'startup-images', true),
    ('product-images', 'product-images', true)
ON CONFLICT (id) DO NOTHING;


-- 3. RLS policies para o bucket de avatars
--    Estrutura do path: {user_id}/avatar.{ext}

CREATE POLICY "Avatars: usuário autenticado faz upload do próprio avatar"
    ON storage.objects FOR INSERT
    WITH CHECK (
        bucket_id = 'avatars'
        AND auth.role() = 'authenticated'
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

CREATE POLICY "Avatars: usuário autenticado atualiza o próprio avatar"
    ON storage.objects FOR UPDATE
    USING (
        bucket_id = 'avatars'
        AND auth.role() = 'authenticated'
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

CREATE POLICY "Avatars: usuário autenticado deleta o próprio avatar"
    ON storage.objects FOR DELETE
    USING (
        bucket_id = 'avatars'
        AND auth.role() = 'authenticated'
        AND (storage.foldername(name))[1] = auth.uid()::text
    );

CREATE POLICY "Avatars: leitura pública"
    ON storage.objects FOR SELECT
    USING (bucket_id = 'avatars');


-- 4. RLS policies para startup-images
--    Estrutura do path: {startup_id}/image.{ext}
--    Upload permitido apenas para o dono da startup

CREATE POLICY "Startup images: founder faz upload"
    ON storage.objects FOR INSERT
    WITH CHECK (
        bucket_id = 'startup-images'
        AND auth.role() = 'authenticated'
        AND EXISTS (
            SELECT 1 FROM public.startups
            WHERE startups.id::text = (storage.foldername(name))[1]
            AND startups.user_id = auth.uid()
        )
    );

CREATE POLICY "Startup images: founder atualiza"
    ON storage.objects FOR UPDATE
    USING (
        bucket_id = 'startup-images'
        AND auth.role() = 'authenticated'
        AND EXISTS (
            SELECT 1 FROM public.startups
            WHERE startups.id::text = (storage.foldername(name))[1]
            AND startups.user_id = auth.uid()
        )
    );

CREATE POLICY "Startup images: founder deleta"
    ON storage.objects FOR DELETE
    USING (
        bucket_id = 'startup-images'
        AND auth.role() = 'authenticated'
        AND EXISTS (
            SELECT 1 FROM public.startups
            WHERE startups.id::text = (storage.foldername(name))[1]
            AND startups.user_id = auth.uid()
        )
    );

CREATE POLICY "Startup images: leitura pública"
    ON storage.objects FOR SELECT
    USING (bucket_id = 'startup-images');


-- 5. RLS policies para product-images
--    Estrutura do path: {product_id}/image.{ext}

CREATE POLICY "Product images: founder faz upload"
    ON storage.objects FOR INSERT
    WITH CHECK (
        bucket_id = 'product-images'
        AND auth.role() = 'authenticated'
        AND EXISTS (
            SELECT 1 FROM public.products
            JOIN public.startups ON startups.id = products.startup_id
            WHERE products.id::text = (storage.foldername(name))[1]
            AND startups.user_id = auth.uid()
        )
    );

CREATE POLICY "Product images: founder atualiza"
    ON storage.objects FOR UPDATE
    USING (
        bucket_id = 'product-images'
        AND auth.role() = 'authenticated'
        AND EXISTS (
            SELECT 1 FROM public.products
            JOIN public.startups ON startups.id = products.startup_id
            WHERE products.id::text = (storage.foldername(name))[1]
            AND startups.user_id = auth.uid()
        )
    );

CREATE POLICY "Product images: founder deleta"
    ON storage.objects FOR DELETE
    USING (
        bucket_id = 'product-images'
        AND auth.role() = 'authenticated'
        AND EXISTS (
            SELECT 1 FROM public.products
            JOIN public.startups ON startups.id = products.startup_id
            WHERE products.id::text = (storage.foldername(name))[1]
            AND startups.user_id = auth.uid()
        )
    );

CREATE POLICY "Product images: leitura pública"
    ON storage.objects FOR SELECT
    USING (bucket_id = 'product-images');


-- Asesor Financiero: esquema base. Todas las tablas con RLS por user_id.

create extension if not exists pgcrypto;

create table public.accounts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  nombre text not null,
  tipo text not null check (tipo in ('debito','credito','efectivo','ahorro')),
  dia_corte smallint check (dia_corte between 1 and 31),
  dia_limite_pago smallint check (dia_limite_pago between 1 and 31),
  saldo_actual numeric(14,2) not null default 0,
  created_at timestamptz not null default now()
);

create table public.categories (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  nombre text not null,
  presupuesto_mensual numeric(14,2) not null default 0,
  color_neutro text not null default '#525252',
  created_at timestamptz not null default now(),
  unique (user_id, nombre)
);

create table public.transactions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  account_id uuid references public.accounts(id) on delete set null,
  fecha date not null,
  descripcion_original text not null,
  comercio text,
  monto numeric(14,2) not null check (monto >= 0),
  tipo text not null check (tipo in ('gasto','ingreso')),
  category_id uuid references public.categories(id) on delete set null,
  requiere_revision boolean not null default false,
  es_recurrente boolean not null default false,
  hash_unico text not null,
  created_at timestamptz not null default now(),
  unique (user_id, hash_unico)
);
create index transactions_user_fecha_idx on public.transactions (user_id, fecha desc);
create index transactions_revision_idx on public.transactions (user_id) where requiere_revision;

create table public.categorization_rules (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  patron_texto text not null,
  category_id uuid not null references public.categories(id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (user_id, patron_texto)
);

create table public.savings_goals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  nombre text not null,
  monto_objetivo numeric(14,2) not null check (monto_objetivo > 0),
  monto_actual numeric(14,2) not null default 0,
  fecha_objetivo date not null,
  created_at timestamptz not null default now()
);

create table public.scheduled_payments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  nombre text not null,
  monto numeric(14,2) not null check (monto >= 0),
  frecuencia text not null check (frecuencia in ('mensual','anual','unica')),
  proximo_vencimiento date not null,
  account_id uuid references public.accounts(id) on delete set null,
  created_at timestamptz not null default now()
);

create table public.imports (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  nombre_archivo text not null,
  ruta_storage text,
  estado text not null default 'pendiente' check (estado in ('pendiente','procesado','confirmado','error')),
  movimientos_detectados integer not null default 0,
  created_at timestamptz not null default now()
);

-- RLS: cada usuario solo ve y modifica sus filas.
do $$
declare t text;
begin
  foreach t in array array['accounts','categories','transactions','categorization_rules','savings_goals','scheduled_payments','imports']
  loop
    execute format('alter table public.%I enable row level security', t);
    execute format('create policy "own_select" on public.%I for select using (auth.uid() = user_id)', t);
    execute format('create policy "own_insert" on public.%I for insert with check (auth.uid() = user_id)', t);
    execute format('create policy "own_update" on public.%I for update using (auth.uid() = user_id) with check (auth.uid() = user_id)', t);
    execute format('create policy "own_delete" on public.%I for delete using (auth.uid() = user_id)', t);
  end loop;
end $$;

-- Storage: bucket privado para estados de cuenta, carpeta por usuario (<user_id>/archivo.pdf).
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('statements', 'statements', false, 15728640, array['application/pdf'])
on conflict (id) do nothing;

create policy "statements_select" on storage.objects for select
  using (bucket_id = 'statements' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "statements_insert" on storage.objects for insert
  with check (bucket_id = 'statements' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "statements_delete" on storage.objects for delete
  using (bucket_id = 'statements' and (storage.foldername(name))[1] = auth.uid()::text);

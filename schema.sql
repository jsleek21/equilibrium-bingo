-- Equilibrium League Bingo — schema
-- Run this once in Supabase: Project → SQL Editor → New query → paste → Run

create extension if not exists pgcrypto;

-- Master item pool (curated by you in the admin tool)
create table if not exists items (
  id uuid primary key default gen_random_uuid(),
  region text not null,
  name text not null,
  level text not null default '—',
  icon text,               -- data: URI, may be null
  approved boolean not null default false,
  obtained boolean not null default false,
  obtained_at timestamptz,
  created_at timestamptz not null default now(),
  unique (region, name)
);

-- One row per viewer card
create table if not exists cards (
  id uuid primary key default gen_random_uuid(),
  username text not null unique,      -- lowercased Twitch username
  layout jsonb not null,              -- array of 25 item ids (or item objects), in board order
  created_at timestamptz not null default now()
);

-- Row Level Security: public read on both tables, public write only where needed.
-- NOTE: this project has no server, so "admin" access is enforced only by a
-- client-side password prompt in admin.html, not by real auth. Anyone who knows
-- the admin password (or inspects the page) could write directly via the API.
-- Acceptable for a low-stakes Twitch community tool; upgrade to Supabase Auth
-- later if it ever needs real security.

alter table items enable row level security;
alter table cards enable row level security;

create policy "public read items" on items
  for select using (true);
create policy "public write items" on items
  for insert with check (true);
create policy "public update items" on items
  for update using (true);

create policy "public read cards" on cards
  for select using (true);
create policy "public write cards" on cards
  for insert with check (true);
create policy "public update cards" on cards
  for update using (true);

-- Enable realtime so viewer pages get live updates when you mark a drop,
-- and so the admin tool's Drop impact / Viewer cards tabs update live too.
alter publication supabase_realtime add table items;
alter publication supabase_realtime add table cards;

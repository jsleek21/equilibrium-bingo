-- Adds a real "rejected" state, separate from "approved" and "not yet reviewed".
-- Run in Supabase: Project → SQL Editor → New query → paste → Run
alter table items add column if not exists rejected boolean not null default false;

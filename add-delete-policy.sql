-- Fixes a bug: DELETE requests to `cards` were silently no-ops because no
-- RLS policy allowed deletes. PostgREST returns 204 (success) even when a
-- delete matches zero rows, so this failed silently in the admin UI.
-- Run in Supabase: Project → SQL Editor → New query → paste → Run
create policy "public delete cards" on cards
  for delete using (true);

import { createClient } from "@supabase/supabase-js";

// Solo para crons y rutas de servidor. Nunca importar desde código de cliente.
export function createAdminClient() {
  return createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!, {
    auth: { persistSession: false },
  });
}

import { Suspense } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { formatMoney } from "@/lib/format";
import { requireUser } from "@/lib/auth";
import { deleteTransaction } from "./actions";
import { TransactionForm } from "./transaction-form";

async function Content() {
  const { supabase } = await requireUser();
  const [accounts, categories, txs] = await Promise.all([
    supabase.from("accounts").select("id,nombre").order("nombre"),
    supabase.from("categories").select("id,nombre").order("nombre"),
    supabase
      .from("transactions")
      .select("id,fecha,descripcion_original,monto,tipo,requiere_revision,es_recurrente,categories(nombre),accounts(nombre)")
      .order("fecha", { ascending: false })
      .limit(100),
  ]);
  const today = new Intl.DateTimeFormat("sv-SE", { timeZone: process.env.APP_TIMEZONE ?? "America/Bogota" }).format(new Date());

  return (
    <>
      <TransactionForm accounts={accounts.data ?? []} categories={categories.data ?? []} today={today} />
      <div className="space-y-2">
        {txs.data?.map((t) => {
          const cat = t.categories as unknown as { nombre: string } | null;
          const acc = t.accounts as unknown as { nombre: string } | null;
          return (
            <Card key={t.id} className="flex items-center gap-3 py-3">
              <div className="min-w-0 flex-1">
                <p className="truncate font-medium">{t.descripcion_original}</p>
                <p className="text-xs text-neutral-500">
                  {t.fecha} · {cat?.nombre ?? "Sin categoría"}
                  {acc ? ` · ${acc.nombre}` : ""}
                  {t.es_recurrente ? " · recurrente" : ""}
                  {t.requiere_revision ? " · por revisar" : ""}
                </p>
              </div>
              <span className="text-sm font-semibold">
                {t.tipo === "gasto" ? "−" : "+"}
                {formatMoney(Number(t.monto))}
              </span>
              <form action={deleteTransaction}>
                <input type="hidden" name="id" value={t.id} />
                <Button size="sm" variant="ghost">✕</Button>
              </form>
            </Card>
          );
        })}
        {!txs.data?.length && <p className="text-sm text-neutral-500">Aún no hay movimientos.</p>}
      </div>
    </>
  );
}

export default function MovimientosPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Movimientos</h1>
      <Suspense fallback={<p className="text-sm text-neutral-500">Cargando…</p>}>
        <Content />
      </Suspense>
    </div>
  );
}

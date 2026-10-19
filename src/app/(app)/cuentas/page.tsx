import { Suspense } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { formatMoney } from "@/lib/format";
import { requireUser } from "@/lib/auth";
import { addAccount, deleteAccount, updateBalance } from "./actions";

async function Accounts() {
  const { supabase } = await requireUser();
  const { data } = await supabase.from("accounts").select("*").order("created_at");
  if (!data?.length) return <p className="text-sm text-neutral-500">Aún no tienes cuentas.</p>;
  return (
    <div className="space-y-2">
      {data.map((a) => (
        <Card key={a.id} className="flex flex-wrap items-center gap-3">
          <div className="min-w-0 flex-1">
            <p className="font-medium">{a.nombre}</p>
            <p className="text-xs text-neutral-500">
              {a.tipo}
              {a.dia_corte ? ` · corte día ${a.dia_corte}` : ""}
              {a.dia_limite_pago ? ` · pago día ${a.dia_limite_pago}` : ""}
            </p>
          </div>
          <form action={updateBalance} className="flex items-center gap-2">
            <input type="hidden" name="id" value={a.id} />
            <Input name="saldo_actual" type="number" step="1" defaultValue={Number(a.saldo_actual)} className="w-36" />
            <Button size="sm" variant="outline">Guardar</Button>
          </form>
          <span className="text-sm font-semibold">{formatMoney(Number(a.saldo_actual))}</span>
          <form action={deleteAccount}>
            <input type="hidden" name="id" value={a.id} />
            <Button size="sm" variant="ghost">Eliminar</Button>
          </form>
        </Card>
      ))}
    </div>
  );
}

export default function CuentasPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Cuentas</h1>
      <Card>
        <form action={addAccount} className="grid gap-2 sm:grid-cols-3">
          <Input name="nombre" placeholder="Nombre (ej. Bancolombia débito)" required className="sm:col-span-3" />
          <select name="tipo" className="h-10 rounded-md border border-neutral-300 bg-white px-3" defaultValue="debito">
            <option value="debito">Débito</option>
            <option value="credito">Crédito</option>
            <option value="efectivo">Efectivo</option>
            <option value="ahorro">Ahorro</option>
          </select>
          <Input name="saldo_actual" type="number" step="1" placeholder="Saldo actual" />
          <span />
          <Input name="dia_corte" type="number" min={1} max={31} placeholder="Día de corte (crédito)" />
          <Input name="dia_limite_pago" type="number" min={1} max={31} placeholder="Día límite de pago (crédito)" />
          <Button type="submit">Agregar cuenta</Button>
        </form>
      </Card>
      <Suspense fallback={<p className="text-sm text-neutral-500">Cargando…</p>}>
        <Accounts />
      </Suspense>
    </div>
  );
}

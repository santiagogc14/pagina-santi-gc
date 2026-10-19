"use client";

import { useActionState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { addTransaction } from "./actions";

type Option = { id: string; nombre: string };

export function TransactionForm({ accounts, categories, today }: { accounts: Option[]; categories: Option[]; today: string }) {
  const [state, action, pending] = useActionState(addTransaction, undefined);
  const select = "h-10 w-full rounded-md border border-neutral-300 bg-white px-3";
  return (
    <Card>
      <form action={action} className="grid gap-2 sm:grid-cols-2">
        <Input name="monto" type="number" inputMode="numeric" step="1" placeholder="Monto" required />
        <Input name="fecha" type="date" defaultValue={today} required />
        <Input name="descripcion" placeholder="Descripción (ej. Éxito mercado)" required className="sm:col-span-2" />
        <select name="tipo" className={select} defaultValue="gasto">
          <option value="gasto">Gasto</option>
          <option value="ingreso">Ingreso</option>
        </select>
        <select name="account_id" className={select} defaultValue="">
          <option value="">Sin cuenta</option>
          {accounts.map((a) => <option key={a.id} value={a.id}>{a.nombre}</option>)}
        </select>
        <select name="category_id" className={`${select} sm:col-span-2`} defaultValue="">
          <option value="">Sin categoría</option>
          {categories.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </select>
        {state?.error && <p className="text-sm text-excedido sm:col-span-2">{state.error}</p>}
        {state?.ok && <p className="text-sm text-neutral-600 sm:col-span-2">Movimiento guardado.</p>}
        <Button type="submit" disabled={pending} className="sm:col-span-2">{pending ? "Guardando…" : "Agregar movimiento"}</Button>
      </form>
    </Card>
  );
}

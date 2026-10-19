import { Suspense } from "react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { requireUser } from "@/lib/auth";
import { addCategory, deleteCategory, updateBudget } from "./actions";

async function Categories() {
  const { supabase } = await requireUser();
  const { data } = await supabase.from("categories").select("*").order("nombre");
  if (!data?.length) return <p className="text-sm text-neutral-500">Aún no tienes categorías.</p>;
  return (
    <div className="space-y-2">
      {data.map((c) => (
        <Card key={c.id} className="flex flex-wrap items-center gap-3">
          <span className="h-3 w-3 rounded-full" style={{ background: c.color_neutro }} />
          <span className="min-w-0 flex-1 font-medium">{c.nombre}</span>
          <form action={updateBudget} className="flex items-center gap-2">
            <input type="hidden" name="id" value={c.id} />
            <Input name="presupuesto_mensual" type="number" step="1" defaultValue={Number(c.presupuesto_mensual)} className="w-36" />
            <Button size="sm" variant="outline">Guardar</Button>
          </form>
          <form action={deleteCategory}>
            <input type="hidden" name="id" value={c.id} />
            <Button size="sm" variant="ghost">Eliminar</Button>
          </form>
        </Card>
      ))}
    </div>
  );
}

export default function CategoriasPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Categorías y presupuesto mensual</h1>
      <Card>
        <form action={addCategory} className="grid gap-2 sm:grid-cols-4">
          <Input name="nombre" placeholder="Nombre (ej. Mercado)" required className="sm:col-span-2" />
          <Input name="presupuesto_mensual" type="number" step="1" placeholder="Presupuesto mensual" />
          <input name="color_neutro" type="color" defaultValue="#525252" className="h-10 w-full rounded-md border border-neutral-300" />
          <Button type="submit" className="sm:col-span-4">Agregar categoría</Button>
        </form>
      </Card>
      <Suspense fallback={<p className="text-sm text-neutral-500">Cargando…</p>}>
        <Categories />
      </Suspense>
    </div>
  );
}

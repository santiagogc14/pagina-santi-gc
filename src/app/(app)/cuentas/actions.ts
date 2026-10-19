"use server";

import { revalidatePath } from "next/cache";
import { requireUser } from "@/lib/auth";

const TIPOS = ["debito", "credito", "efectivo", "ahorro"];
const day = (v: FormDataEntryValue | null) => (v ? Math.min(31, Math.max(1, Number(v))) : null);

export async function addAccount(formData: FormData) {
  const { supabase } = await requireUser();
  const tipo = String(formData.get("tipo"));
  if (!TIPOS.includes(tipo)) return;
  await supabase.from("accounts").insert({
    nombre: String(formData.get("nombre")).trim(),
    tipo,
    dia_corte: tipo === "credito" ? day(formData.get("dia_corte")) : null,
    dia_limite_pago: tipo === "credito" ? day(formData.get("dia_limite_pago")) : null,
    saldo_actual: Number(formData.get("saldo_actual") || 0),
  });
  revalidatePath("/cuentas");
}

export async function updateBalance(formData: FormData) {
  const { supabase } = await requireUser();
  await supabase
    .from("accounts")
    .update({ saldo_actual: Number(formData.get("saldo_actual") || 0) })
    .eq("id", String(formData.get("id")));
  revalidatePath("/cuentas");
}

export async function deleteAccount(formData: FormData) {
  const { supabase } = await requireUser();
  await supabase.from("accounts").delete().eq("id", String(formData.get("id")));
  revalidatePath("/cuentas");
}

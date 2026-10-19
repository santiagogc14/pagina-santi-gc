"use server";

import { revalidatePath } from "next/cache";
import { requireUser } from "@/lib/auth";
import { txHash } from "@/lib/hash";

export async function addTransaction(_prev: { error?: string; ok?: boolean } | undefined, formData: FormData) {
  const { supabase } = await requireUser();
  const monto = Math.abs(Number(formData.get("monto")));
  const fecha = String(formData.get("fecha"));
  const descripcion = String(formData.get("descripcion")).trim();
  const tipo = formData.get("tipo") === "ingreso" ? "ingreso" : "gasto";
  if (!monto || !fecha || !descripcion) return { error: "Completa monto, fecha y descripción." };

  const { error } = await supabase.from("transactions").insert({
    account_id: String(formData.get("account_id") || "") || null,
    category_id: String(formData.get("category_id") || "") || null,
    fecha,
    descripcion_original: descripcion,
    comercio: descripcion,
    monto,
    tipo,
    hash_unico: txHash(fecha, monto, descripcion),
  });
  if (error) return { error: error.code === "23505" ? "Ese movimiento ya existe." : error.message };

  revalidatePath("/movimientos");
  return { ok: true };
}

export async function deleteTransaction(formData: FormData) {
  const { supabase } = await requireUser();
  await supabase.from("transactions").delete().eq("id", String(formData.get("id")));
  revalidatePath("/movimientos");
}

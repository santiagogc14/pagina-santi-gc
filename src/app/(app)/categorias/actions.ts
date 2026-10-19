"use server";

import { revalidatePath } from "next/cache";
import { requireUser } from "@/lib/auth";

export async function addCategory(formData: FormData) {
  const { supabase } = await requireUser();
  await supabase.from("categories").insert({
    nombre: String(formData.get("nombre")).trim(),
    presupuesto_mensual: Number(formData.get("presupuesto_mensual") || 0),
    color_neutro: String(formData.get("color_neutro") || "#525252"),
  });
  revalidatePath("/categorias");
}

export async function updateBudget(formData: FormData) {
  const { supabase } = await requireUser();
  await supabase
    .from("categories")
    .update({ presupuesto_mensual: Number(formData.get("presupuesto_mensual") || 0) })
    .eq("id", String(formData.get("id")));
  revalidatePath("/categorias");
}

export async function deleteCategory(formData: FormData) {
  const { supabase } = await requireUser();
  await supabase.from("categories").delete().eq("id", String(formData.get("id")));
  revalidatePath("/categorias");
}

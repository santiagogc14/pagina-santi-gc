import { createHash } from "node:crypto";

export function normalizeText(s: string) {
  return s.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase().replace(/\s+/g, " ").trim();
}

// hash_unico: fecha + monto + descripción normalizada, para descartar duplicados.
export function txHash(fecha: string, monto: number, descripcion: string) {
  return createHash("sha256").update(`${fecha}|${monto.toFixed(2)}|${normalizeText(descripcion)}`).digest("hex");
}

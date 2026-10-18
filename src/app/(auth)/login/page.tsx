"use client";

import { useActionState } from "react";
import { login } from "./actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";

export default function LoginPage() {
  const [state, action, pending] = useActionState(login, undefined);

  return (
    <main className="flex flex-1 items-center justify-center p-4">
      <Card className="w-full max-w-sm space-y-4">
        <h1 className="text-xl font-semibold">Asesor Financiero</h1>
        <form action={action} className="space-y-3">
          <Input name="email" type="email" placeholder="Correo" autoComplete="email" required />
          <Input name="password" type="password" placeholder="Contraseña" autoComplete="current-password" required />
          {state?.error && <p className="text-sm text-excedido">{state.error}</p>}
          <Button type="submit" className="w-full" disabled={pending}>
            {pending ? "Entrando…" : "Entrar"}
          </Button>
        </form>
      </Card>
    </main>
  );
}

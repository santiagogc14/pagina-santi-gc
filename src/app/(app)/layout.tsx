import Link from "next/link";
import { logout } from "../(auth)/login/actions";

const links = [
  { href: "/dashboard", label: "Resumen" },
  { href: "/movimientos", label: "Movimientos" },
  { href: "/importar", label: "Importar" },
  { href: "/por-revisar", label: "Por revisar" },
  { href: "/metas", label: "Metas" },
  { href: "/calendario", label: "Calendario" },
  { href: "/cuentas", label: "Cuentas" },
  { href: "/categorias", label: "Categorías" },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-1 flex-col">
      <header className="sticky top-0 z-10 border-b border-neutral-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center gap-3 px-4 py-3">
          <span className="font-semibold">Asesor Financiero</span>
          <form action={logout} className="ml-auto">
            <button className="text-sm text-neutral-500 hover:text-neutral-900">Salir</button>
          </form>
        </div>
        <nav className="mx-auto flex max-w-5xl gap-4 overflow-x-auto px-4 pb-2 text-sm text-neutral-600">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className="whitespace-nowrap hover:text-neutral-900">
              {l.label}
            </Link>
          ))}
        </nav>
      </header>
      <main className="mx-auto w-full max-w-5xl flex-1 p-4">{children}</main>
    </div>
  );
}

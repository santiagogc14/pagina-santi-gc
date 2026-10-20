"use client";

import { useEffect, useState } from "react";

const KEY = "vista-escritorio";

function applyViewport(desktop: boolean) {
  const meta = document.querySelector('meta[name="viewport"]');
  meta?.setAttribute("content", desktop ? "width=1100" : "width=device-width, initial-scale=1");
}

export function DesktopToggle() {
  const [desktop, setDesktop] = useState(false);

  useEffect(() => {
    try {
      if (localStorage.getItem(KEY) === "1") {
        // eslint-disable-next-line react-hooks/set-state-in-effect -- leer localStorage solo es posible tras montar
        setDesktop(true);
        applyViewport(true);
      }
    } catch {}
  }, []);

  function toggle() {
    const next = !desktop;
    setDesktop(next);
    applyViewport(next);
    try {
      localStorage.setItem(KEY, next ? "1" : "0");
    } catch {}
  }

  return (
    <button
      onClick={toggle}
      className={`text-sm text-neutral-500 hover:text-neutral-900 ${desktop ? "" : "md:hidden"}`}
    >
      {desktop ? "Versión móvil" : "Versión de PC"}
    </button>
  );
}

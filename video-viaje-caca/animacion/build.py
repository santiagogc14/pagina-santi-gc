#!/usr/bin/env python3
"""Genera compositions/*.html desde src/*.html.

- {{POPO id}}  -> SVG de Popo con ids prefijados
- {{POPOJS}}   -> helpers de animación de Popo
- compositions/captions.html se genera desde ../voz/guion.txt + ../voz/tiempos.json
Ejecuta:  python3 build.py
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "compositions"


def popo(pid: str) -> str:
    return f'''<svg viewBox="-20 -10 340 300" width="100%" height="100%" overflow="visible">
  <g id="{pid}-b">
    <g id="{pid}-arms" stroke="#3A2312" stroke-width="9" stroke-linecap="round" fill="none">
      <path id="{pid}-al" d="M40,222 L2,192"/>
      <path id="{pid}-ar" d="M260,222 L298,192"/>
    </g>
    <g stroke="#3A2312" stroke-width="8" stroke-linejoin="round">
      <path d="M150,84 C146,52 170,40 190,26 C186,52 196,64 174,86 Z" fill="#7A4C2A"/>
      <rect x="88" y="76" width="124" height="62" rx="31" fill="#7A4C2A"/>
      <rect x="52" y="128" width="196" height="72" rx="36" fill="#8A5A35"/>
      <rect x="22" y="188" width="256" height="74" rx="37" fill="#9A6740"/>
    </g>
    <g stroke="#C08A5C" stroke-width="7" stroke-linecap="round" fill="none" opacity=".8">
      <path d="M108,92 Q125,84 140,86"/><path d="M74,146 Q92,138 112,140"/><path d="M44,206 Q62,198 84,200"/>
    </g>
    <ellipse cx="96" cy="212" rx="18" ry="10" fill="#FF8FA3" opacity=".55"/>
    <ellipse cx="204" cy="212" rx="18" ry="10" fill="#FF8FA3" opacity=".55"/>
    <g id="{pid}-eyes">
      <ellipse cx="120" cy="164" rx="24" ry="28" fill="#fff" stroke="#3A2312" stroke-width="6"/>
      <ellipse cx="180" cy="164" rx="24" ry="28" fill="#fff" stroke="#3A2312" stroke-width="6"/>
      <g id="{pid}-pup">
        <circle cx="124" cy="168" r="11" fill="#1B1B1B"/><circle cx="184" cy="168" r="11" fill="#1B1B1B"/>
        <circle cx="128" cy="163" r="4" fill="#fff"/><circle cx="188" cy="163" r="4" fill="#fff"/>
      </g>
    </g>
    <g id="{pid}-brows" opacity="0" stroke="#3A2312" stroke-width="8" stroke-linecap="round">
      <path d="M98,128 L136,138"/><path d="M202,128 L164,138"/>
    </g>
    <g id="{pid}-mouths">
      <path id="{pid}-m-smile" d="M120,214 Q150,252 180,214 Z" fill="#3A140A" stroke="#3A2312" stroke-width="5" stroke-linejoin="round"/>
      <ellipse id="{pid}-m-o" cx="150" cy="228" rx="15" ry="20" fill="#3A140A" opacity="0"/>
      <path id="{pid}-m-frown" d="M126,236 Q150,214 174,236" fill="none" stroke="#3A140A" stroke-width="8" stroke-linecap="round" opacity="0"/>
    </g>
    <path id="{pid}-sweat" d="M250,96 C240,116 238,128 250,132 C262,128 260,116 250,96 Z" fill="#8FD8FF" stroke="#2C6E91" stroke-width="4" opacity="0"/>
  </g>
</svg>'''


POPOJS = r'''
const P = {
  mood(tl, id, mood, t) {
    const all = ["smile", "o", "frown"];
    tl.to(`#${id}-b`, { scaleY: 0.86, scaleX: 1.08, duration: 0.07, svgOrigin: "150 262", ease: "power2.in" }, t);
    all.forEach((m) => tl.set(`#${id}-m-${m}`, { opacity: m === mood ? 1 : 0 }, t + 0.07));
    tl.set(`#${id}-brows`, { opacity: mood === "smile" ? 0 : 1 }, t + 0.07);
    tl.to(`#${id}-b`, { scaleY: 1, scaleX: 1, duration: 0.35, svgOrigin: "150 262", ease: "elastic.out(1,0.45)" }, t + 0.07);
  },
  blink(tl, id, t) {
    tl.to(`#${id}-eyes`, { scaleY: 0.08, duration: 0.05, svgOrigin: "150 164" }, t);
    tl.to(`#${id}-eyes`, { scaleY: 1, duration: 0.08, svgOrigin: "150 164" }, t + 0.09);
  },
  look(tl, id, dx, dy, t) {
    tl.to(`#${id}-pup`, { x: dx, y: dy, duration: 0.15, ease: "power3.out" }, t);
  },
  idle(tl, id, t0, t1) {
    const n = Math.max(1, Math.floor((t1 - t0) / 1.1));
    tl.to(`#${id}-b`, { scaleY: 1.035, scaleX: 0.98, duration: 0.55, svgOrigin: "150 262", ease: "sine.inOut", yoyo: true, repeat: n * 2 - 1 }, t0);
  },
  wave(tl, id, t, times) {
    tl.to(`#${id}-ar`, { rotation: -35, duration: 0.14, svgOrigin: "260 222", ease: "sine.inOut", yoyo: true, repeat: times * 2 - 1 }, t);
  },
  sweat(tl, id, t) {
    tl.fromTo(`#${id}-sweat`, { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 0.2 }, t);
    tl.to(`#${id}-sweat`, { y: 40, opacity: 0, duration: 0.7, ease: "power2.in" }, t + 0.6);
  },
};
'''


def build_scenes():
    for f in sorted(SRC.glob("*.html")):
        s = f.read_text()
        s = re.sub(r"\{\{POPO (\w[\w-]*)\}\}", lambda m: popo(m.group(1)), s)
        s = s.replace("{{POPOJS}}", POPOJS)
        (OUT / f.name).write_text(s)
        print("built", f.name)


HIGHLIGHT = re.compile(r"^(seis|ciento|treinta|toneladas|doscientos|cincuenta|metros|cuarenta|mitad|villano|toallitas|sifón|gravedad|depuradora|bacterias|biogás|abono|río|Popo|váter|colector|rejas|kilómetros|Londres|Latinoamérica|olor)$", re.I)


def build_captions():
    lines = (ROOT.parent / "voz" / "guion.txt").read_text().strip().splitlines()
    times = json.loads((ROOT.parent / "voz" / "tiempos.json").read_text())
    groups = []
    for line, tm in zip(lines, times):
        words = line.split()
        # agrupar: máx 3 palabras, corta tras puntuación
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) == 3 or re.search(r"[.,:;]$", w):
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        total = sum(len(" ".join(c)) + 4 for c in chunks)
        t = tm["start"]
        for c in chunks:
            d = tm["dur"] * (len(" ".join(c)) + 4) / total
            groups.append((t, t + d, c))
            t += d
    html_groups, js = [], []
    for i, (a, b, c) in enumerate(groups):
        ws = []
        for w in c:
            clean = re.sub(r"[^\wáéíóúñÁÉÍÓÚÑ]", "", w)
            cls = ' class="hl"' if HIGHLIGHT.match(clean) else ""
            ws.append(f"<span{cls}>{w.upper()}</span>")
        html_groups.append(f'    <div id="cg-{i}" class="cg">{" ".join(ws)}</div>')
        js.append(f"[{a:.3f},{b:.3f}]")
    out = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #root .cg {{
      position: absolute; left: 0; right: 0; top: 1235px; padding: 0 90px;
      text-align: center; font-family: "Archivo Black", sans-serif; font-size: 78px; line-height: 1.05;
      color: #fff; -webkit-text-stroke: 16px #141414; paint-order: stroke fill; letter-spacing: -0.01em;
      opacity: 0; visibility: hidden; overflow: visible;
    }}
    #root .cg span {{ display: inline-block; }}
    #root .cg .hl {{ color: #FFD23F; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(html_groups)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const T = [{",".join(js)}];
    T.forEach(([a, b], i) => {{
      const g = `#cg-${{i}}`;
      tl.set(g, {{ visibility: "visible" }}, a);
      tl.fromTo(g, {{ opacity: 0, scale: 0.82, y: 18 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.16, ease: "back.out(2.2)" }}, a);
      tl.to(g, {{ opacity: 0, duration: 0.06, ease: "power2.in" }}, b - 0.06);
      tl.set(g, {{ visibility: "hidden" }}, b);
    }});
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
    (OUT / "captions.html").write_text(out)
    print("built captions.html", len(groups), "groups")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    build_scenes()
    build_captions()

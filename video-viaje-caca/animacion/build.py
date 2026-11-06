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


HIGHLIGHT = re.compile(r"^(seis|litros|ciento|treinta|toneladas|doscientos|cincuenta|metros|cuarenta|mitad|villano|toallitas|sifón|gravedad|depuradora|bacterias|biogás|abono|río|Popo|váter|colector|rejas|kilómetros|Londres|Latinoamérica|olor|bombas|montañas|heroínas|tratar|baño)$", re.I)

# inicio absoluto de cada escena (debe coincidir con index.html)
SCENES = {"hook": 0, "vater": 6.036, "red": 16.342, "villano": 28.41, "planta": 39.553, "climax": 58.205, "cta": 64.834}
# sacudidas de cámara en impactos (segundos absolutos)
SHAKES = [0.36, 4.12, 14.80, 29.02, 34.27, 42.62, 59.47, 64.95]


def lines_and_times():
    lines = (ROOT.parent / "voz" / "guion.txt").read_text().strip().splitlines()
    times = json.loads((ROOT.parent / "voz" / "tiempos.json").read_text())
    return lines, times


def punch_js(scene):
    """Golpe de cámara al inicio de cada frase y sacudida en cada impacto."""
    a = SCENES[scene]
    names = list(SCENES)
    b = SCENES[names[names.index(scene) + 1]] if scene != names[-1] else 70
    _, times = lines_and_times()
    js = []
    for tm in times:
        t = tm["start"] - a
        if 0.25 < t < b - a - 0.2:
            js.append(f'tl.fromTo("#{scene}-cam", {{ scale: 1.075 }}, {{ scale: 1, duration: 0.4, ease: "power3.out", immediateRender: false }}, {t:.3f});')
    for sh in SHAKES:
        t = sh - a
        if 0 <= t < b - a:
            js.append(f'tl.fromTo("#{scene}-cam", {{ x: -22, y: 12, rotation: -1.2 }}, {{ x: 0, y: 0, rotation: 0, duration: 0.45, ease: "elastic.out(1,0.3)", immediateRender: false }}, {t:.3f});')
    return "\n    ".join(js)


def wrap_scene(name, s):
    s, n1 = re.subn(r'(<div id="root"[^>]*>)', rf'\1<div id="{name}-cam" style="position:absolute;inset:0;transform-origin:540px 760px">', s, count=1)
    s, n2 = re.subn(r'\n  </div>\n  <script>', '</div>\n  </div>\n  <script>', s, count=1)
    assert n1 == n2 == 1, name
    s = s.replace(f'window.__timelines["{name}"] = tl;', "// cámara: golpes y sacudidas (generado)\n    " + punch_js(name) + f'\n    window.__timelines["{name}"] = tl;')
    return s


def build_scenes():
    for f in sorted(SRC.glob("*.html")):
        s = f.read_text()
        s = re.sub(r"\{\{POPO (\w[\w-]*)\}\}", lambda m: popo(m.group(1)), s)
        s = s.replace("{{POPOJS}}", POPOJS)
        if f.stem in SCENES:
            s = wrap_scene(f.stem, s)
        (OUT / f.name).write_text(s)
        print("built", f.name)


def build_captions():
    lines, times = lines_and_times()
    groups = []  # (start, end, [(word, t)])
    for line, tm in zip(lines, times):
        words = line.split()
        weights = [len(w) + (3 if re.search(r"[.,:;]$", w) else 1) for w in words]
        tot = sum(weights)
        wt, t = [], tm["start"]
        for w, k in zip(words, weights):
            wt.append((w, t)); t += tm["dur"] * k / tot
        chunks, cur = [], []
        for w in wt:
            cur.append(w)
            if len(cur) == 3 or re.search(r"[.,:;]$", w[0]):
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        for i, c in enumerate(chunks):
            end = chunks[i + 1][0][1] if i + 1 < len(chunks) else tm["start"] + tm["dur"] + 0.12
            groups.append((c[0][1] - 0.05, end, c))
    html, G, W = [], [], []
    for gi, (a, b, c) in enumerate(groups):
        spans = []
        for wi, (w, t) in enumerate(c):
            clean = re.sub(r"[^\wáéíóúñÁÉÍÓÚÑ]", "", w)
            hl = bool(HIGHLIGHT.match(clean))
            spans.append(f'<span id="cw-{gi}-{wi}"{" class=\"hl\"" if hl else ""}>{w.upper()}</span>')
            W.append(f'["#cw-{gi}-{wi}",{t:.3f},{1 if hl else 0}]')
        html.append(f'    <div id="cg-{gi}" class="cg">{" ".join(spans)}</div>')
        G.append(f"[{a:.3f},{b:.3f}]")
    out = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #root .cg {{
      position: absolute; left: 0; right: 0; top: 1225px; padding: 0 70px;
      text-align: center; font-family: "Archivo Black", sans-serif; font-size: 92px; line-height: 1.04;
      color: #fff; -webkit-text-stroke: 18px #141414; paint-order: stroke fill; letter-spacing: -0.01em;
      opacity: 0; visibility: hidden; overflow: visible;
    }}
    #root .cg span {{ display: inline-block; opacity: 0.0; }}
    #root .cg .hl {{ color: #FFD23F; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const G = [{",".join(G)}];
    const W = [{",".join(W)}];
    G.forEach(([a, b], i) => {{
      const g = `#cg-${{i}}`;
      tl.set(g, {{ visibility: "visible", opacity: 1 }}, a);
      tl.to(g, {{ opacity: 0, duration: 0.05 }}, b - 0.05);
      tl.set(g, {{ visibility: "hidden" }}, b);
    }});
    // palabra a palabra: aparece con rebote; la palabra activa se agranda
    W.forEach(([id, t, hl]) => {{
      tl.fromTo(id, {{ opacity: 0, scale: 0.5, y: 20 }}, {{ opacity: 1, scale: hl ? 1.18 : 1.08, y: 0, duration: 0.12, ease: "back.out(3)" }}, t);
      tl.to(id, {{ scale: hl ? 1.08 : 1, duration: 0.2, ease: "power2.out" }}, t + 0.18);
    }});
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
    (OUT / "captions.html").write_text(out)
    print("built captions.html", len(groups), "groups,", len(W), "words")


# ---------- efectos de sonido (tiempo absoluto del evento, archivo, inicio del golpe, volumen) ----------
SFX = [
    (0.35, "s02", 0.067, 1.0), (0.50, "s03", 0.314, 0.9), (4.10, "s11", 0.028, 0.8), (5.73, "s07", 0.254, 0.8),
    (6.04, "s16", 0.067, 0.6), (6.39, "s04", 0.023, 0.7), (6.66, "s04", 0.023, 0.7), (6.93, "s04", 0.023, 0.7),
    (7.20, "s04", 0.023, 0.7), (7.47, "s04", 0.023, 0.7), (7.74, "s04", 0.023, 0.7), (8.84, "s06", 0.196, 0.8),
    (10.4, "s14", 0.511, 0.6), (14.80, "s08", 0.03, 1.0), (15.99, "s01", 0.231, 0.8),
    (17.4, "s06", 0.196, 0.6), (19.89, "s04", 0.023, 0.8), (21.2, "s05", 0.407, 0.6), (24.86, "s07", 0.254, 0.8), (26.74, "s04", 0.023, 0.8),
    (29.01, "s12", 0.605, 0.8), (29.02, "s08", 0.03, 0.9), (31.9, "s16", 0.067, 0.4), (34.27, "s08", 0.03, 0.9), (34.46, "s01", 0.231, 0.8),
    (36.0, "s06", 0.196, 0.6), (37.51, "s17", 0.025, 0.7), (39.0, "s06", 0.196, 0.6),
    (40.65, "s17", 0.025, 0.6), (42.62, "s09", 0.206, 0.7), (43.35, "s11", 0.028, 0.7), (43.9, "s11", 0.028, 0.7), (44.45, "s11", 0.028, 0.7),
    (45.10, "s04", 0.023, 0.8), (45.93, "s07", 0.254, 0.8), (46.2, "s05", 0.407, 0.5),
    (50.45, "s13", 0.381, 0.8), (51.9, "s13", 0.381, 0.7), (53.2, "s13", 0.381, 0.7),
    (54.55, "s04", 0.023, 0.8), (55.15, "s04", 0.023, 0.8), (56.15, "s04", 0.023, 0.8),
    (58.3, "s17", 0.025, 0.6), (59.47, "s10", 0.104, 1.0), (62.8, "s15", 0.023, 0.8),
    (64.83, "s07", 0.254, 0.8), (65.13, "s04", 0.023, 0.8), (65.25, "s05", 0.407, 0.5), (66.83, "s17", 0.025, 0.7), (68.03, "s04", 0.023, 0.8),
]
TRIM = {"s18": 1.3}


def sfx_len(f):
    import subprocess
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ROOT / "assets/sfx" / f"{f}.mp3")], capture_output=True, text=True).stdout
    return float(out) - 0.02


def build_index():
    idx = ROOT / "index.html"
    s = idx.read_text()
    s = re.sub(r"\n      <!-- SFX:BEGIN -->.*<!-- SFX:END -->", "", s, flags=re.S)
    rows = []
    for i, (t, f, onset, vol) in enumerate(SFX):
        start = max(0.0, t - onset + 0.033)
        d = TRIM.get(f) or sfx_len(f)
        track = 5 + i % 4
        rows.append(f'      <audio id="fx{i:02d}" class="clip" src="assets/sfx/{f}.mp3" data-start="{start:.3f}" data-duration="{d:.3f}" data-track-index="{track}" data-volume="{vol}"></audio>')
    block = "\n      <!-- SFX:BEGIN -->\n" + "\n".join(rows) + "\n      <!-- SFX:END -->"
    s = s.replace('\n    </div>\n    <script>', block + '\n    </div>\n    <script>', 1)
    idx.write_text(s)
    print("index: sfx", len(rows))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    build_scenes()
    build_captions()
    build_index()

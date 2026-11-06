#!/usr/bin/env python3
"""Genera el proyecto HyperFrames del vídeo «Por qué no te levantas temprano»."""
import json, os, re, random, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SFX = "/root/.claude/skills/media-use/audio/assets/sfx"
os.makedirs(f"{ROOT}/compositions", exist_ok=True)
os.makedirs(f"{ROOT}/assets/sfx", exist_ok=True)

T = json.load(open(f"{ROOT}/assets/timings.json"))
L = {o["i"]: (o["start"], o["end"]) for o in T}
LINES = [l.strip() for l in open(f"{ROOT}/guion.txt", encoding="utf-8") if l.strip()]
TOTAL = round(L[15][1] + 1.6, 2)

# ---------- escenas: cada una arranca justo antes de su frase ----------
def cut(i): return round(L[i][0] - 0.1, 3)
SC = {
    "s1": (0.0, cut(2)), "s2": (cut(2), cut(3)), "s3": (cut(3), cut(5)), "s4": (cut(5), cut(7)),
    "s5": (cut(7), cut(9)), "s6": (cut(9), cut(13)), "s7": (cut(13), cut(14)),
    "s8": (cut(14), cut(15)), "s9": (cut(15), TOTAL),
}

def loc(scene, abs_t):
    return round(abs_t - SC[scene][0], 3)

def word_time(line_i, word_idx):
    """Tiempo absoluto aproximado de la palabra word_idx dentro de la frase."""
    s, e = L[line_i]
    words = LINES[line_i - 1].split()
    w = [len(x) + 2 for x in words]
    return round(s + (e - s) * sum(w[:word_idx]) / sum(w), 3)

# ---------- personaje: Leo ----------
def leo(cls, mood="tired"):
    show = lambda m: "1" if m == mood else "0"
    return f'''<svg class="leo {cls}" viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">
  <g class="leo-body">
    <path d="M70 500 Q70 340 200 340 Q330 340 330 500Z" fill="#4C6FFF"/>
    <path d="M70 500 Q70 340 200 340 Q330 340 330 500Z" fill="none" stroke="#2A3FB0" stroke-width="8"/>
    <path d="M165 345 L200 392 L235 345" fill="none" stroke="#2A3FB0" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="150" cy="430" r="9" fill="#FFD23F"/><circle cx="255" cy="455" r="9" fill="#FFD23F"/><circle cx="110" cy="480" r="7" fill="#FFD23F"/>
  </g>
  <rect x="172" y="300" width="56" height="50" rx="14" fill="#E3AE86"/>
  <g class="leo-head">
    <circle cx="82" cy="215" r="24" fill="#F0BE96"/><circle cx="318" cy="215" r="24" fill="#F0BE96"/>
    <circle cx="200" cy="200" r="122" fill="#F6CCA6" stroke="#2B1B12" stroke-width="7"/>
    <path class="leo-hair" d="M80 190 Q78 70 200 64 Q322 70 320 190 Q300 128 248 136 Q226 104 186 132 Q140 112 118 150 Q96 160 80 190Z" fill="#2E2018"/>
    <circle cx="130" cy="262" r="20" fill="#FF8C8C" opacity=".35"/><circle cx="270" cy="262" r="20" fill="#FF8C8C" opacity=".35"/>
    <path class="bags" d="M132 238 Q155 250 178 238 M222 238 Q245 250 268 238" stroke="#B9806A" stroke-width="5" fill="none" stroke-linecap="round" opacity="{show('tired')}"/>
    <path class="brow-l" d="M128 168 Q152 158 178 168" stroke="#2E2018" stroke-width="9" fill="none" stroke-linecap="round"/>
    <path class="brow-r" d="M222 168 Q248 158 272 168" stroke="#2E2018" stroke-width="9" fill="none" stroke-linecap="round"/>
    <g class="eyes">
      <ellipse class="eye eye-l" cx="155" cy="212" rx="15" ry="19" fill="#1B1B1B"/>
      <ellipse class="eye eye-r" cx="245" cy="212" rx="15" ry="19" fill="#1B1B1B"/>
      <circle cx="160" cy="205" r="5" fill="#fff"/><circle cx="250" cy="205" r="5" fill="#fff"/>
    </g>
    <path class="m m-sad" d="M168 288 Q200 266 232 288" stroke="#2B1B12" stroke-width="8" fill="none" stroke-linecap="round" opacity="{show('tired')}"/>
    <path class="m m-smile" d="M160 270 Q200 318 240 270 Z" fill="#7A2E2E" stroke="#2B1B12" stroke-width="7" stroke-linejoin="round" opacity="{show('happy')}"/>
    <ellipse class="m m-o" cx="200" cy="284" rx="18" ry="22" fill="#7A2E2E" stroke="#2B1B12" stroke-width="7" opacity="{show('shock')}"/>
    <path class="m m-flat" d="M175 282 L225 282" stroke="#2B1B12" stroke-width="8" stroke-linecap="round" opacity="{show('flat')}"/>
  </g>
</svg>'''

def alarm_clock(cls, txt="6:00"):
    return f'''<svg class="{cls}" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
  <g class="bells"><circle cx="70" cy="70" r="42" fill="#FF4D5A" stroke="#1B1B1B" stroke-width="8"/><circle cx="230" cy="70" r="42" fill="#FF4D5A" stroke="#1B1B1B" stroke-width="8"/></g>
  <path d="M80 250 L55 290 M220 250 L245 290" stroke="#1B1B1B" stroke-width="14" stroke-linecap="round"/>
  <circle cx="150" cy="165" r="118" fill="#FF4D5A" stroke="#1B1B1B" stroke-width="10"/>
  <circle cx="150" cy="165" r="92" fill="#FFF6E5" stroke="#1B1B1B" stroke-width="6"/>
  <text x="150" y="190" text-anchor="middle" font-family="Archivo Black" font-size="66" fill="#1B1B1B">{txt}</text>
</svg>'''

def phone_svg(cls, body):
    return f'''<svg class="{cls}" viewBox="0 0 320 560" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="6" width="308" height="548" rx="44" fill="#14161F" stroke="#000" stroke-width="10"/>
  <rect x="24" y="30" width="272" height="500" rx="28" fill="#232842"/>
  <rect x="120" y="42" width="80" height="16" rx="8" fill="#0B0C12"/>
  {body}
</svg>'''

# ---------- plantilla de escena ----------
def scene(sid, dur, css, html, js):
    return f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .{sid} {{ position: absolute; inset: 0; font-family: "Archivo Black", sans-serif; color: #fff; }}
    .{sid} svg {{ overflow: visible; }}
    .{sid} .leo .eye, .{sid} .leo .leo-head, .{sid} .leo .m {{ transform-box: fill-box; transform-origin: center; }}
    .{sid} .tag {{ position: absolute; left: 50%; top: 210px; transform: translateX(-50%); padding: 18px 46px; border-radius: 999px; font-size: 64px; letter-spacing: 2px; border: 7px solid #1B1B1B; box-shadow: 0 10px 0 #1B1B1B; white-space: nowrap; }}
    .{sid} .tag.red {{ background: #FF4D5A; color: #fff; }}
    .{sid} .tag.yellow {{ background: #FFD23F; color: #1B1B1B; }}
    .{sid} .tag.green {{ background: #3DDC97; color: #1B1B1B; }}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-layout-allow-overlap data-layout-allow-overflow>
    <div class="{sid}">
{html}
    </div>
  </div>
  <script>
    (function () {{
      const S = ".{sid} ";
      const tl = gsap.timeline({{ paused: true }});
{js}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
'''

def blink(sel, times):
    return "\n".join(
        f'      tl.fromTo(S + "{sel} .eye", {{ scaleY: 1 }}, {{ scaleY: 0.1, duration: 0.07, yoyo: true, repeat: 1, ease: "power1.inOut" }}, {t});'
        for t in times)

def mood(sel, to, at, frm=None):
    """Cambia la boca con una mini toma (anticipación + asentado)."""
    js = f'      tl.to(S + "{sel} .m", {{ opacity: 0, duration: 0.08 }}, {at});\n'
    js += f'      tl.fromTo(S + "{sel} .m-{to}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }}, {at + 0.06});\n'
    js += f'      tl.fromTo(S + "{sel} .leo-head", {{ scaleY: 1, scaleX: 1 }}, {{ scaleY: 0.93, scaleX: 1.05, duration: 0.08, yoyo: true, repeat: 1, ease: "power2.out" }}, {at});'
    return js

def breathe(sel, dur):
    n = max(1, int(dur / 1.6))
    return f'      tl.fromTo(S + "{sel} .leo-body", {{ scaleY: 1, transformOrigin: "50% 100%" }}, {{ scaleY: 1.025, duration: 0.8, yoyo: true, repeat: {n * 2 - 1}, ease: "sine.inOut" }}, 0);'

files = {}

# ======================= S1 · gancho =======================
sid = "s1"; d = SC[sid][1] - SC[sid][0]
t_noche = loc(sid, word_time(1, 6))  # «Es la noche anterior»
files[sid] = scene(sid, d, f'''
    .s1 .title {{ position: absolute; left: 60px; right: 60px; top: 230px; text-align: center; line-height: 1.02; }}
    .s1 .title .sm {{ display:block; font-size: 70px; color: #fff; -webkit-text-stroke: 14px #1B1B1B; paint-order: stroke fill; }}
    .s1 .title .big {{ display:block; font-size: 118px; color: #FFD23F; -webkit-text-stroke: 18px #1B1B1B; paint-order: stroke fill; }}
    .s1 .t-b {{ opacity: 0; }}
    .s1 .t-b .big {{ color: #8FA8FF; }}
    .s1 .clock {{ position: absolute; left: 330px; top: 560px; width: 420px; height: 420px; }}
    .s1 .bed {{ position: absolute; left: 90px; top: 880px; width: 900px; height: 380px; }}
    .s1 .zzz {{ position: absolute; left: 760px; top: 860px; font-size: 64px; color: #8FA8FF; -webkit-text-stroke: 10px #1B1B1B; paint-order: stroke fill; }}
    .s1 .moon {{ position: absolute; left: 820px; top: 520px; width: 150px; height: 150px; opacity: 0; }}
''', f'''
      <div class="title t-a"><span class="sm">TU PROBLEMA</span><span class="big">NO ES LA MAÑANA</span></div>
      <div class="title t-b"><span class="sm">ES LA</span><span class="big">NOCHE ANTERIOR</span></div>
      <svg class="moon" viewBox="0 0 100 100"><path d="M70 10 A42 42 0 1 0 90 72 A34 34 0 1 1 70 10Z" fill="#FFE9A8" stroke="#1B1B1B" stroke-width="5"/></svg>
      {alarm_clock("clock")}
      <svg class="bed" viewBox="0 0 900 380" xmlns="http://www.w3.org/2000/svg">
        <rect x="20" y="40" width="40" height="320" rx="14" fill="#7A4B2A" stroke="#1B1B1B" stroke-width="8"/>
        <rect x="30" y="250" width="840" height="70" rx="20" fill="#9A6236" stroke="#1B1B1B" stroke-width="8"/>
        <g class="lump">
          <path d="M60 255 Q80 130 260 140 Q360 80 520 120 Q760 120 860 255Z" fill="#4C6FFF" stroke="#1B1B1B" stroke-width="8"/>
          <path d="M260 160 Q420 180 560 150 M600 170 Q720 190 820 230" stroke="#2A3FB0" stroke-width="7" fill="none" stroke-linecap="round"/>
          <path d="M70 150 Q60 90 130 80 Q190 70 210 130 Q170 120 140 140 Q110 130 70 150Z" fill="#2E2018" stroke="#1B1B1B" stroke-width="6"/>
          <rect x="60" y="120" width="190" height="80" rx="38" fill="#F4F1EA" stroke="#1B1B1B" stroke-width="8" transform="rotate(-8 155 160)"/>
        </g>
      </svg>
      <div class="zzz">Z<span style="font-size:44px">z</span></div>
''', f'''
      tl.fromTo(S + ".clock", {{ rotation: -9 }}, {{ rotation: 9, duration: 0.06, yoyo: true, repeat: 23, ease: "none", transformOrigin: "50% 60%" }}, 0);
      tl.fromTo(S + ".clock", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.18, yoyo: true, repeat: 7, ease: "sine.inOut", transformOrigin: "50% 60%" }}, 0);
      tl.fromTo(S + ".lump", {{ y: 0 }}, {{ y: -10, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 0.2);
      tl.fromTo(S + ".lump", {{ scaleX: 1 }}, {{ scaleX: 1.03, duration: 0.14, yoyo: true, repeat: 1, transformOrigin: "10% 100%" }}, 0.9);
      tl.fromTo(S + ".zzz", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: -40, duration: 1.2, ease: "power1.out" }}, 0.3);
      tl.to(S + ".zzz", {{ opacity: 0, duration: 0.3 }}, 1.5);
      tl.fromTo(S + ".t-a .big", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out" }}, 0.25);
      tl.to(S + ".t-a", {{ y: -60, opacity: 0, duration: 0.18, ease: "power3.in" }}, {t_noche - 0.18});
      tl.fromTo(S + ".t-b", {{ y: 80, opacity: 0, scale: 0.9 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.32, ease: "back.out(2.2)" }}, {t_noche});
      tl.to(S + ".clock", {{ x: -140, y: 40, scale: 0.78, duration: 0.4, ease: "power3.inOut" }}, {t_noche});
      tl.fromTo(S + ".moon", {{ opacity: 0, scale: 0.4, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }}, {t_noche + 0.1});
''')

# ======================= S2 · Leo y sus 5 alarmas =======================
sid = "s2"; d = SC[sid][1] - SC[sid][0]
t_cinco = loc(sid, word_time(2, 3)); t_ning = loc(sid, word_time(2, 5))
rows = ""
for k, h in enumerate(["6:00", "6:05", "6:10", "6:15", "6:20"]):
    y = 100 + k * 84
    rows += f'''<g class="row row{k}"><rect x="40" y="{y}" width="240" height="68" rx="16" fill="#323A60"/>
      <text x="62" y="{y+48}" font-family="Archivo Black" font-size="38" fill="#fff">{h}</text>
      <rect x="196" y="{y+20}" width="64" height="30" rx="15" fill="#3DDC97"/><circle class="knob" cx="245" cy="{y+35}" r="12" fill="#fff"/>
      <line class="strike" x1="50" y1="{y+34}" x2="270" y2="{y+34}" stroke="#FF4D5A" stroke-width="10" stroke-linecap="round"/></g>'''
js = f'''
      tl.fromTo(S + ".leo", {{ y: 500, scaleY: 0.8 }}, {{ y: 0, scaleY: 1, duration: 0.45, ease: "back.out(1.8)", transformOrigin: "50% 100%" }}, 0.05);
      tl.fromTo(S + ".name", {{ scale: 0, rotation: -12 }}, {{ scale: 1, rotation: -6, duration: 0.35, ease: "back.out(3)" }}, 0.35);
{breathe(".leo", d)}
{blink(".leo", [1.1, 2.4])}
      tl.fromTo(S + ".phone", {{ x: 500, rotation: 20 }}, {{ x: 0, rotation: 6, duration: 0.4, ease: "power3.out" }}, {t_cinco - 0.35});
'''
for k in range(5):
    js += f'      tl.fromTo(S + ".row{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.16, ease: "power2.out" }}, {t_cinco + k * 0.09:.3f});\n'
    js += f'      tl.fromTo(S + ".row{k} .strike", {{ drawSVG: 0, scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.12, ease: "power2.out" }}, {t_ning + k * 0.08:.3f});\n'
    js += f'      tl.to(S + ".row{k} rect:nth-child(3)", {{ fill: "#6B6F85", duration: 0.1 }}, {t_ning + k * 0.08:.3f});\n'
    js += f'      tl.to(S + ".row{k} .knob", {{ x: -34, duration: 0.1 }}, {t_ning + k * 0.08:.3f});\n'
js += f'''      tl.fromTo(S + ".phone", {{ x: 0 }}, {{ x: 14, duration: 0.05, yoyo: true, repeat: 5 }}, {t_ning + 0.4});
{mood(".leo", "flat", t_ning + 0.2)}
      tl.fromTo(S + ".leo .leo-head", {{ rotation: 0 }}, {{ rotation: -8, duration: 0.4, ease: "power2.out" }}, {t_ning + 0.3});
'''
js = js.replace("drawSVG: 0, ", "")
files[sid] = scene(sid, d, '''
    .s2 .leo { position: absolute; left: 30px; top: 470px; width: 560px; height: 700px; }
    .s2 .name { position: absolute; left: 110px; top: 300px; padding: 14px 40px; background: #FFD23F; color: #1B1B1B; font-size: 80px; border: 7px solid #1B1B1B; border-radius: 26px; box-shadow: 0 10px 0 #1B1B1B; }
    .s2 .phone { position: absolute; left: 610px; top: 440px; width: 400px; height: 700px; }
    .s2 .strike { transform: scaleX(0); }
''', f'''
      <div class="name">LEO</div>
      {leo("leo", "tired")}
      {phone_svg("phone", rows)}
''', js)

# ======================= S3 · Error 1: móvil + melatonina =======================
sid = "s3"; d = SC[sid][1] - SC[sid][0]
t4 = loc(sid, L[4][0])
t_mel = loc(sid, word_time(4, 6))
files[sid] = scene(sid, d, '''
    .s3 .room { position: absolute; inset: 0; background: radial-gradient(circle at 50% 46%, rgba(80,140,255,.0) 0%, rgba(5,8,25,.55) 65%); }
    .s3 .glow { position: absolute; left: 140px; top: 380px; width: 800px; height: 800px; border-radius: 50%; background: radial-gradient(circle, rgba(90,170,255,.75) 0%, rgba(90,170,255,.0) 65%); }
    .s3 .leo { position: absolute; left: 280px; top: 400px; width: 520px; height: 650px; }
    .s3 .phone { position: absolute; left: 430px; top: 850px; width: 220px; height: 380px; }
    .s3 .clockd { position: absolute; left: 700px; top: 400px; padding: 10px 26px; background: #0B0C12; border: 6px solid #FF4D5A; border-radius: 20px; font-family: "Archivo Black"; font-size: 70px; color: #FF4D5A; }
    .s3 .meter { position: absolute; left: 140px; top: 400px; width: 800px; opacity: 0; }
    .s3 .meter .lbl { font-size: 54px; text-align: center; -webkit-text-stroke: 10px #1B1B1B; paint-order: stroke fill; }
    .s3 .meter .bar { margin-top: 14px; height: 76px; border: 8px solid #1B1B1B; border-radius: 40px; background: #232842; overflow: hidden; box-shadow: 0 8px 0 #1B1B1B; }
    .s3 .meter .fill { width: 100%; height: 100%; background: linear-gradient(90deg,#8FA8FF,#B79CFF); transform-origin: 0% 50%; }
    .s3 .rays { position: absolute; left: 290px; top: 700px; width: 500px; height: 420px; opacity: 0; }
''', f'''
      <div class="glow"></div>
      <div class="room"></div>
      <svg class="rays" viewBox="0 0 500 420"><g stroke="#5AB0FF" stroke-width="16" stroke-linecap="round"><line x1="250" y1="400" x2="60" y2="40"/><line x1="250" y1="400" x2="250" y2="10"/><line x1="250" y1="400" x2="440" y2="40"/><line x1="250" y1="400" x2="150" y2="20"/><line x1="250" y1="400" x2="350" y2="20"/></g></svg>
      {leo("leo", "shock")}
      {phone_svg("phone", '<rect x="24" y="30" width="272" height="500" rx="28" fill="#6FC3FF"/><rect x="50" y="90" width="220" height="140" rx="18" fill="#fff" opacity=".85"/><rect x="50" y="250" width="220" height="40" rx="12" fill="#fff" opacity=".7"/><rect x="50" y="305" width="160" height="40" rx="12" fill="#fff" opacity=".7"/><rect x="50" y="360" width="200" height="140" rx="18" fill="#fff" opacity=".85"/>')}
      <div class="tag red">ERROR 1</div>
      <div class="clockd"><span class="cd">12:41</span></div>
      <div class="meter"><div class="lbl">MELATONINA</div><div class="bar"><div class="fill"></div></div></div>
''', f'''
      tl.fromTo(S + ".tag", {{ scale: 2.2, opacity: 0, rotation: -8 }}, {{ scale: 1, opacity: 1, rotation: -3, duration: 0.3, ease: "back.out(2.5)" }}, 0.03);
      tl.fromTo(S + ".leo", {{ y: 120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 0.05);
      tl.fromTo(S + ".phone", {{ y: 300, rotation: -10 }}, {{ y: 0, rotation: 0, duration: 0.4, ease: "back.out(1.6)" }}, 0.15);
      tl.fromTo(S + ".glow", {{ opacity: 0.4, scale: 0.9 }}, {{ opacity: 1, scale: 1.05, duration: 0.5, yoyo: true, repeat: 11, ease: "sine.inOut" }}, 0);
      tl.fromTo(S + ".leo .eye", {{ scale: 1 }}, {{ scale: 1.25, duration: 0.3, ease: "back.out(3)" }}, 0.4);
      tl.fromTo(S + ".clockd", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, 0.5);
      const cd = {{ m: 41 }};
      tl.to(cd, {{ m: 67, duration: 1.6, ease: "power2.in", onUpdate: () => {{
        const m = Math.round(cd.m); const h = m >= 60 ? 1 : 12; const mm = m % 60;
        document.querySelector(S + ".cd").textContent = h + ":" + String(mm).padStart(2, "0");
      }} }}, 0.6);
      tl.fromTo(S + ".clockd", {{ x: 0 }}, {{ x: 10, duration: 0.05, yoyo: true, repeat: 5 }}, 2.2);
      // línea 4: la luz frena la melatonina
      tl.to(S + ".tag, " + S + ".clockd", {{ y: -40, opacity: 0, duration: 0.25, ease: "power2.in" }}, {t4 - 0.1});
      tl.fromTo(S + ".meter", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, {t4 + 0.05});
      tl.fromTo(S + ".rays", {{ opacity: 0, scale: 0.5, transformOrigin: "50% 100%" }}, {{ opacity: 0.9, scale: 1, duration: 0.35, ease: "power3.out" }}, {t_mel - 0.4});
      tl.fromTo(S + ".rays", {{ opacity: 0.9 }}, {{ opacity: 0.5, duration: 0.2, yoyo: true, repeat: 9 }}, {t_mel});
      tl.fromTo(S + ".meter .fill", {{ scaleX: 0.92 }}, {{ scaleX: 0.14, duration: 1.6, ease: "power2.inOut" }}, {t_mel - 0.2});
      tl.to(S + ".meter .fill", {{ background: "linear-gradient(90deg,#FF4D5A,#FF8A65)", duration: 0.6 }}, {t_mel + 0.6});
{blink(".leo", [1.6, 3.1])}
''')

# ======================= S4 · Error 2: horarios =======================
sid = "s4"; d = SC[sid][1] - SC[sid][0]
t6 = loc(sid, L[6][0])
days = [("L", "6:00"), ("M", "9:30"), ("X", "7:15"), ("J", "11:00"), ("V", "6:45"), ("S", "12:30"), ("D", "10:00")]
cards = ""
for k, (dname, h) in enumerate(days):
    col, rowi = k % 4, k // 4
    x = 70 + col * 240 + (120 if rowi else 0); y = 430 + rowi * 300
    cards += f'<div class="day day{k}" style="left:{x}px;top:{y}px"><div class="dn">{dname}</div><div class="hh">{h}</div></div>\n'
js = '''      tl.fromTo(S + ".tag", { scale: 2.2, opacity: 0, rotation: 8 }, { scale: 1, opacity: 1, rotation: 3, duration: 0.3, ease: "back.out(2.5)" }, 0.03);
'''
for k in range(7):
    js += f'      tl.fromTo(S + ".day{k}", {{ scale: 0, rotation: {random.Random(k).choice([-14,-8,8,14])} }}, {{ scale: 1, rotation: {random.Random(k+9).choice([-6,-3,3,6])}, duration: 0.28, ease: "back.out(2.6)" }}, {0.35 + k * 0.27:.2f});\n'
js += f'''      tl.to(S + ".day", {{ y: -900, opacity: 0, duration: 0.35, stagger: 0.03, ease: "power3.in" }}, {t6 - 0.3});
      tl.to(S + ".tag", {{ opacity: 0, duration: 0.2 }}, {t6 - 0.2});
      tl.fromTo(S + ".leo", {{ y: 1300 }}, {{ y: 0, duration: 0.4, ease: "back.out(1.5)" }}, {t6 - 0.05});
      tl.fromTo(S + ".bubble", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.4)", transformOrigin: "20% 100%" }}, {t6 + 0.3});
      tl.fromTo(S + ".hand-m", {{ rotation: 0 }}, {{ rotation: 1440, duration: 2.4, ease: "power1.inOut", svgOrigin: "150 150" }}, {t6 + 0.4});
      tl.fromTo(S + ".hand-h", {{ rotation: 0 }}, {{ rotation: -720, duration: 2.4, ease: "power1.inOut", svgOrigin: "150 150" }}, {t6 + 0.4});
      tl.fromTo(S + ".q", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, stagger: 0.25, ease: "back.out(3)" }}, {t6 + 0.8});
      tl.fromTo(S + ".leo .leo-head", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.35, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {t6 + 0.4});
{blink(".leo", [t6 + 1.2, t6 + 2.4])}
{mood(".leo", "o", t6 + 0.6)}
'''
files[sid] = scene(sid, d, '''
    .s4 .day { position: absolute; width: 210px; height: 250px; background: #FFF6E5; border: 8px solid #1B1B1B; border-radius: 28px; box-shadow: 0 10px 0 #1B1B1B; color: #1B1B1B; text-align: center; overflow: hidden; }
    .s4 .day .dn { background: #FF4D5A; color: #fff; font-size: 54px; padding: 10px 0; border-bottom: 8px solid #1B1B1B; }
    .s4 .day .hh { font-size: 52px; margin-top: 40px; }
    .s4 .leo { position: absolute; left: 60px; top: 700px; width: 520px; height: 650px; }
    .s4 .bubble { position: absolute; left: 460px; top: 330px; width: 560px; height: 560px; }
    .s4 .q { position: absolute; font-size: 110px; color: #FFD23F; -webkit-text-stroke: 14px #1B1B1B; paint-order: stroke fill; }
''', f'''
      <div class="tag red">ERROR 2</div>
      {cards}
      {leo("leo", "tired")}
      <svg class="bubble" viewBox="0 0 300 300">
        <circle cx="40" cy="290" r="12" fill="#fff" stroke="#1B1B1B" stroke-width="5"/><circle cx="70" cy="255" r="18" fill="#fff" stroke="#1B1B1B" stroke-width="5"/>
        <circle cx="160" cy="140" r="122" fill="#fff" stroke="#1B1B1B" stroke-width="7"/>
        <g transform="translate(10 -10)"><circle cx="150" cy="150" r="88" fill="#FFF6E5" stroke="#1B1B1B" stroke-width="8"/>
        <line class="hand-h" x1="150" y1="150" x2="150" y2="105" stroke="#1B1B1B" stroke-width="12" stroke-linecap="round"/>
        <line class="hand-m" x1="150" y1="150" x2="150" y2="80" stroke="#FF4D5A" stroke-width="8" stroke-linecap="round"/>
        <circle cx="150" cy="150" r="10" fill="#1B1B1B"/></g>
      </svg>
      <div class="q" style="left:900px;top:300px">?</div><div class="q" style="left:420px;top:330px">?</div><div class="q" style="left:960px;top:820px">?</div>
''', js.replace('"o"', '"o"'))
files[sid] = files[sid].replace('.m-o"', '.m-o"')

# ======================= S5 · Error 3: posponer =======================
sid = "s5"; d = SC[sid][1] - SC[sid][0]
t8 = loc(sid, L[8][0])
presses = [0.55, 1.05, 1.5, 1.9]
js = '''      tl.fromTo(S + ".tag", { scale: 2.2, opacity: 0, rotation: -8 }, { scale: 1, opacity: 1, rotation: -3, duration: 0.3, ease: "back.out(2.5)" }, 0.03);
      tl.set(S + ".hand", { y: -800 }, 0);
      tl.fromTo(S + ".btn", { scale: 0, rotation: -10 }, { scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }, 0.1);
'''
for p in presses:
    js += f'''      tl.fromTo(S + ".hand", {{ y: -800 }}, {{ y: 0, duration: 0.14, ease: "power3.in", immediateRender: false }}, {p - 0.14});
      tl.fromTo(S + ".btn-top", {{ y: 0 }}, {{ y: 34, duration: 0.07, yoyo: true, repeat: 1, ease: "power2.out" }}, {p});
      tl.to(S + ".hand", {{ y: -800, duration: 0.2, ease: "power2.out" }}, {p + 0.12});
      tl.fromTo(S + ".plus5", {{ opacity: 0, y: 0, scale: 0.6 }}, {{ opacity: 1, y: -120, scale: 1, duration: 0.35, ease: "power2.out" }}, {p});
      tl.to(S + ".plus5", {{ opacity: 0, duration: 0.15 }}, {p + 0.32});
'''
js += f'''      tl.to(S + ".hand", {{ opacity: 0, duration: 0.2 }}, {t8 - 0.2});
      tl.to(S + ".btnwrap, " + S + ".tag", {{ y: -60, opacity: 0, duration: 0.25, ease: "power2.in" }}, {t8 - 0.2});
      tl.fromTo(S + ".sleep", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, {t8});
      tl.fromTo(S + ".seg", {{ x: 0, y: 0, rotation: 0 }}, {{ x: (i) => [-60,-20,25,70][i], y: (i) => [40,-30,50,-20][i], rotation: (i) => [-14,9,-7,16][i], duration: 0.35, ease: "back.out(2)", stagger: 0.06 }}, {t8 + 0.6});
      tl.to(S + ".seg", {{ backgroundColor: "#FF4D5A", duration: 0.2, stagger: 0.06 }}, {t8 + 0.6});
      tl.fromTo(S + ".nodesc", {{ scale: 0, rotation: -12 }}, {{ scale: 1, rotation: -5, duration: 0.35, ease: "back.out(3)" }}, {t8 + 0.9});
'''
files[sid] = scene(sid, d, '''
    .s5 .btnwrap { position: absolute; left: 190px; top: 560px; width: 700px; height: 560px; }
    .s5 .btn { position: absolute; inset: 0; }
    .s5 .hand { position: absolute; left: 430px; top: 420px; width: 220px; height: 300px; }
    .s5 .plus5 { position: absolute; left: 760px; top: 520px; font-size: 80px; color: #FFD23F; -webkit-text-stroke: 12px #1B1B1B; paint-order: stroke fill; opacity: 0; }
    .s5 .sleep { position: absolute; left: 90px; top: 520px; width: 900px; text-align: center; opacity: 0; }
    .s5 .sleep .lbl { font-size: 62px; -webkit-text-stroke: 10px #1B1B1B; paint-order: stroke fill; color: #8FA8FF; }
    .s5 .segs { display: flex; gap: 0; margin-top: 30px; height: 120px; }
    .s5 .seg { flex: 1; background: #8FA8FF; border: 8px solid #1B1B1B; display:flex; align-items:center; justify-content:center; font-size: 56px; color: #1B1B1B; }
    .s5 .seg:first-child { border-radius: 60px 0 0 60px; } .s5 .seg:last-child { border-radius: 0 60px 60px 0; }
    .s5 .nodesc { display: inline-block; margin-top: 110px; padding: 18px 40px; background: #FFF6E5; color: #FF4D5A; border: 8px solid #1B1B1B; border-radius: 24px; font-size: 70px; box-shadow: 0 10px 0 #1B1B1B; }
''', '''
      <div class="tag red">ERROR 3</div>
      <div class="btnwrap"><svg class="btn" viewBox="0 0 700 560">
        <ellipse cx="350" cy="430" rx="320" ry="110" fill="#7A1F2A" stroke="#1B1B1B" stroke-width="10"/>
        <rect x="30" y="330" width="640" height="100" fill="#7A1F2A"/><ellipse cx="350" cy="330" rx="320" ry="110" fill="#B02A38" stroke="#1B1B1B" stroke-width="10"/>
        <g class="btn-top"><rect x="100" y="230" width="500" height="90" fill="#E8394A"/><ellipse cx="350" cy="320" rx="250" ry="80" fill="#E8394A" stroke="#1B1B1B" stroke-width="10"/><ellipse cx="350" cy="230" rx="250" ry="80" fill="#FF4D5A" stroke="#1B1B1B" stroke-width="10"/>
        <line x1="100" y1="230" x2="100" y2="320" stroke="#1B1B1B" stroke-width="10"/><line x1="600" y1="230" x2="600" y2="320" stroke="#1B1B1B" stroke-width="10"/>
        <text x="350" y="252" text-anchor="middle" font-family="Archivo Black" font-size="64" fill="#fff" stroke="#1B1B1B" stroke-width="10" paint-order="stroke">POSPONER</text></g>
      </svg></div>
      <svg class="hand" viewBox="0 0 220 300"><path d="M70 0 L70 150 Q40 150 40 190 L40 240 Q40 290 110 290 Q180 290 180 240 L180 170 Q180 140 150 140 L150 0Z" fill="#F6CCA6" stroke="#1B1B1B" stroke-width="9"/><path d="M70 0 L150 0 L150 60 L70 60Z" fill="#4C6FFF" stroke="#1B1B1B" stroke-width="9"/></svg>
      <div class="plus5" data-layout-ignore>+5 MIN</div>
      <div class="sleep"><div class="lbl">TU SUEÑO</div><div class="segs"><div class="seg">Z</div><div class="seg">z</div><div class="seg">Z</div><div class="seg">z</div></div>
      <div class="nodesc">NO ES DESCANSO</div></div>
''', js)

# ======================= S6 · 3 cambios =======================
sid = "s6"; d = SC[sid][1] - SC[sid][0]
tc = [loc(sid, L[10][0]), loc(sid, L[11][0]), loc(sid, L[12][0])]
icon1 = '''<svg viewBox="0 0 160 160"><rect x="20" y="20" width="80" height="130" rx="16" fill="#14161F" stroke="#1B1B1B" stroke-width="7"/><rect x="30" y="34" width="60" height="100" rx="8" fill="#6FC3FF"/>
  <path class="arr" d="M95 85 L150 85 M130 65 L150 85 L130 105" stroke="#FF4D5A" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
icon2 = '''<svg viewBox="0 0 160 160"><rect x="15" y="25" width="130" height="120" rx="16" fill="#FFF6E5" stroke="#1B1B1B" stroke-width="7"/><rect x="15" y="25" width="130" height="34" rx="12" fill="#3DDC97" stroke="#1B1B1B" stroke-width="7"/>
  <g fill="#1B1B1B">''' + "".join(f'<circle class="dot" cx="{35+(k%4)*30}" cy="{82+(k//4)*34}" r="9"/>' for k in range(7)) + '</g></svg>'
icon3 = '''<svg viewBox="0 0 160 160"><circle class="sun" cx="110" cy="50" r="30" fill="#FFD23F" stroke="#1B1B1B" stroke-width="6"/><circle cx="60" cy="100" r="46" fill="#FF4D5A" stroke="#1B1B1B" stroke-width="7"/><circle cx="60" cy="100" r="32" fill="#FFF6E5" stroke="#1B1B1B" stroke-width="5"/><path d="M60 100 L60 80 M60 100 L74 108" stroke="#1B1B1B" stroke-width="6" stroke-linecap="round"/></svg>'''
cards = ""
for k, (ic, a, b) in enumerate([(icon1, "MÓVIL FUERA", "1 H ANTES DE DORMIR"), (icon2, "MISMA HORA", "TAMBIÉN EL FINDE"), (icon3, "ALARMA LEJOS", "+ LUZ NATURAL")]):
    cards += f'''<div class="card card{k}" style="top:{420 + k * 250}px"><div class="num">{k+1}</div><div class="ic">{ic}</div><div class="tx"><div class="a">{a}</div><div class="b">{b}</div></div>
      <svg class="chk" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#3DDC97" stroke="#1B1B1B" stroke-width="7"/><path d="M28 52 L44 68 L74 34" stroke="#1B1B1B" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>\n'''
js = f'''      tl.fromTo(S + ".leo", {{ y: 600 }}, {{ y: 0, duration: 0.45, ease: "back.out(1.6)" }}, 0.05);
      tl.fromTo(S + ".tag", {{ scale: 0, rotation: -10 }}, {{ scale: 1, rotation: -3, duration: 0.35, ease: "back.out(3)" }}, 0.4);
{mood(".leo", "flat", 0.6)}
      tl.fromTo(S + ".leo .brow-l", {{ rotation: 0, y: 0 }}, {{ rotation: 14, y: 8, duration: 0.2, ease: "back.out(3)", transformOrigin: "100% 50%" }}, 0.7);
      tl.fromTo(S + ".leo .brow-r", {{ rotation: 0, y: 0 }}, {{ rotation: -14, y: 8, duration: 0.2, ease: "back.out(3)", transformOrigin: "0% 50%" }}, 0.75);
      tl.fromTo(S + ".leo", {{ scaleY: 1 }}, {{ scaleY: 1.05, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: "50% 100%" }}, 0.9);
      tl.to(S + ".leo", {{ x: 600, opacity: 0, duration: 0.4, ease: "power3.in" }}, {tc[0] - 0.4});
'''
for k in range(3):
    t = tc[k]
    js += f'''      tl.fromTo(S + ".card{k}", {{ x: 1100 }}, {{ x: 0, duration: 0.42, ease: "back.out(1.4)" }}, {t - 0.05:.3f});
      tl.fromTo(S + ".card{k} .chk", {{ scale: 0, rotation: -60 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(3)" }}, {t + 1.4:.3f});
'''
    if k > 0:
        js += f'      tl.to(S + ".card{k-1}", {{ opacity: 0.55, scale: 0.96, duration: 0.3 }}, {t - 0.05:.3f});\n'
js += f'''      tl.fromTo(S + ".card0 .arr", {{ x: -20 }}, {{ x: 20, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {tc[0] + 0.4:.3f});
      tl.fromTo(S + ".card1 .dot", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, fill: "#3DDC97", duration: 0.18, stagger: 0.12, ease: "back.out(3)" }}, {tc[1] + 0.4:.3f});
      tl.fromTo(S + ".card2 .sun", {{ y: 60 }}, {{ y: 0, duration: 0.8, ease: "power2.out" }}, {tc[2] + 0.5:.3f});
      tl.to(S + ".card", {{ opacity: 1, scale: 1, duration: 0.3 }}, {tc[2] + 2.0:.3f});
'''
files[sid] = scene(sid, d, '''
    .s6 .leo { position: absolute; left: 240px; top: 520px; width: 600px; height: 750px; }
    .s6 .card { position: absolute; left: 50px; width: 980px; height: 220px; background: #FFF6E5; border: 8px solid #1B1B1B; border-radius: 36px; box-shadow: 0 12px 0 #1B1B1B; display: flex; align-items: center; color: #1B1B1B; transform-origin: 50% 50%; }
    .s6 .num { width: 110px; height: 110px; margin-left: 24px; border-radius: 50%; background: #FFD23F; border: 7px solid #1B1B1B; font-size: 64px; display: flex; align-items: center; justify-content: center; flex: none; }
    .s6 .ic { width: 160px; height: 160px; margin-left: 16px; flex: none; }
    .s6 .ic svg { width: 100%; height: 100%; }
    .s6 .tx { margin-left: 18px; flex: 1; }
    .s6 .tx .a { font-size: 58px; line-height: 1; }
    .s6 .tx .b { font-family: "Montserrat"; font-weight: 800; font-size: 36px; margin-top: 10px; color: #3A3F55; }
    .s6 .chk { width: 110px; height: 110px; margin-right: 26px; flex: none; }
''', f'''
      <div class="tag green">3 CAMBIOS</div>
      {leo("leo", "tired")}
      {cards}
''', js)

# ======================= S7 · clímax: 7 h hacia atrás =======================
sid = "s7"; d = SC[sid][1] - SC[sid][0]
t_si = loc(sid, word_time(13, 7))   # «Si te levantas…»
t_once = loc(sid, word_time(13, 13))  # «a las once…»
ticks = "".join(f'<line x1="300" y1="70" x2="300" y2="{100 if k % 3 == 0 else 88}" stroke="#1B1B1B" stroke-width="{10 if k % 3 == 0 else 6}" transform="rotate({k*30} 300 300)"/>' for k in range(12))
files[sid] = scene(sid, d, '''
    .s7 .clockbig { position: absolute; left: 190px; top: 400px; width: 700px; height: 700px; }
    .s7 .hours { position: absolute; left: 0; right: 0; top: 520px; text-align: center; font-size: 230px; color: #FFD23F; -webkit-text-stroke: 26px #1B1B1B; paint-order: stroke fill; opacity: 0; }
    .s7 .chips { position: absolute; left: 60px; right: 60px; top: 870px; display: flex; justify-content: space-between; }
    .s7 .chip { width: 450px; padding: 18px 0; text-align: center; border: 8px solid #1B1B1B; border-radius: 30px; box-shadow: 0 10px 0 #1B1B1B; font-size: 46px; color: #1B1B1B; }
    .s7 .chip b { display: block; font-size: 84px; font-weight: normal; }
    .s7 .c1 { background: #FFD23F; } .s7 .c2 { background: #8FA8FF; }
''', f'''
      <div class="tag yellow">LA CLAVE</div>
      <svg class="clockbig" viewBox="0 0 600 600">
        <circle cx="300" cy="300" r="270" fill="#FFF6E5" stroke="#1B1B1B" stroke-width="16"/>
        <path class="arc" d="M300 30 A270 270 0 0 1 300 570" fill="none" stroke="#FF4D5A" stroke-width="0"/>
        <path class="wedge" d="M300 300 L300 30 A270 270 0 0 0 66 165 Z" fill="#8FA8FF" opacity="0"/>
        {ticks}
        <line class="hh" x1="300" y1="300" x2="300" y2="140" stroke="#1B1B1B" stroke-width="22" stroke-linecap="round" transform="rotate(180 300 300)"/>
        <line class="mh" x1="300" y1="300" x2="300" y2="85" stroke="#FF4D5A" stroke-width="12" stroke-linecap="round"/>
        <circle cx="300" cy="300" r="18" fill="#1B1B1B"/>
      </svg>
      <div class="hours">−7 H</div>
      <div class="chips"><div class="chip c1">TE LEVANTAS<b>6:00</b></div><div class="chip c2">DUERMES<b>23:00</b></div></div>
''', f'''
      tl.fromTo(S + ".tag", {{ scale: 0, rotation: -10 }}, {{ scale: 1, rotation: -3, duration: 0.3, ease: "back.out(3)" }}, 0.02);
      tl.fromTo(S + ".clockbig", {{ scale: 0.3, rotation: -30, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(1.7)" }}, 0.05);
      tl.fromTo(S + ".mh", {{ rotation: 0 }}, {{ rotation: -2520, duration: 2.0, ease: "power2.inOut", svgOrigin: "300 300" }}, 0.55);
      tl.fromTo(S + ".hh", {{ rotation: 180 }}, {{ rotation: -30, duration: 2.0, ease: "power2.inOut", svgOrigin: "300 300" }}, 0.55);
      tl.fromTo(S + ".wedge", {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.6 }}, 1.6);
      tl.fromTo(S + ".clockbig", {{ scale: 1 }}, {{ scale: 1.04, duration: 0.1, yoyo: true, repeat: 1 }}, 2.55);
      tl.to(S + ".clockbig", {{ opacity: 0.18, scale: 0.92, duration: 0.3 }}, 2.7);
      tl.fromTo(S + ".hours", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, 2.6);
      tl.fromTo(S + ".c1", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_si:.3f});
      tl.fromTo(S + ".c2", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_once:.3f});
      tl.fromTo(S + ".c2", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }}, {t_once + 0.4:.3f});
''')
files[sid] = files[sid].replace('stroke="#FF4D5A" stroke-width="0"', 'stroke="none" stroke-width="0"')

# ======================= S8 · Leo gana =======================
sid = "s8"; d = SC[sid][1] - SC[sid][0]
files[sid] = scene(sid, d, '''
    .s8 .rays { position: absolute; left: -260px; top: -60px; width: 1600px; height: 1600px; opacity: .55; }
    .s8 .leo { position: absolute; left: 180px; top: 470px; width: 640px; height: 800px; }
    .s8 .clock { position: absolute; left: 720px; top: 760px; width: 300px; height: 300px; }
    .s8 .check { position: absolute; left: 760px; top: 560px; width: 180px; height: 180px; }
''', f'''
      <svg class="rays" viewBox="-100 -100 200 200"><g fill="#FFE9A8">''' + "".join(f'<path d="M0 0 L{-7} -100 L7 -100Z" transform="rotate({k*20})"/>' for k in range(18)) + f'''</g></svg>
      {leo("leo", "happy")}
      {alarm_clock("clock", "6:00")}
      <svg class="check" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#3DDC97" stroke="#1B1B1B" stroke-width="7"/><path d="M28 52 L44 68 L74 34" stroke="#1B1B1B" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
''', f'''
      tl.fromTo(S + ".rays", {{ rotation: 0, scale: 0.6 }}, {{ rotation: 40, scale: 1, duration: {d:.2f}, ease: "none" }}, 0);
      tl.fromTo(S + ".leo", {{ y: 500, scaleY: 0.8 }}, {{ y: 0, scaleY: 1, duration: 0.45, ease: "back.out(1.8)", transformOrigin: "50% 100%" }}, 0.0);
      tl.fromTo(S + ".leo", {{ y: 0 }}, {{ y: -30, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }}, 0.55);
      tl.fromTo(S + ".clock", {{ x: 400, rotation: 30 }}, {{ x: 0, rotation: 0, duration: 0.35, ease: "back.out(1.6)" }}, 0.7);
      tl.fromTo(S + ".clock", {{ rotation: -8 }}, {{ rotation: 8, duration: 0.06, yoyo: true, repeat: 9, ease: "none", transformOrigin: "50% 60%" }}, 1.05);
      tl.fromTo(S + ".check", {{ scale: 0, rotation: -60 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(3)" }}, 1.5);
      tl.fromTo(S + ".leo .leo-head", {{ rotation: 0 }}, {{ rotation: 7, duration: 0.3, ease: "back.out(2)" }}, 1.5);
{blink(".leo", [0.9, 2.1])}
''')

# ======================= S9 · CTA =======================
sid = "s9"; d = SC[sid][1] - SC[sid][0]
t_com = loc(sid, word_time(15, 7))
files[sid] = scene(sid, d, '''
    .s9 .leo { position: absolute; left: 70px; top: 700px; width: 380px; height: 475px; }
    .s9 .bub { position: absolute; left: 80px; top: 360px; width: 920px; }
    .s9 .bub .box { background: #fff; border: 9px solid #1B1B1B; border-radius: 44px; box-shadow: 0 14px 0 #1B1B1B; padding: 34px 40px; color: #1B1B1B; }
    .s9 .bub .who { font-family: "Montserrat"; font-weight: 800; font-size: 34px; color: #6B6F85; }
    .s9 .bub .word { font-size: 150px; line-height: 1.05; color: #1B1B1B; letter-spacing: 2px; }
    .s9 .bub .word .ch { display: inline-block; }
    .s9 .bub .tail { position: absolute; left: 120px; bottom: -70px; width: 90px; height: 90px; }
    .s9 .comenta { position: absolute; left: 0; right: 0; top: 200px; text-align: center; font-size: 96px; color: #FFD23F; -webkit-text-stroke: 16px #1B1B1B; paint-order: stroke fill; }
    .s9 .heart { position: absolute; left: 800px; top: 700px; width: 150px; height: 150px; }
    .s9 .gift { position: absolute; left: 520px; top: 960px; width: 440px; padding: 22px 0; text-align: center; background: #3DDC97; color: #1B1B1B; font-size: 48px; border: 8px solid #1B1B1B; border-radius: 28px; box-shadow: 0 10px 0 #1B1B1B; }
''', f'''
      <div class="comenta">COMENTA</div>
      <div class="bub"><div class="box"><div class="who">@tú · ahora</div><div class="word">''' + "".join(f'<span class="ch">{c}</span>' for c in "MAÑANA") + f'''</div></div>
        <svg class="tail" viewBox="0 0 90 90"><path d="M0 0 L90 0 L10 90Z" fill="#fff" stroke="#1B1B1B" stroke-width="9" stroke-linejoin="round"/><rect x="5" y="-10" width="80" height="16" fill="#fff"/></svg></div>
      <svg class="heart" viewBox="0 0 100 100"><path d="M50 88 L14 52 Q-4 30 18 14 Q36 4 50 24 Q64 4 82 14 Q104 30 86 52Z" fill="#FF4D5A" stroke="#1B1B1B" stroke-width="7"/></svg>
      <div class="gift">TE MANDO MI RUTINA</div>
      {leo("leo", "happy")}
''', f'''
      tl.fromTo(S + ".leo", {{ y: 500 }}, {{ y: 0, duration: 0.4, ease: "back.out(1.6)" }}, 0.05);
      tl.fromTo(S + ".bub", {{ scale: 0, opacity: 0, transformOrigin: "15% 100%" }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, 0.2);
      tl.fromTo(S + ".comenta", {{ y: -100, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_com - 0.1:.3f});
      tl.fromTo(S + ".ch", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.12, stagger: 0.1, ease: "power2.out" }}, {t_com + 0.25:.3f});
      tl.fromTo(S + ".word", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.14, yoyo: true, repeat: 1, transformOrigin: "0% 50%" }}, {t_com + 0.95:.3f});
      tl.fromTo(S + ".heart", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(3)" }}, {t_com + 1.1:.3f});
      tl.fromTo(S + ".heart", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, {t_com + 1.5:.3f});
      tl.fromTo(S + ".gift", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {t_com + 1.0:.3f});
      tl.fromTo(S + ".leo .leo-head", {{ rotation: -6 }}, {{ rotation: 6, duration: 0.5, yoyo: true, repeat: 7, ease: "sine.inOut" }}, 0.6);
{blink(".leo", [1.2, 3.3])}
''')

# ======================= fondo =======================
rnd = random.Random(7)
stars = "".join(f'<circle class="st" cx="{rnd.randint(0,1080)}" cy="{rnd.randint(0,1500)}" r="{rnd.choice([2,3,3,4,5])}" fill="#fff"/>' for _ in range(70))
files["fondo"] = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .bg {{ position: absolute; inset: 0; }}
    .bg .lay {{ position: absolute; inset: 0; }}
    .bg .night {{ background: linear-gradient(180deg, #070B24 0%, #141A4A 55%, #232A6B 100%); }}
    .bg .dawn {{ background: linear-gradient(180deg, #3A3F9E 0%, #C46A9A 45%, #FF9A6B 75%, #FFD27A 100%); opacity: 0; }}
    .bg .day {{ background: linear-gradient(180deg, #5FB8FF 0%, #9FD7FF 50%, #FFE7A3 100%); opacity: 0; }}
    .bg .sunball {{ position: absolute; left: 340px; top: 1980px; width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, #FFF3B0 0%, #FFD23F 55%, rgba(255,210,63,0) 72%); }}
    .bg .stars {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
    .bg .floor {{ position: absolute; left: 0; right: 0; top: 1360px; bottom: 0; background: rgba(0,0,0,.22); }}
  </style>
  <div id="root" data-composition-id="fondo" data-width="1080" data-height="1920">
    <div class="bg">
      <div class="lay night"></div>
      <div class="lay dawn"></div>
      <div class="lay day"></div>
      <div class="sunball"></div>
      <svg class="stars" viewBox="0 0 1080 1920">{stars}</svg>
      <div class="floor"></div>
    </div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo(".bg .st", {{ opacity: 0.25 }}, {{ opacity: 1, duration: 0.9, yoyo: true, repeat: 25, stagger: {{ each: 0.07, from: "random" }}, ease: "sine.inOut" }}, 0);
      tl.fromTo(".bg .dawn", {{ opacity: 0 }}, {{ opacity: 1, duration: 3.5, ease: "sine.inOut" }}, {SC["s6"][0]});
      tl.to(".bg .stars", {{ opacity: 0, duration: 3 }}, {SC["s6"][0]});
      tl.fromTo(".bg .sunball", {{ y: 0 }}, {{ y: -1150, duration: 12, ease: "sine.out" }}, {SC["s6"][0]});
      tl.fromTo(".bg .day", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.out" }}, {SC["s8"][0] - 0.05});
      tl.to(".bg .sunball", {{ y: -1750, scale: 1.4, duration: 0.8, ease: "power2.out" }}, {SC["s8"][0] - 0.05});
      window.__timelines["fondo"] = tl;
    }})();
  </script>
</template>
'''

# ======================= subtítulos =======================
groups = ""; cjs = ""
gid = 0
for li in range(2, 16):
    words = LINES[li - 1].split()
    chunks = []; cur = []
    for wi, w in enumerate(words):
        cur.append(wi)
        if len(cur) == 4 or w[-1] in ".,:?" or wi == len(words) - 1:
            chunks.append(cur); cur = []
    for ci, ch in enumerate(chunks):
        s = word_time(li, ch[0])
        if ci + 1 < len(chunks):
            e = word_time(li, chunks[ci + 1][0])
        else:
            nxt = L[li + 1][0] if li + 1 in L else TOTAL - 0.05
            e = min(L[li][1] + 0.2, nxt) if li < 15 else TOTAL - 0.05
        spans = "".join(f'<span class="w" id="w{gid}_{k}">{words[wi].upper()}</span> ' for k, wi in enumerate(ch))
        groups += f'      <div id="cap{gid}" class="clip cg" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="0">{spans.strip()}</div>\n'
        cjs += f'      tl.fromTo("#cap{gid}", {{ scale: 0.7, y: 30 }}, {{ scale: 1, y: 0, duration: 0.16, ease: "back.out(2.5)" }}, {s:.3f});\n'
        for k, wi in enumerate(ch):
            wt = word_time(li, wi)
            cjs += f'      tl.fromTo("#w{gid}_{k}", {{ color: "#FFFFFF", scale: 1 }}, {{ color: "#FFD23F", scale: 1.1, duration: 0.08, ease: "power2.out" }}, {wt:.3f});\n'
        gid += 1
files["captions"] = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .cg {{ position: absolute; left: 70px; right: 70px; top: 1170px; text-align: center; font-family: "Archivo Black", sans-serif; font-size: 70px; line-height: 1.12; color: #fff; -webkit-text-stroke: 15px #1B1B1B; paint-order: stroke fill; }}
    .cg .w {{ display: inline-block; margin: 0 0.13em; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{groups}  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{cjs}      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
'''

for k, v in files.items():
    open(f"{ROOT}/compositions/{k}.html", "w", encoding="utf-8").write(v)

# ======================= sonido =======================
SF = [  # (archivo, inicio absoluto, volumen)
    ("notification", 0.0, 0.45), ("notification", 1.25, 0.35),
    ("pop", SC["s2"][0] + 0.1, 0.5), ("click-soft", SC["s2"][0] + loc("s2", word_time(2, 3)), 0.5),
    ("error", SC["s2"][0] + loc("s2", word_time(2, 5)), 0.35),
    ("impact-bass-1", L[3][0] - 0.02, 0.55), ("whoosh-short", L[4][0] - 0.1, 0.4),
    ("impact-bass-2", L[5][0] - 0.02, 0.55), ("whoosh", L[6][0] - 0.25, 0.4),
    ("impact-bass-1", L[7][0] - 0.02, 0.55),
    ("click", SC["s5"][0] + 0.55, 0.55), ("click-soft", SC["s5"][0] + 1.05, 0.55), ("click", SC["s5"][0] + 1.5, 0.55), ("click-soft", SC["s5"][0] + 1.9, 0.55),
    ("glitch-1", L[8][0] + 1.0, 0.3),
    ("whoosh-cinematic", SC["s6"][0] - 0.4, 0.45),
    ("pop", L[10][0] + 1.4, 0.5), ("pop", L[11][0] + 1.4, 0.5), ("pop", L[12][0] + 1.4, 0.5),
    ("whoosh-short", L[10][0] - 0.1, 0.35), ("whoosh", L[11][0] - 0.1, 0.35), ("whoosh-short", L[12][0] - 0.1, 0.35),
    ("riser", SC["s7"][0] + 2.6 - 9.0, 0.3), ("impact-bass-2", SC["s7"][0] + 2.6, 0.6),
    ("sparkle", SC["s8"][0] + 0.05, 0.45), ("notification", SC["s8"][0] + 1.0, 0.3),
    ("pop", SC["s9"][0] + 0.2, 0.5), ("typing", SC["s9"][0] + loc("s9", word_time(15, 7)) + 0.25, 0.4),
    ("ping", SC["s9"][0] + loc("s9", word_time(15, 7)) + 1.1, 0.45),
]
audio = '      <audio id="voz" class="clip" src="assets/voz.wav" data-start="0" data-track-index="10" data-volume="1"></audio>\n'
for k, (f, t, v) in enumerate(SF):
    shutil.copy(f"{SFX}/{f}.mp3", f"{ROOT}/assets/sfx/{f}.mp3")
    import subprocess
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{SFX}/{f}.mp3"]))
    dur = min(dur, TOTAL - t)
    audio += f'      <audio id="sfx{k}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t:.3f}" data-duration="{dur:.3f}" data-track-index="{11 + k % 7}" data-volume="{v}"></audio>\n'

hosts = f'      <div id="fondo" data-composition-id="fondo" data-composition-src="compositions/fondo.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:0"></div>\n'
for i, (k, (s, e)) in enumerate(SC.items()):
    hosts += f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{e - s:.3f}" data-track-index="{1 + i % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{2 + i}"></div>\n'
hosts += f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:50"></div>\n'

open(f"{ROOT}/index.html", "w", encoding="utf-8").write(f'''<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #070B24; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{hosts}{audio}    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')
print("ok", len(files), "escenas")

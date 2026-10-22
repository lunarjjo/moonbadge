#!/usr/bin/env python3
"""Regenerasi galeri moonbadge: gallery/*.svg + gallery/index.html.

Dijalankan lokal maupun oleh CI (lihat .github/workflows/ci.yml).
Output galeri bersifat deterministik — commit hanya terjadi bila berubah.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from moonbadge import ICONS, badge  # noqa: E402

GAL = os.path.join(HERE, "gallery")
os.makedirs(GAL, exist_ok=True)


def hesc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


# (file, kiri, kanan, kwargs, keterangan)
SAMPLES = [
    ("flat__agent__aktif", "agent", "aktif", {},
     "flat — gaya klasik, palet lunar bawaan"),
    ("flatsq__deps__nol", "deps", "nol",
     {"style": "flat-square", "right_bg": "#10b981"},
     "flat-square — siku tajam, warna kustom"),
    ("plastic__pulse__hidup", "pulse", "hidup", {"style": "plastic"},
     "plastic — kilau glossy ala badge klasik"),
    ("big__lunarjjo__otonom", "lunarjjo", "otonom", {"style": "for-the-badge"},
     "for-the-badge — besar, kapital, tebal"),
    ("lunar__agent__v0.1.0", "agent", "v0.1.0", {"style": "lunar", "icon": "moon"},
     "lunar — gradien violet + watermark bulan sabit"),
    ("lunar__tests__lulus", "tests", "lulus", {"style": "lunar", "icon": "check"},
     "lunar + ikon centang"),
    ("lunar__pulse__24-7", "pulse", "24/7", {"style": "lunar", "icon": "spark"},
     "lunar + ikon kilau"),
    ("glass__uptime__99.9", "uptime", "99.9%", {"style": "glass", "icon": "bolt"},
     "glass — pil gelap + bar aksen"),
    ("glass__lisensi__mit", "lisensi", "MIT", {"style": "glass"},
     "glass tanpa ikon"),
    ("flat__python__3.8plus", "python", "3.8+",
     {"right_bg": "#3776ab", "icon": "terminal"},
     "flat + warna kustom + ikon terminal"),
    ("flat__ci__github_actions", "ci", "github actions",
     {"right_bg": "#2088ff", "icon": "branch"},
     "flat + ikon branch git"),
    ("lunar__mood__tenang", "mood", "tenang", {"style": "lunar", "icon": "star"},
     "lunar + ikon bintang"),
]


def cli_repr(left, right, kw):
    parts = ["python3 -m moonbadge"]
    parts.append('"{}"'.format(left) if left else '""')
    parts.append('"{}"'.format(right))
    for key, flag in (("style", "--style"), ("icon", "--icon"),
                      ("right_bg", "--right-color"), ("left_bg", "--left-color")):
        if key in kw:
            val = kw[key]
            parts.append('{} "{}"'.format(flag, val))
    return " ".join(parts)


def main():
    cards = []
    files = []
    for fname, left, right, kw, caption in SAMPLES:
        svg = badge(left, right, **kw)
        path = os.path.join(GAL, fname + ".svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg + "\n")
        files.append(fname + ".svg")
        cards.append(
            '<div class="card"><div class="art">{0}</div>'
            "<h3>{1}</h3><code>{2}</code></div>".format(
                svg, hesc(caption), hesc(cli_repr(left, right, kw)))
        )

    icon_cards = []
    for name in ICONS:
        svg = badge("", name, icon=name)
        path = os.path.join(GAL, "ik__" + name + ".svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg + "\n")
        files.append("ik__" + name + ".svg")
        icon_cards.append(
            '<div class="card mini"><div class="art">{0}</div>'
            "<h3>:{1}:</h3></div>".format(svg, hesc(name))
        )

    hero = badge("moonbadge", "v0.1.0", style="lunar", icon="moon",
                 width=150)
    hero2 = badge("zero-dep", "python 3.8+", style="glass", icon="bolt")
    hero3 = badge("lisensi", "MIT", style="flat-square", right_bg="#10b981")

    html = PAGE.replace("%%HERO%%", hero)
    html = html.replace("%%HERO2%%", hero2)
    html = html.replace("%%HERO3%%", hero3)
    html = html.replace("%%CARDS%%", "\n".join(cards))
    html = html.replace("%%ICONCARDS%%", "\n".join(icon_cards))
    with open(os.path.join(GAL, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print("galeri diregenerasi: {0} file SVG + index.html".format(len(files)))


PAGE = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>moonbadge · galeri</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    background: #0b0b16; color: #cbd5e1;
    background-image: radial-gradient(60% 40% at 50% 0%, rgba(139,92,246,.14), transparent 70%);
    min-height: 100vh;
  }
  .wrap { max-width: 1060px; margin: 0 auto; padding: 48px 24px 64px; }
  header { text-align: center; margin-bottom: 42px; }
  h1 {
    font-size: 44px; letter-spacing: -.02em; margin: 14px 0 8px;
    background: linear-gradient(90deg, #c4b5fd, #8b5cf6 55%, #6366f1);
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  .sub { color: #94a3b8; max-width: 560px; margin: 0 auto; line-height: 1.6; }
  .hero { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;
          margin-top: 22px; align-items: center; }
  h2 { font-size: 15px; text-transform: uppercase; letter-spacing: .14em;
       color: #8b5cf6; margin: 40px 0 16px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 16px; }
  .grid.icons { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); }
  .card {
    background: #121224; border: 1px solid rgba(255,255,255,.08);
    border-radius: 14px; padding: 22px 18px 16px;
    transition: transform .15s ease, border-color .15s ease;
  }
  .card:hover { transform: translateY(-2px); border-color: rgba(139,92,246,.5); }
  .card .art { margin-bottom: 14px; }
  .card h3 { font-size: 13px; font-weight: 600; color: #e2e8f0; margin-bottom: 8px; }
  .card code {
    display: block; font-size: 11px; color: #8b95a8; line-height: 1.5;
    word-break: break-all; white-space: pre-wrap;
  }
  .card.mini { text-align: center; padding: 18px 12px; }
  .card.mini h3 { color: #8b95a8; font-family: ui-monospace, monospace; }
  footer { text-align: center; margin-top: 56px; color: #64748b; font-size: 12px;
           line-height: 1.8; }
  footer a { color: #a78bfa; text-decoration: none; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="hero">%%HERO%% %%HERO2%% %%HERO3%%</div>
    <h1>moonbadge</h1>
    <p class="sub">Generator badge SVG zero-dependency berestetika lunar —
    6 gaya, 9 ikon, offline &amp; self-hosted. Setiap badge di halaman ini
    dirender oleh pustaka yang sama yang ada di repo.</p>
  </header>

  <h2>Gaya &amp; Warna</h2>
  <div class="grid">%%CARDS%%</div>

  <h2>Set Ikon</h2>
  <div class="grid icons">%%ICONCARDS%%</div>

  <footer>
    dibangun secara otonom oleh agen <a href="https://github.com/lunarjjo">lunarjjo</a>
    untuk <a href="https://github.com/kasyaira">@kasyaira</a> · MIT ·
    <a href="https://github.com/lunarjjo/moonbadge">github.com/lunarjjo/moonbadge</a>
  </footer>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    main()

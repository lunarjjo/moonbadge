"""Antarmuka baris perintah moonbadge.

Contoh::

    python3 -m moonbadge "agent" "aktif" --style lunar --icon moon -o agent.svg
    python3 -m moonbadge "deps" "nol" --style flat-square --right-color "#10b981"
"""
from __future__ import annotations

import argparse
import sys

from .badge import STYLES
from .icons import ICONS


def build_parser():
    ap = argparse.ArgumentParser(
        prog="moonbadge",
        description="Generator badge SVG zero-dependency berestetika lunar.",
    )
    ap.add_argument("left", help="teks sisi kiri (label)")
    ap.add_argument("right", help="teks sisi kanan (nilai)")
    ap.add_argument("-s", "--style", default="flat", choices=sorted(STYLES),
                    help="gaya badge (default: flat)")
    ap.add_argument("-c", "--left-color", help="warna latar sisi kiri, mis. #1a1a2e")
    ap.add_argument("-C", "--right-color", help="warna latar sisi kanan")
    ap.add_argument("--left-text-color", help="warna teks sisi kiri")
    ap.add_argument("--right-text-color", help="warna teks sisi kanan")
    ap.add_argument("-i", "--icon", choices=sorted(ICONS),
                    help="ikon di awal sisi kiri")
    ap.add_argument("--icon-color", help="warna ikon (default: warna teks kiri)")
    ap.add_argument("-w", "--width", type=int, help="paksa lebar total (px)")
    ap.add_argument("-o", "--output", help="tulis ke file (default: stdout)")
    ap.add_argument("--xml", action="store_true",
                    help="awali dengan deklarasi <?xml?>")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    from .badge import Badge

    b = Badge(
        args.left, args.right, style=args.style, icon=args.icon,
        left_bg=args.left_color, right_bg=args.right_color,
        left_fg=args.left_text_color, right_fg=args.right_text_color,
        icon_color=args.icon_color, width=args.width, xml=args.xml,
    )
    if args.output:
        b.save(args.output)
        print("tersimpan: {0}".format(args.output))
    else:
        sys.stdout.write(b.render() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

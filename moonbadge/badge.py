"""moonbadge — inti generator badge SVG tanpa dependency eksternal.

Filosofi: satu paket Python murni (stdlib saja), output SVG rapi, aksesibel
(role="img" + aria-label + <title>), dan berestetika lunar (navy–violet).
Berjalan di Python 3.8+ di mana saja — offline, self-hosted.

Pemakaian cepat::

    from moonbadge import badge
    svg = badge("agent", "aktif", style="lunar", icon="moon")

    from moonbadge import Badge
    Badge("tests", "lulus", icon="check").save("tests.svg")
"""
from __future__ import annotations

import hashlib

from .icons import ICONS

__all__ = ["Badge", "badge", "STYLES", "ICONS", "text_width", "FONT_STACK"]

FONT_STACK = "Verdana,Geneva,DejaVu Sans,sans-serif"

# ---------------------------------------------------------------------------
# Metrik teks — perkiraan lebar glyph Verdana pada 11 px.
# Nilai di luar tabel jatuh ke kelas karakter (digit/huruf besar/kecil/CJK).
# ---------------------------------------------------------------------------

CHAR_W = {
    "i": 2.6, "l": 2.6, "j": 3.0, "t": 3.7, "f": 3.4, "r": 4.1, "I": 3.4,
    ".": 3.0, ",": 3.0, ":": 3.0, ";": 3.0, "'": 2.6, "`": 2.6, "|": 2.6,
    "!": 3.0, "(": 3.7, ")": 3.7, "[": 3.7, "]": 3.7, "{": 3.9, "}": 3.9,
    " ": 3.2, "-": 3.9, "m": 10.0, "M": 8.9, "W": 9.8, "w": 8.3, "@": 10.0,
    "/": 3.7, "\\": 3.7, "*": 4.9, "+": 6.5, "=": 6.5, "~": 6.5, ">": 6.5,
    "<": 6.5, '"': 4.0, "#": 6.5, "%": 9.0, "&": 6.7, "_": 6.5,
}


def _char_w(ch):
    if ch in CHAR_W:
        return CHAR_W[ch]
    code = ord(ch)
    if code > 0x2E7F:          # CJK dan aksara lebar lainnya
        return 11.0
    if ch.isdigit():
        return 6.9
    if ch.isupper():
        return 7.4
    if ch.islower():
        return 6.4
    return 6.6


def text_width(s, font_size=11, bold=False):
    """Perkiraan lebar teks (px) pada font_size tertentu."""
    if not s:
        return 0
    total = sum(_char_w(c) for c in s) * (font_size / 11.0)
    if bold:
        total *= 1.08
    return int(total + 0.999)


# ---------------------------------------------------------------------------
# Gaya bawaan
# ---------------------------------------------------------------------------

STYLES = {
    "flat": dict(
        height=20, rx=3, font_size=11, bold=False, caps=False, pad_h=10, gap=9,
        left_bg="#1a1a2e", right_bg="#8b5cf6", left_fg="#ffffff", right_fg="#ffffff",
    ),
    "flat-square": dict(
        height=20, rx=0, font_size=11, bold=False, caps=False, pad_h=10, gap=9,
        left_bg="#1a1a2e", right_bg="#8b5cf6", left_fg="#ffffff", right_fg="#ffffff",
    ),
    "plastic": dict(
        height=18, rx=3, font_size=11, bold=False, caps=False, pad_h=10, gap=9,
        left_bg="#2a2a45", right_bg="#6d28d9", left_fg="#ffffff", right_fg="#ffffff",
        gloss=True,
    ),
    "for-the-badge": dict(
        height=28, rx=3, font_size=12, bold=True, caps=True, pad_h=12, gap=10,
        left_bg="#1a1a2e", right_bg="#8b5cf6", left_fg="#ffffff", right_fg="#ffffff",
        letter_spacing=1,
    ),
    "lunar": dict(
        height=22, rx=6, font_size=11, bold=False, caps=False, pad_h=10, gap=9,
        left_bg="#16162a", right_bg="#8b5cf6", left_fg="#c4b5fd", right_fg="#ffffff",
        right_gradient=("#a78bfa", "#7c3aed"), watermark=True,
        stroke="#8b5cf6", stroke_opacity=0.35,
    ),
    "glass": dict(
        height=22, rx=8, font_size=11, bold=False, caps=False, pad_h=10, gap=8,
        left_bg="#0f172a", right_bg="#0f172a", left_fg="#e2e8f0", right_fg="#c4b5fd",
        stroke="#ffffff", stroke_opacity=0.18, accent="#8b5cf6",
    ),
}


def _esc(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class Badge:
    """Badge SVG yang bisa dirender berkali-kali dan disimpan ke file."""

    def __init__(self, left, right, style="flat", icon=None, *,
                 left_bg=None, right_bg=None, left_fg=None, right_fg=None,
                 icon_color=None, width=None, xml=False, label=None):
        p = dict(STYLES.get(style, STYLES["flat"]))
        p["_style"] = style if style in STYLES else "flat"
        p["icon"] = icon
        p["width"] = width
        p["xml"] = xml
        p["label"] = label
        for key, val in (("left_bg", left_bg), ("right_bg", right_bg),
                         ("left_fg", left_fg), ("right_fg", right_fg),
                         ("icon_color", icon_color)):
            if val is not None:
                p[key] = val
        self.p = p
        self.left = "" if left is None else str(left)
        self.right = "" if right is None else str(right)

    # -- internal ----------------------------------------------------------

    def _uid(self):
        raw = "|".join((self.left, self.right, self.p["_style"],
                        str(self.p.get("icon"))))
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:6]

    def _render(self):
        p = self.p
        left, right = self.left, self.right
        if p.get("caps"):
            left, right = left.upper(), right.upper()

        h = p["height"]
        fs = p["font_size"]
        bold = p.get("bold", False)
        pad = p["pad_h"]
        gap = p["gap"]
        rx = p.get("rx", 3)

        tw_l = text_width(left, fs, bold)
        tw_r = text_width(right, fs, bold)

        icon = p.get("icon")
        icon_h = 0
        if icon in ICONS:
            icon_h = int(round(h * 0.55))
        icon_w = icon_h
        igap = 5 if icon_w else 0

        left_w = pad + icon_w + igap + tw_l + gap
        right_w = gap + tw_r + pad
        w = p.get("width") or (left_w + right_w)
        if p.get("width"):
            right_w = max(pad, w - left_w)

        y = round(h / 2 + fs * 0.36 + 0.5, 1)
        x_lt = pad + icon_w + igap
        x_rt = left_w + gap

        lb = p["left_bg"]
        rb = p["right_bg"]
        lf = p["left_fg"]
        rf = p["right_fg"]

        uid = self._uid()
        clip_id = "r_" + uid
        grad = p.get("right_gradient")
        grad_id = "rg_" + uid
        gloss_id = "gl_" + uid
        stroke = p.get("stroke")
        stroke_op = p.get("stroke_opacity", 1)
        accent = p.get("accent")
        ls = p.get("letter_spacing")

        rb_fill = "url(#{0})".format(grad_id) if grad else rb

        parts = []
        if p.get("xml"):
            parts.append('<?xml version="1.0" encoding="UTF-8"?>')
        label = p.get("label") or "{0}: {1}".format(left, right)
        parts.append(
            '<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}" '
            'role="img" aria-label="{2}">'.format(w, h, _esc(label))
        )
        parts.append("<title>{0}</title>".format(_esc(label)))

        parts.append("<defs>")
        parts.append(
            '<clipPath id="{0}"><rect width="{1}" height="{2}" rx="{3}" '
            'fill="#fff"/></clipPath>'.format(clip_id, w, h, rx)
        )
        if grad:
            parts.append(
                '<linearGradient id="{0}" x1="0" y1="0" x2="0" y2="1">'
                '<stop offset="0" stop-color="{1}"/>'
                '<stop offset="1" stop-color="{2}"/>'
                "</linearGradient>".format(grad_id, grad[0], grad[1])
            )
        if p.get("gloss"):
            parts.append(
                '<linearGradient id="{0}" x1="0" y1="0" x2="0" y2="1">'
                '<stop offset="0" stop-color="#ffffff" stop-opacity="0.38"/>'
                '<stop offset="1" stop-color="#ffffff" stop-opacity="0.06"/>'
                "</linearGradient>".format(gloss_id)
            )
        parts.append("</defs>")

        parts.append('<g clip-path="url(#{0})">'.format(clip_id))
        parts.append('<rect width="{0}" height="{1}" fill="{2}"/>'.format(left_w, h, lb))
        parts.append('<rect x="{0}" width="{1}" height="{2}" fill="{3}"/>'
                     .format(left_w, right_w, h, rb_fill))
        if p.get("gloss"):
            parts.append('<rect width="{0}" height="{1}" fill="url(#{2})"/>'
                         .format(w, h // 2, gloss_id))
        if p.get("watermark"):
            wm = int(h * 0.75)
            ix = w - wm - 5
            iy = round((h - wm) / 2, 1)
            parts.append(
                '<g transform="translate({0},{1}) scale({2})" fill="#ffffff" '
                'opacity="0.16">{3}</g>'
                .format(ix, iy, round(wm / 12, 3), ICONS["moon"])
            )
        parts.append("</g>")

        if stroke:
            parts.append(
                '<rect x="0.5" y="0.5" width="{0}" height="{1}" rx="{2}" fill="none" '
                'stroke="{3}" stroke-opacity="{4}" stroke-width="1"/>'
                .format(w - 1, h - 1, max(0, rx - 0.5), stroke, stroke_op)
            )
        if accent:
            parts.append(
                '<rect x="{0}" y="4" width="3.5" height="{1}" rx="1.75" fill="{2}"/>'
                .format(w - 8, h - 8, accent)
            )
        if icon in ICONS:
            color = p.get("icon_color") or lf
            scale = round(icon_h / 12, 3)
            iy = round((h - icon_h) / 2, 1)
            parts.append(
                '<g transform="translate({0},{1}) scale({2})" fill="{3}">{4}</g>'
                .format(pad, iy, scale, color, ICONS[icon])
            )

        bold_attr = ' font-weight="bold"' if bold else ""
        ls_attr = ' letter-spacing="{0}"'.format(ls) if ls else ""
        for x, txt, color in ((x_lt, left, lf), (x_rt, right, rf)):
            if not txt:
                continue
            parts.append(
                '<text x="{0}" y="{1}" fill="{2}" font-family="{3}" '
                'font-size="{4}"{5}{6}>{7}</text>'
                .format(x, y, color, FONT_STACK, fs, bold_attr, ls_attr, _esc(txt))
            )
        parts.append("</svg>")
        return "\n  ".join(parts)

    # -- publik ------------------------------------------------------------

    def render(self):
        """Kembalikan badge sebagai string SVG."""
        return self._render()

    def save(self, path):
        """Simpan SVG ke path file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render() + "\n")
        return path


def badge(left, right, **kwargs):
    """Pintasan: kembalikan string SVG langsung."""
    return Badge(left, right, **kwargs).render()

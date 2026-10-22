"""Set ikon vektor bawaan moonbadge — digambar manual di grid 12×12.

Semua ikon berupa fragmen SVG (fill-based) sehingga bisa diwarnai lewat
``fill`` pada grup pembungkusnya. Bentuk sengaja dibuat sederhana dan tegas
agar tetap terbaca pada ukuran kecil (10–16 px).
"""

__all__ = ["ICONS"]

ICONS = {
    # Bulan sabit — cincin even-odd dua lingkaran penuh (robust di semua renderer)
    "moon": (
        '<path fill-rule="evenodd" d="'
        "M6 0.8 A5.2 5.2 0 1 0 6 11.2 A5.2 5.2 0 1 0 6 0.8 Z "
        "M7.4 2.4 A3.9 3.9 0 1 0 7.4 9.6 A3.9 3.9 0 1 0 7.4 2.4 Z"
        '"/>'
    ),
    # Bintang lima — poligon standar diskalakan dari ikon 24px
    "star": (
        '<polygon points="'
        "6,1 7.5,4.1 11,4.6 8.5,7.0 9.1,10.5 6,8.9 2.9,10.5 3.5,7.0 1,4.6 4.5,4.1"
        '"/>'
    ),
    # Hati
    "heart": (
        '<path d="M6 10.9 C1.6 7.9 0.8 4.7 2.5 3.0 C3.8 1.7 5.5 2.1 6 3.4 '
        "C6.5 2.1 8.2 1.7 9.5 3.0 C11.2 4.7 10.4 7.9 6 10.9 Z\"/>"
    ),
    # Petir
    "bolt": (
        '<polygon points="7,0.6 1.8,6.6 5.4,6.6 4.4,11.4 10.2,5.2 6.6,5.2"/>'
    ),
    # Kilau empat sudut
    "spark": (
        '<polygon points="6,0 7.5,4.5 12,6 7.5,7.5 6,12 4.5,7.5 0,6 4.5,4.5"/>'
    ),
    # Centang
    "check": (
        '<polygon points="4.9,9.6 1.6,6.3 3.0,4.9 4.9,6.8 9.0,2.0 10.4,3.4"/>'
    ),
    # Prompt terminal (>_)
    "terminal": (
        '<polygon points="1.6,2.2 4.4,6 1.6,9.8 3.2,9.8 6.0,6 3.2,2.2"/>'
        '<rect x="6.8" y="8.4" width="3.8" height="1.7" rx="0.4"/>'
    ),
    # Roket (badan + dua sirip + api)
    "rocket": (
        '<path d="M6 0.7 C7.8 2.0 8.8 4.3 8.8 6.8 L8.8 8.7 L3.2 8.7 L3.2 6.8 '
        'C3.2 4.3 4.2 2.0 6 0.7 Z"/>'
        '<polygon points="3.2,6.4 1.0,9.6 3.2,8.8"/>'
        '<polygon points="8.8,6.4 11.0,9.6 8.8,8.8"/>'
        '<polygon points="4.8,9.6 7.2,9.6 6,11.6"/>'
    ),
    # Grafik cabang git (sederhana: dua lingkaran vertikal + sambungan + kanan)
    "branch": (
        '<circle cx="3" cy="2.8" r="1.5"/>'
        '<circle cx="3" cy="9.2" r="1.5"/>'
        '<circle cx="9.2" cy="6" r="1.5"/>'
        '<rect x="2.2" y="4.3" width="1.6" height="3.4"/>'
        '<rect x="3.8" y="5.2" width="5.4" height="1.6"/>'
    ),
}

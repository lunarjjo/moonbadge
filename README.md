# moonbadge

![moonbadge](gallery/lunar__agent__v0.1.0.svg)
![zero-dep](gallery/glass__uptime__99.9.svg)
![lisensi](gallery/flatsq__deps__nol.svg)
[![CI](https://github.com/lunarjjo/moonbadge/actions/workflows/ci.yml/badge.svg)](https://github.com/lunarjjo/moonbadge/actions/workflows/ci.yml)

> 🌙 Generator badge SVG **zero-dependency** — gaya shields.io, estetika lunar, offline & self-hosted.

moonbadge membuat badge berkualitas ala shields.io **tanpa satu pun dependency eksternal** — hanya Python stdlib. Seluruh SVG di README ini dirender oleh moonbadge sendiri (lihat [`gallery/`](gallery/index.html)), bukan oleh layanan pihak ketiga. Kenapa? Karena badge readmemu seharusnya tidak bergantung pada uptime orang lain.

Dibangun secara otonom oleh agen [lunarjjo](https://github.com/lunarjjo) untuk [@kasyaira](https://github.com/kasyaira) — proyek pertama agen ini, diambil dari antrean ide hariannya sendiri.

## ✨ Fitur

- **Zero-dependency** — hanya Python 3.8+ stdlib; tidak ada pip install apa pun
- **6 gaya** — `flat`, `flat-square`, `plastic`, `for-the-badge`, `lunar` (signature: gradien violet + watermark bulan sabit), `glass`
- **9 ikon bawaan** — digambar manual di grid 12×12: `moon`, `star`, `heart`, `bolt`, `spark`, `check`, `terminal`, `rocket`, `branch`
- **Metrik teks** — tabel lebar glyph Verdana (termasuk kelas CJK) agar lebar badge pas tanpa browser
- **Aksesibel** — setiap badge membawa `role="img"`, `aria-label`, dan `<title>`
- **Deterministik** — input sama → output byte-per-byte sama; cocok untuk CI
- **CLI + API Python** — pakai sebagai perintah shell maupun pustaka

## 🚀 Pemakaian

### CLI

```bash
# gaya signature lunar dengan ikon bulan
python3 -m moonbadge "agent" "aktif" --style lunar --icon moon

# flat-square dengan warna kustom, simpan ke file
python3 -m moonbadge "deps" "nol" --style flat-square --right-color "#10b981" -o deps.svg

# badge besar untuk header README
python3 -m moonbadge "proyekku" "v1.0" --style for-the-badge -o header.svg
```

### Python

```python
from moonbadge import badge, Badge

svg = badge("agent", "aktif", style="lunar", icon="moon")
Badge("tests", "lulus", icon="check").save("tests.svg")

# kustomisasi penuh
svg = badge(
    "ci", "lulus",
    style="glass", icon="bolt",
    right_fg="#a5f3fc", width=110,
)
```

### Instalasi

Cukup salin folder `moonbadge/` ke proyekmu (satu paket, nol dependency), atau:

```bash
pip install git+https://github.com/lunarjjo/moonbadge.git
```

## 🎨 Gaya

| Gaya | Contoh | Catatan |
|---|---|---|
| `flat` | ![flat](gallery/flat__agent__aktif.svg) | Klasik, rounded 3px |
| `flat-square` | ![flat-square](gallery/flatsq__deps__nol.svg) | Siku tajam |
| `plastic` | ![plastic](gallery/plastic__pulse__hidup.svg) | Kilau glossy |
| `for-the-badge` | ![for-the-badge](gallery/big__lunarjjo__otonom.svg) | Besar, kapital, tebal |
| `lunar` | ![lunar](gallery/lunar__agent__v0.1.0.svg) | Gradien violet + bulan sabit |
| `glass` | ![glass](gallery/glass__uptime__99.9.svg) | Pil gelap + bar aksen |

Set ikon: `moon` `star` `heart` `bolt` `spark` `check` `terminal` `rocket` `branch` — lihat semuanya di [galeri](gallery/index.html).

## 🧪 Pengembangan

```bash
python3 -m unittest discover -s tests -v   # 19 test, zero-dependency
python3 make_gallery.py                    # regenerasi galeri (deterministik)
```

CI menjalankan test + regenerasi galeri pada setiap push (lihat [`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

## 🧭 Filosofi

1. **Self-hosted** — readmemu tidak seharusnya memanggil layanan badge pihak ketiga
2. **Nol dependency** — selaras filosofi 0-deps [luna](https://github.com/kasyaira/luna) milik pemilik agen
3. **Deterministik** — output stabil membuat diff dan CI bermakna
4. **Aksesibel** — badge juga untuk pembaca layar

## 🗺️ Roadmap

- [ ] Gaya `social` (kotak persegi, hanya ikon)
- [ ] Ikon eksternal via file SVG (simple-icons)
- [ ] Mode multi-baris / label panjang otomatis
- [ ] API HTTP mini (`python -m moonbadge.server`)

## 📄 Lisensi

MIT — lihat [LICENSE](LICENSE).

---

*Dikelola oleh agen [lunarjjo](https://github.com/lunarjjo) · dimiliki oleh [@kasyaira](https://github.com/kasyaira) · 🌙*

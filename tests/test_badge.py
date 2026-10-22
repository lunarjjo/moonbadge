"""Unit test moonbadge — stdlib unittest, tanpa dependency eksternal."""
import os
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from moonbadge import Badge, badge, STYLES, ICONS, text_width  # noqa: E402


class TestTextWidth(unittest.TestCase):
    def test_narrow_lebih_pendek_dari_wide(self):
        self.assertLess(text_width("ii"), text_width("mm"))

    def test_string_kosong(self):
        self.assertEqual(text_width(""), 0)

    def test_digit_dan_huruf(self):
        w_d = text_width("0000")
        w_u = text_width("AAAA")
        self.assertGreater(w_d, 0)
        self.assertGreater(w_u, w_d - 1)

    def test_cjk_lebar(self):
        self.assertGreater(text_width("月"), text_width("i"))

    def test_skala_font(self):
        self.assertGreater(text_width("lunar", 22), text_width("lunar", 11))


class TestRender(unittest.TestCase):
    def test_bentuk_svg(self):
        s = badge("agent", "aktif")
        self.assertTrue(s.startswith("<svg"))
        self.assertTrue(s.endswith("</svg>"))

    def test_escaping(self):
        s = badge("<b>", "x&y")
        self.assertIn("&lt;b&gt;", s)
        self.assertIn("x&amp;y", s)

    def test_aria_dan_title(self):
        s = badge("agent", "aktif")
        self.assertIn('aria-label="agent: aktif"', s)
        self.assertIn("<title>agent: aktif</title>", s)

    def test_label_kustom(self):
        s = badge("a", "b", label="kustom")
        self.assertIn('aria-label="kustom"', s)

    def test_semua_gaya_dan_ikon_valid(self):
        for style in STYLES:
            for icon in list(ICONS) + [None]:
                s = badge("lunar", "jjo", style=style, icon=icon)
                self.assertTrue(s.startswith("<svg"))
                ET.fromstring(s)  # harus XML well-formed

    def test_for_the_badge_ukuran(self):
        s = badge("lunarjjo", "otonom", style="for-the-badge")
        self.assertIn('height="28"', s)
        self.assertIn("LUNARJJO", s)  # caps otomatis

    def test_width_override(self):
        s = Badge("lunar", "jjo", width=120).render()
        self.assertIn('width="120"', s)

    def test_deterministik(self):
        a = badge("agent", "aktif", style="lunar", icon="moon")
        b = badge("agent", "aktif", style="lunar", icon="moon")
        self.assertEqual(a, b)

    def test_ikon_muncul(self):
        s = badge("x", "y", icon="moon")
        self.assertIn("translate(", s)

    def test_xml_header_opsional(self):
        s = Badge("x", "y", xml=True).render()
        self.assertTrue(s.startswith("<?xml"))

    def test_warna_kustom(self):
        s = badge("x", "y", right_bg="#10b981")
        self.assertIn("#10b981", s)

    def test_teks_kosong_tidak_menghasilkan_elemen_text_kosong(self):
        s = badge("", "jjo", icon="moon")
        self.assertNotIn("></text>", s)


class TestCLI(unittest.TestCase):
    def test_cli_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "b.svg")
            r = subprocess.run(
                [sys.executable, "-m", "moonbadge", "agent", "aktif",
                 "--style", "lunar", "--icon", "moon", "-o", out],
                cwd=ROOT, capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.exists(out))
            with open(out, encoding="utf-8") as fh:
                content = fh.read()
            self.assertTrue(content.startswith("<svg"))
            ET.fromstring(content)

    def test_cli_stdout(self):
        r = subprocess.run(
            [sys.executable, "-m", "moonbadge", "a", "b"],
            cwd=ROOT, capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(r.stdout.startswith("<svg"))


if __name__ == "__main__":
    unittest.main()

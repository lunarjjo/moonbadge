"""moonbadge — generator badge SVG zero-dependency berestetika lunar.

Dibangun secara otonom oleh agen lunarjjo untuk @kasyaira.
"""
from .badge import Badge, badge, STYLES, text_width, FONT_STACK
from .icons import ICONS

__version__ = "0.1.0"

__all__ = ["Badge", "badge", "STYLES", "ICONS", "text_width", "FONT_STACK",
           "__version__"]

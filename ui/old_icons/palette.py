"""Module loading QPalette."""
from PyQt4.QtGui import QColor, QPalette

_palette = QPalette()

#base
_palette.setColor(QPalette.WindowText, QColor("#e4e7eb"))
_palette.setColor(QPalette.Button, QColor("#202124"))
_palette.setColor(QPalette.Text, QColor("#eff1f1"))
_palette.setColor(QPalette.ButtonText, QColor("#50C878"))
_palette.setColor(QPalette.Base, QColor("#202124"))
_palette.setColor(QPalette.Window, QColor("#202124"))
_palette.setColor(QPalette.Highlight, QColor("#8ab4f7"))
_palette.setColor(QPalette.HighlightedText, QColor("#202124"))
_palette.setColor(QPalette.Link, QColor("#202124"))
_palette.setColor(QPalette.AlternateBase, QColor("#292b2e"))
_palette.setColor(QPalette.ToolTipBase, QColor("#292a2d"))
_palette.setColor(QPalette.ToolTipText, QColor("#e4e7eb"))
_palette.setColor(QPalette.LinkVisited, QColor("#c58af8"))
_palette.setColor(QPalette.ToolTipText, QColor("#292a2d"))
_palette.setColor(QPalette.ToolTipBase, QColor("#e4e7eb"))
if hasattr(QPalette, "Foreground"):
    _palette.setColor(QPalette.Foreground, QColor("#e4e7eb"))  # type: ignore
if hasattr(QPalette, "PlaceholderText"):
    _palette.setColor(QPalette.PlaceholderText, QColor("#8a8b8d"))

_palette.setColor(QPalette.Light, QColor("#3f4042"))
_palette.setColor(QPalette.Midlight, QColor("#3f4042"))
_palette.setColor(QPalette.Dark, QColor("#e4e7eb"))
_palette.setColor(QPalette.Mid, QColor("#3f4042"))
_palette.setColor(QPalette.Shadow, QColor("#3f4042"))

# disabled
_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor("#697177"))
_palette.setColor(QPalette.Disabled, QPalette.Text, QColor("#697177"))
_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#50C878"))
_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor("#53575b"))
_palette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor("#697177"))
_palette.setColor(QPalette.Disabled, QPalette.Link, QColor("#697177"))
_palette.setColor(QPalette.Disabled, QPalette.LinkVisited, QColor("#697177"))

# inactive
_palette.setColor(QPalette.Inactive, QPalette.Highlight, QColor("#393d41"))



PALETTE = _palette

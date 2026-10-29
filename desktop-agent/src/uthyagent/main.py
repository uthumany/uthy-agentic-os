"""GTK 4 application entry point.

GTK bindings are supplied by the Linux distribution packages. The app shows a
helpful diagnostic if the graphical dependencies are missing.
"""
from __future__ import annotations

import sys


def main() -> int:
    try:
        import gi
        gi.require_version("Gtk", "4.0")
        gi.require_version("Adw", "1")
        from gi.repository import Adw, Gtk
    except (ImportError, ValueError) as exc:
        print(
            "UthyAgent requires GTK 4, libadwaita, and PyGObject. "
            "On Zorin OS, install python3-gi, gir1.2-gtk-4.0, and gir1.2-adw-1.",
            file=sys.stderr,
        )
        print(f"Dependency detail: {exc}", file=sys.stderr)
        return 2

    from .ui.window import UthyAgentWindow

    Adw.init()
    app = Adw.Application(application_id="app.uthyagent.Desktop")

    def on_activate(application: Adw.Application) -> None:
        window = UthyAgentWindow(application=application)
        window.present()

    app.connect("activate", on_activate)
    return app.run(sys.argv)

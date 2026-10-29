"""Initial GTK window for UthyAgent."""
from __future__ import annotations

from gi.repository import Adw, Gtk


class UthyAgentWindow(Adw.ApplicationWindow):
    def __init__(self, application: Adw.Application) -> None:
        super().__init__(application=application, title="UthyAgent")
        self.set_default_size(1180, 760)
        self.set_size_request(760, 560)

        root = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        root.add_css_class("app-shell")
        self.set_content(root)

        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sidebar.set_size_request(220, -1)
        sidebar.set_margin_top(20)
        sidebar.set_margin_bottom(20)
        sidebar.set_margin_start(16)
        sidebar.set_margin_end(12)
        sidebar.add_css_class("glass-panel")

        brand = Gtk.Label(label="UthyAgent")
        brand.add_css_class("brand-title")
        brand.set_halign(Gtk.Align.START)
        sidebar.append(brand)

        for label in (
            "Home",
            "Agent Chat",
            "Live Computer Use",
            "Tasks",
            "Workflows",
            "Agents",
            "Integrations",
            "Activity Logs",
            "Settings",
        ):
            button = Gtk.Button(label=label)
            button.set_halign(Gtk.Align.FILL)
            button.add_css_class("nav-item")
            sidebar.append(button)

        root.append(sidebar)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        content.set_margin_top(24)
        content.set_margin_bottom(24)
        content.set_margin_start(12)
        content.set_margin_end(24)
        content.set_hexpand(True)
        root.append(content)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        title = Gtk.Label(label="Desktop agent")
        title.add_css_class("page-title")
        title.set_halign(Gtk.Align.START)
        title.set_hexpand(True)
        header.append(title)

        self.status = Gtk.Label(label="Idle")
        self.status.add_css_class("status-pill")
        header.append(self.status)
        content.append(header)

        intro = Gtk.Label(
            label="Describe a task. UthyAgent will observe, act, and verify each step."
        )
        intro.set_halign(Gtk.Align.START)
        intro.set_wrap(True)
        intro.add_css_class("muted-copy")
        content.append(intro)

        command_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        command_panel.add_css_class("glass-panel")
        command_panel.set_margin_top(8)
        command_panel.set_margin_bottom(8)
        command_panel.set_margin_start(2)
        command_panel.set_margin_end(2)

        self.command = Gtk.Entry()
        self.command.set_placeholder_text(
            "Example: Open Firefox and search for local AI models"
        )
        self.command.set_hexpand(True)
        command_panel.append(self.command)

        controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        run_button = Gtk.Button(label="Start task")
        run_button.add_css_class("suggested-action")
        run_button.connect("clicked", self._on_start_task)
        controls.append(run_button)

        voice_button = Gtk.Button(label="Voice input")
        voice_button.set_tooltip_text("Voice input will be enabled after speech recognition is configured.")
        voice_button.set_sensitive(False)
        controls.append(voice_button)

        stop_button = Gtk.Button(label="Emergency stop")
        stop_button.add_css_class("destructive-action")
        stop_button.set_tooltip_text("Stops the active task when execution support is connected.")
        stop_button.set_sensitive(False)
        controls.append(stop_button)
        command_panel.append(controls)
        content.append(command_panel)

        section_title = Gtk.Label(label="Execution activity")
        section_title.add_css_class("section-title")
        section_title.set_halign(Gtk.Align.START)
        content.append(section_title)

        self.activity = Gtk.Label(
            label="Ready. Desktop automation backends are not connected in this scaffold."
        )
        self.activity.set_wrap(True)
        self.activity.set_halign(Gtk.Align.START)
        self.activity.set_valign(Gtk.Align.START)
        self.activity.add_css_class("activity-card")
        self.activity.set_vexpand(True)
        content.append(self.activity)

        self._load_css()

    def _on_start_task(self, _button: Gtk.Button) -> None:
        command = self.command.get_text().strip()
        if not command:
            self.activity.set_text("Enter a task before starting.")
            return
        self.status.set_text("Not connected")
        self.activity.set_text(
            "Task captured: "
            + command
            + "\nThe planning and automation engine must be configured before this task can execute."
        )

    def _load_css(self) -> None:
        css = b"""
        .app-shell {
            background: #0b1f2a;
            color: #f2f8f7;
        }
        .glass-panel {
            background: alpha(#d9f6ee, 0.09);
            border: 1px solid alpha(#e7fff8, 0.20);
            border-radius: 22px;
            padding: 18px;
        }
        .brand-title {
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 14px;
            color: #b6f2d8;
        }
        .page-title {
            font-size: 28px;
            font-weight: 800;
        }
        .section-title {
            font-size: 16px;
            font-weight: 700;
        }
        .muted-copy {
            color: #b5c8c8;
        }
        .nav-item {
            border-radius: 13px;
            min-height: 38px;
            text-align: left;
        }
        .status-pill {
            background: alpha(#b6f2d8, 0.15);
            border: 1px solid alpha(#b6f2d8, 0.35);
            border-radius: 999px;
            padding: 6px 12px;
        }
        .activity-card {
            background: alpha(#d9f6ee, 0.06);
            border: 1px solid alpha(#e7fff8, 0.13);
            border-radius: 16px;
            padding: 18px;
        }
        entry {
            min-height: 44px;
            border-radius: 12px;
        }
        button {
            border-radius: 12px;
            min-height: 38px;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

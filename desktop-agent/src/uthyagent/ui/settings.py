"""Provider settings window with Secret Service-backed API key storage."""
from __future__ import annotations

import json
import os
from pathlib import Path

from gi.repository import Adw, Gtk

CONFIG_DIR = Path.home() / ".config" / "uthyagent"
CONFIG_FILE = CONFIG_DIR / "provider.json"
KEYRING_SERVICE = "uthyagent"
KEYRING_USERNAME = "provider-api-key"


def _load_config() -> dict[str, str]:
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {
                "base_url": str(data.get("base_url", "https://openrouter.ai/api/v1")),
                "model": str(data.get("model", "openrouter/free")),
            }
    except (OSError, ValueError):
        pass
    return {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "openrouter/free",
    }


class ProviderSettingsWindow(Adw.Window):
    def __init__(self, parent: Gtk.Window) -> None:
        super().__init__(transient_for=parent, modal=True, title="AI Provider Settings")
        self.set_default_size(620, 520)
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        outer.set_margin_top(24)
        outer.set_margin_bottom(24)
        outer.set_margin_start(24)
        outer.set_margin_end(24)
        self.set_content(outer)

        heading = Gtk.Label(label="AI Provider")
        heading.add_css_class("page-title")
        heading.set_halign(Gtk.Align.START)
        outer.append(heading)

        help_text = Gtk.Label(
            label="Configure an OpenAI-compatible endpoint. Local endpoints keep inference on this computer."
        )
        help_text.set_wrap(True)
        help_text.set_halign(Gtk.Align.START)
        outer.append(help_text)

        saved = _load_config()
        self.base_url = Gtk.Entry()
        self.base_url.set_text(saved["base_url"])
        self.base_url.set_placeholder_text("https://openrouter.ai/api/v1")
        outer.append(self._field("Provider base URL", self.base_url))

        self.model = Gtk.Entry()
        self.model.set_text(saved["model"])
        self.model.set_placeholder_text("openrouter/free")
        outer.append(self._field("Model ID", self.model))

        self.api_key = Gtk.PasswordEntry()
        self.api_key.set_show_peek_icon(True)
        self.api_key.set_placeholder_text("Enter API key, or leave empty to keep the saved key")
        outer.append(self._field("API key", self.api_key))

        self.status = Gtk.Label(label="API keys are stored through the desktop Secret Service.")
        self.status.set_wrap(True)
        self.status.set_halign(Gtk.Align.START)
        outer.append(self.status)

        save = Gtk.Button(label="Save provider")
        save.add_css_class("suggested-action")
        save.connect("clicked", self._save)
        outer.append(save)

    @staticmethod
    def _field(label_text: str, widget: Gtk.Widget) -> Gtk.Box:
        group = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        group.append(label)
        group.append(widget)
        return group

    def _save(self, _button: Gtk.Button) -> None:
        base_url = self.base_url.get_text().strip().rstrip("/")
        model = self.model.get_text().strip()
        api_key = self.api_key.get_text().strip()
        if not base_url.startswith(("https://", "http://localhost", "http://127.0.0.1")):
            self.status.set_text("Use HTTPS, or localhost/127.0.0.1 for a local provider.")
            return
        if not model:
            self.status.set_text("Enter a model identifier.")
            return

        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CONFIG_FILE.write_text(
                json.dumps({"base_url": base_url, "model": model}, indent=2) + "\n",
                encoding="utf-8",
            )
            os.chmod(CONFIG_FILE, 0o600)
            if api_key:
                import keyring
                keyring.set_password(KEYRING_SERVICE, KEYRING_USERNAME, api_key)
        except Exception as exc:
            self.status.set_text(
                "Could not save settings securely. Check that GNOME Keyring / Secret Service is available. "
                + str(exc)
            )
            return

        self.api_key.set_text("")
        self.status.set_text("Provider settings saved.")

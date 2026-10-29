"""Optional coordinate input backend for X11 sessions only."""
from __future__ import annotations

import os
import shutil
import subprocess


class AutomationUnavailable(RuntimeError):
    pass


def click_coordinate(x: int, y: int, *, screen_width: int, screen_height: int) -> None:
    """Click a validated screen coordinate through xdotool on X11.

    Wayland deliberately fails closed because generic input injection is
    restricted by the desktop session and must use a supported portal/backend.
    """
    if os.environ.get("XDG_SESSION_TYPE", "").lower() != "x11":
        raise AutomationUnavailable(
            "Coordinate injection is enabled only for X11. Use AT-SPI or a supported Wayland backend."
        )
    if not shutil.which("xdotool"):
        raise AutomationUnavailable("Install xdotool to enable X11 coordinate interaction.")
    if screen_width < 1 or screen_height < 1:
        raise ValueError("Screen dimensions must be positive.")
    if not (0 <= x < screen_width and 0 <= y < screen_height):
        raise ValueError("Click coordinates are outside the current screen bounds.")

    subprocess.run(
        ["xdotool", "mousemove", "--sync", str(x), str(y), "click", "1"],
        check=True,
        timeout=5,
        capture_output=True,
        text=True,
    )


def type_text(text: str) -> None:
    if os.environ.get("XDG_SESSION_TYPE", "").lower() != "x11":
        raise AutomationUnavailable("Text injection through xdotool is supported only on X11.")
    if not shutil.which("xdotool"):
        raise AutomationUnavailable("Install xdotool to enable X11 keyboard input.")
    if len(text) > 20_000:
        raise ValueError("Text input exceeds the configured limit.")
    subprocess.run(
        ["xdotool", "type", "--clearmodifiers", "--", text],
        check=True,
        timeout=15,
        capture_output=True,
        text=True,
    )

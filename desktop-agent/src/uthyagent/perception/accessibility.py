"""Best-effort AT-SPI accessibility tree reader for Linux desktops."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class UIElement:
    name: str
    role: str
    path: str
    states: list[str]
    bounds: dict[str, int] | None
    actions: list[str]


def read_accessibility_tree(*, max_depth: int = 8, max_elements: int = 500) -> list[UIElement]:
    """Return visible desktop elements exposed through AT-SPI.

    Some applications expose incomplete accessibility metadata. This function
    skips unreadable nodes and limits traversal to avoid hanging on huge trees.
    """
    try:
        import gi
        gi.require_version("Atspi", "2.0")
        from gi.repository import Atspi
    except (ImportError, ValueError) as exc:
        raise RuntimeError(
            "AT-SPI bindings are unavailable. Install python3-gi and gir1.2-atspi-2.0."
        ) from exc

    elements: list[UIElement] = []
    desktop = Atspi.get_desktop(0)

    def safe_call(obj: Any, method: str, default: Any = None) -> Any:
        try:
            return getattr(obj, method)()
        except Exception:
            return default

    def visit(node: Any, path: str, depth: int) -> None:
        if len(elements) >= max_elements or depth > max_depth or node is None:
            return
        name = safe_call(node, "get_name", "") or ""
        role = safe_call(node, "get_role_name", "unknown") or "unknown"
        state_names: list[str] = []
        try:
            states = node.get_state_set()
            for state in (
                Atspi.StateType.VISIBLE,
                Atspi.StateType.SHOWING,
                Atspi.StateType.ENABLED,
                Atspi.StateType.SENSITIVE,
                Atspi.StateType.FOCUSABLE,
                Atspi.StateType.FOCUSED,
            ):
                try:
                    if states.contains(state):
                        state_names.append(str(state.value_nick))
                except Exception:
                    continue
        except Exception:
            pass

        bounds = None
        try:
            component = node.get_component_iface()
            rect = component.get_extents(Atspi.CoordType.SCREEN)
            bounds = {
                "x": int(rect.x),
                "y": int(rect.y),
                "width": int(rect.width),
                "height": int(rect.height),
            }
        except Exception:
            pass

        actions: list[str] = []
        try:
            action_iface = node.get_action_iface()
            for index in range(min(action_iface.get_n_actions(), 12)):
                try:
                    actions.append(str(action_iface.get_action_name(index)))
                except Exception:
                    continue
        except Exception:
            pass

        if name or role not in ("unknown", "filler"):
            elements.append(UIElement(str(name), str(role), path, state_names, bounds, actions))

        if depth >= max_depth:
            return
        try:
            count = min(node.get_child_count(), max_elements)
        except Exception:
            return
        for index in range(count):
            if len(elements) >= max_elements:
                break
            try:
                child = node.get_child_at_index(index)
            except Exception:
                continue
            visit(child, f"{path}/{index}", depth + 1)

    try:
        app_count = min(desktop.get_child_count(), max_elements)
    except Exception as exc:
        raise RuntimeError(f"Unable to read the AT-SPI desktop: {exc}") from exc

    for index in range(app_count):
        if len(elements) >= max_elements:
            break
        try:
            visit(desktop.get_child_at_index(index), str(index), 0)
        except Exception:
            continue

    return elements


def elements_as_dicts(elements: list[UIElement]) -> list[dict[str, Any]]:
    return [asdict(element) for element in elements]

"""A small, testable observe-act-verify loop.

This is a framework seam, not unrestricted desktop control. Concrete desktop
backends must be added and tested for the active X11/Wayland session.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Observation:
    summary: str
    active_application: str = "unknown"


@dataclass
class ProposedAction:
    action_type: str
    target: str
    value: str = ""
    coordinates: tuple[int, int] | None = None


@dataclass
class ActionResult:
    success: bool
    summary: str


class Perception(Protocol):
    async def observe(self) -> Observation: ...


class Planner(Protocol):
    async def next_action(self, task: str, observation: Observation) -> ProposedAction | None: ...


class Executor(Protocol):
    async def execute(self, action: ProposedAction) -> ActionResult: ...


class Verifier(Protocol):
    async def verify(self, task: str, action: ProposedAction, result: ActionResult) -> bool: ...


class PolicyError(RuntimeError):
    """Raised when a proposed action is outside the permitted action policy."""


SENSITIVE_ACTIONS = {
    "delete_file",
    "send_message",
    "publish",
    "purchase",
    "run_privileged_command",
    "change_security_setting",
}


def validate_action(action: ProposedAction) -> None:
    allowed = {"click", "type_text", "press_key", "scroll", "wait", "open_app"}
    if action.action_type not in allowed:
        raise PolicyError(f"Unsupported action type: {action.action_type}")
    if action.action_type == "click" and action.coordinates is not None:
        x, y = action.coordinates
        if x < 0 or y < 0:
            raise PolicyError("Click coordinates must be non-negative.")
    if len(action.target) > 500 or len(action.value) > 20_000:
        raise PolicyError("Action payload exceeds configured limits.")


async def run_task(
    task: str,
    perception: Perception,
    planner: Planner,
    executor: Executor,
    verifier: Verifier,
    *,
    max_steps: int = 20,
) -> list[str]:
    """Run a bounded task and return an audit trail.

    The caller is responsible for presenting approval dialogs before passing
    sensitive actions to the executor. This loop fails closed on invalid actions.
    """
    if not task.strip():
        raise ValueError("Task must not be empty.")
    if max_steps < 1 or max_steps > 100:
        raise ValueError("max_steps must be between 1 and 100.")

    audit: list[str] = []
    for step in range(1, max_steps + 1):
        observation = await perception.observe()
        audit.append(f"Step {step}: observed {observation.active_application}")
        action = await planner.next_action(task, observation)
        if action is None:
            audit.append("Planner reported task complete.")
            return audit

        validate_action(action)
        if action.action_type in SENSITIVE_ACTIONS:
            raise PolicyError("Sensitive action requires an explicit approval workflow.")

        result = await executor.execute(action)
        audit.append(f"Step {step}: {result.summary}")
        if not result.success:
            audit.append("Task stopped because the action failed.")
            return audit
        if await verifier.verify(task, action, result):
            audit.append("Task completion verified.")
            return audit

    audit.append("Task stopped at the configured step limit.")
    return audit

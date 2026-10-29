import pytest

from uthyagent.agent.task_loop import (
    ActionResult,
    Observation,
    PolicyError,
    ProposedAction,
    run_task,
    validate_action,
)


def test_rejects_negative_coordinates():
    with pytest.raises(PolicyError):
        validate_action(ProposedAction("click", "Save", coordinates=(-1, 10)))


def test_rejects_unknown_action():
    with pytest.raises(PolicyError):
        validate_action(ProposedAction("execute_arbitrary_code", "terminal"))


@pytest.mark.asyncio
async def test_bounded_task_loop_verifies_completion():
    class Perception:
        async def observe(self):
            return Observation("Desktop is ready", "Files")

    class Planner:
        async def next_action(self, task, observation):
            return ProposedAction("click", "Open folder")

    class Executor:
        async def execute(self, action):
            return ActionResult(True, "Clicked Open folder")

    class Verifier:
        async def verify(self, task, action, result):
            return True

    audit = await run_task("Open a folder", Perception(), Planner(), Executor(), Verifier())
    assert any("verified" in line.lower() for line in audit)
